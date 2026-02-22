#!/usr/bin/env python3
"""
split_md.py — 按语义边界拆分大 Markdown 文件

用法：
    python split_md.py input.md --max-lines 600 --min-lines 100 --max-size 20000 --min-part-lines 20 --output-dir ./_parts/

输出：
    _part_01.md, _part_02.md, ... + _split_manifest.json

--- 核心逻辑 ---

拆分触发条件：行数超出 max-lines 或字节大小超出 max-size（UTF-8），任一满足即触发。

每个片段的搜索窗口为 [current + min_lines, min(current + max_lines, size_limit_line)]，
其中 size_limit_line 通过对预计算的字节前缀和数组执行二分查找得出。

拆分点优先级（从高到低）：
  H1 标题 > H2 标题 > H3 标题 > 任意标题 > 空行 > 强制截断

代码块保护（向前优先策略）：
  若选中的拆分点落在代码块内，优先向前移到开始 ``` 之前。
  若代码块起始位置已在当前片段起始之前（即窗口整体落在代码块内部），
  为满足 max-size 硬约束，将在代码块内部强制拆分，并输出警告。
"""

import argparse
import io
import json
import re
import sys
from pathlib import Path

# Windows 下强制 UTF-8 输出，避免 GBK 编码错误
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def parse_args():
    parser = argparse.ArgumentParser(description="按语义边界拆分大 Markdown 文件")
    parser.add_argument("input", help="输入 Markdown 文件路径")
    parser.add_argument("--max-lines", type=int, default=600, help="每个片段最大行数（默认 600）")
    parser.add_argument("--min-lines", type=int, default=100, help="每个片段最小行数（默认 100）")
    parser.add_argument("--max-size", type=int, default=20000,
                        help="每个片段最大字节数，UTF-8 编码（默认 20000）")
    parser.add_argument("--min-part-lines", type=int, default=20,
                        help="拆分后片段最小行数；低于该值时尝试与相邻片段合并（默认 20，设为 0 表示关闭）")
    parser.add_argument("--output-dir", default="./_parts/", help="输出目录（默认 ./_parts/）")
    return parser.parse_args()


def read_lines(filepath: str) -> list[str]:
    """读取文件所有行，保留换行符。"""
    path = Path(filepath)
    if not path.exists():
        print(f"错误：文件不存在 - {filepath}", file=sys.stderr)
        sys.exit(1)
    return path.read_text(encoding="utf-8").splitlines(keepends=True)


def find_heading_positions(lines: list[str]) -> list[tuple[int, int]]:
    """
    找出所有标题行的位置和层级。
    返回 [(行号, 层级), ...]，行号从 0 开始。
    跳过代码块内的 # 符号。
    """
    headings = []
    in_code_block = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # 检测代码块边界
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        # 匹配 ATX 风格标题
        match = re.match(r'^(#{1,6})\s+\S', line)
        if match:
            level = len(match.group(1))
            headings.append((i, level))

    return headings


def get_title_text(line: str) -> str:
    """从标题行提取标题文本。"""
    match = re.match(r'^#{1,6}\s+(.+?)(?:\s*#*\s*)?$', line.strip())
    return match.group(1).strip() if match else line.strip()


def precompute_code_block_ranges(lines: list[str]) -> list[tuple[int, int]]:
    """
    预计算所有代码块的行号区间。
    返回 [(start, end), ...]，start 是 ``` 开始行，end 是 ``` 结束行。
    """
    ranges = []
    open_line = None

    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
            if open_line is None:
                open_line = i
            else:
                ranges.append((open_line, i))
                open_line = None

    # 未闭合的代码块延伸到文件末尾
    if open_line is not None:
        ranges.append((open_line, len(lines)))

    return ranges


def is_in_code_block_fast(code_block_ranges: list[tuple[int, int]], line_idx: int) -> bool:
    """用二分搜索判断指定行是否在代码块内。"""
    if not code_block_ranges:
        return False

    lo, hi = 0, len(code_block_ranges) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        start, end = code_block_ranges[mid]
        if line_idx < start:
            hi = mid - 1
        elif line_idx > end:
            lo = mid + 1
        else:
            return True
    return False


def find_enclosing_code_block(code_block_ranges: list[tuple[int, int]],
                               line_idx: int) -> tuple[int, int] | None:
    """找到包含指定行的代码块范围，返回 (start, end) 或 None。"""
    if not code_block_ranges:
        return None

    lo, hi = 0, len(code_block_ranges) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        start, end = code_block_ranges[mid]
        if line_idx < start:
            hi = mid - 1
        elif line_idx > end:
            lo = mid + 1
        else:
            return start, end
    return None


def is_in_list(lines: list[str], line_idx: int) -> bool:
    """判断指定行是否在列表中间。"""
    if line_idx >= len(lines):
        return False
    line = lines[line_idx].strip()
    if re.match(r'^[-*+]\s|^\d+\.\s', line):
        return True
    if line and line_idx > 0:
        prev = lines[line_idx - 1].strip()
        if re.match(r'^[-*+]\s|^\d+\.\s', prev):
            return True
    return False


def compute_byte_prefix(lines: list[str]) -> list[int]:
    """
    计算每行的累积 UTF-8 字节前缀和。
    prefix[i] 是前 i 行（lines[0..i-1]）的总字节数。
    lines[start:end] 的字节数 = prefix[end] - prefix[start]。
    """
    prefix = [0]
    for line in lines:
        prefix.append(prefix[-1] + len(line.encode("utf-8")))
    return prefix


def find_size_limit_line(byte_prefix: list[int], current_start: int,
                          max_size: int, total: int) -> int:
    """
    二分查找：从 current_start 开始，不超过 max_size 字节的最远行号。
    返回值 n 满足：byte_prefix[n] - byte_prefix[current_start] <= max_size。
    """
    target = byte_prefix[current_start] + max_size
    lo, hi = current_start, total
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if byte_prefix[mid] <= target:
            lo = mid
        else:
            hi = mid - 1
    return lo


def find_split_points(lines: list[str], headings: list[tuple[int, int]],
                      max_lines: int, min_lines: int,
                      byte_prefix: list[int] | None = None,
                      max_size: int | None = None) -> list[int]:
    """
    确定拆分点（行号列表）。
    优先在一级标题处拆，其次二级、三级。
    确保每个片段不超过 max_lines 行且不超过 max_size 字节（如指定）。
    代码块保护：拆分点落在代码块内时，向前移到代码块开始之前。
    """
    total = len(lines)

    # 初始检查：行数和大小都不超则无需拆分
    size_ok = (max_size is None or byte_prefix is None or
               byte_prefix[total] - byte_prefix[0] <= max_size)
    if total <= max_lines and size_ok:
        return []

    # 预计算代码块区间
    code_block_ranges = precompute_code_block_ranges(lines)

    # 按层级分组标题位置
    h1_positions = [pos for pos, level in headings if level == 1]
    h2_positions = [pos for pos, level in headings if level == 2]
    h3_positions = [pos for pos, level in headings if level == 3]
    all_heading_positions = sorted([pos for pos, _ in headings])

    split_points = []
    current_start = 0

    while current_start < total:
        remaining = total - current_start

        # 终止条件：行数不超，且大小不超（如有大小限制）
        if remaining <= max_lines:
            if max_size is None or byte_prefix is None:
                break
            current_size = byte_prefix[total] - byte_prefix[current_start]
            if current_size <= max_size:
                break

        # 大小约束：计算从 current_start 开始不超过 max_size 字节的最远行
        if max_size is not None and byte_prefix is not None:
            size_limit_line = find_size_limit_line(byte_prefix, current_start, max_size, total)
        else:
            size_limit_line = total

        # search_end 取行数上限和大小上限两者的最小值
        search_end = min(current_start + max_lines, size_limit_line, total)
        search_start = current_start + min_lines

        # 如果 min_lines 范围内就已超出大小限制，收缩 search_start
        if search_start > search_end:
            search_start = current_start + 1  # 至少向前推进 1 行，防止死循环

        best_point = None

        # 优先找 H1
        for pos in h1_positions:
            if search_start <= pos <= search_end:
                best_point = pos
                break

        # 其次找 H2
        if best_point is None:
            for pos in h2_positions:
                if search_start <= pos <= search_end:
                    best_point = pos
                    break

        # 再找 H3
        if best_point is None:
            for pos in h3_positions:
                if search_start <= pos <= search_end:
                    best_point = pos
                    break

        # 找任意标题
        if best_point is None:
            for pos in all_heading_positions:
                if search_start <= pos <= search_end:
                    best_point = pos
                    break

        # 找空行作为段落边界（从 search_end 向前扫）
        if best_point is None:
            for pos in range(search_end - 1, search_start - 1, -1):
                if pos < total and lines[pos].strip() == "":
                    if not is_in_code_block_fast(code_block_ranges, pos) and not is_in_list(lines, pos):
                        best_point = pos + 1
                        break

        # 实在找不到，强制在 search_end 处拆
        if best_point is None:
            best_point = search_end

        # 代码块保护：向前优先策略
        # 拆分点落在代码块内 → 优先向前移到代码块开始之前（保守，不超大小限制）
        # 若代码块从当前片段起始前就已开始（窗口整体在代码块内）：
        # 为满足 max-size 硬约束，允许在代码块内部强制拆分并告警
        if is_in_code_block_fast(code_block_ranges, best_point):
            block = find_enclosing_code_block(code_block_ranges, best_point)
            if block:
                code_start, code_end = block
                if code_start > current_start:
                    # 在代码块开始前拆，新片段从代码块 ``` 行开始
                    best_point = code_start
                else:
                    # 代码块从当前片段起始就存在：为满足 max-size 硬约束，允许在代码块内部强制切分。
                    # 这样会把一个超长代码块拆成多个片段，但可确保每个片段大小受控。
                    best_point = search_end
                    if best_point <= current_start:
                        best_point = min(current_start + 1, total)
                    print(
                        f"  警告：代码块跨越拆分窗口（行 {code_start + 1}-{code_end + 1}），"
                        f"为满足大小限制，已在代码块内部强制拆分",
                        file=sys.stderr
                    )

        # best_point 达到文件末尾，剩余内容作为最后一片，不再继续
        if best_point >= total:
            break

        split_points.append(best_point)
        current_start = best_point

    return split_points


def get_context_lines(lines: list[str], start: int, end: int,
                      prev_end: int, next_start: int) -> dict:
    """生成上下文信息。"""
    context = {}

    # 前文最后 5 行
    if start > 0:
        ctx_start = max(prev_end if prev_end >= 0 else 0, start - 5)
        context["preceding_lines"] = [l.rstrip("\n\r") for l in lines[ctx_start:start]]

    # 后文前 3 行
    if end < len(lines):
        ctx_end = min(next_start if next_start > 0 else len(lines), end + 3)
        context["following_lines"] = [l.rstrip("\n\r") for l in lines[end:ctx_end]]

    return context


def get_title_range(lines: list[str], start: int, end: int) -> str:
    """获取片段内的标题范围描述。"""
    titles = []
    in_code = False
    for i in range(start, min(end, len(lines))):
        stripped = lines[i].strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        match = re.match(r'^#{1,6}\s+(.+?)(?:\s*#*\s*)?$', stripped)
        if match:
            titles.append(match.group(1).strip())

    if not titles:
        return f"Lines {start + 1}-{end}"
    if len(titles) == 1:
        return titles[0]
    return f"{titles[0]} ~ {titles[-1]}"


def merge_small_parts(boundaries: list[int], byte_prefix: list[int],
                      max_lines: int, max_size: int,
                      min_part_lines: int) -> list[int]:
    """
    合并过小片段，避免碎片化输出。
    策略：优先并入前一片段，不满足约束时尝试并入后一片段。
    合并时严格满足 max-lines 和 max-size。
    """
    if min_part_lines <= 0 or len(boundaries) <= 2:
        return boundaries

    parts = [[boundaries[i], boundaries[i + 1]] for i in range(len(boundaries) - 1)]
    i = 0
    while i < len(parts):
        start, end = parts[i]
        lines_count = end - start

        # 最后一片且只有单片时不处理
        if len(parts) == 1 or lines_count >= min_part_lines:
            i += 1
            continue

        merged = False

        # 优先并入前一片
        if i > 0:
            prev_start, _ = parts[i - 1]
            merged_start = prev_start
            merged_end = end
            merged_lines = merged_end - merged_start
            merged_bytes = byte_prefix[merged_end] - byte_prefix[merged_start]
            if merged_lines <= max_lines and merged_bytes <= max_size:
                parts[i - 1][1] = end
                del parts[i]
                merged = True
                i = max(i - 1, 0)

        # 前一片不满足约束时，尝试并入后一片
        if not merged and i + 1 < len(parts):
            _, next_end = parts[i + 1]
            merged_start = start
            merged_end = next_end
            merged_lines = merged_end - merged_start
            merged_bytes = byte_prefix[merged_end] - byte_prefix[merged_start]
            if merged_lines <= max_lines and merged_bytes <= max_size:
                parts[i][1] = next_end
                del parts[i + 1]
                merged = True

        if not merged:
            i += 1

    merged_boundaries = [parts[0][0]]
    for _, end in parts:
        merged_boundaries.append(end)
    return merged_boundaries


def main():
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    lines = read_lines(str(input_path))
    total_lines = len(lines)

    # 预计算字节前缀和
    byte_prefix = compute_byte_prefix(lines)
    total_bytes = byte_prefix[total_lines]

    print(f"文件：{input_path.name}")
    print(f"总行数：{total_lines}，总大小：{total_bytes / 1024:.1f} kB")
    print(f"限制：每片段最多 {args.max_lines} 行 / {args.max_size / 1024:.1f} kB")

    # 检查是否需要拆分
    if total_lines <= args.max_lines and total_bytes <= args.max_size:
        print("文件未超过任何阈值，无需拆分。")
        sys.exit(0)

    # 找标题位置
    headings = find_heading_positions(lines)
    print(f"发现 {len(headings)} 个标题")

    # 确定拆分点
    split_points = find_split_points(
        lines, headings,
        args.max_lines, args.min_lines,
        byte_prefix=byte_prefix,
        max_size=args.max_size,
    )

    if not split_points:
        print("未找到合适的拆分点。")
        sys.exit(0)

    boundaries = [0] + split_points + [total_lines]
    if args.min_part_lines > 0 and len(boundaries) > 2:
        merged_boundaries = merge_small_parts(
            boundaries,
            byte_prefix,
            args.max_lines,
            args.max_size,
            args.min_part_lines,
        )
        if len(merged_boundaries) != len(boundaries):
            print(
                f"小片段合并：{len(boundaries) - 1} 片 -> {len(merged_boundaries) - 1} 片 "
                f"（阈值：{args.min_part_lines} 行）"
            )
        boundaries = merged_boundaries

    parts = []

    for i in range(len(boundaries) - 1):
        start = boundaries[i]
        end = boundaries[i + 1]
        part_num = i + 1
        part_filename = f"_part_{part_num:02d}.md"
        part_path = output_dir / part_filename

        # 写入片段文件
        content = "".join(lines[start:end])
        part_path.write_text(content, encoding="utf-8")

        size_bytes = byte_prefix[end] - byte_prefix[start]

        # 上下文信息
        prev_end = boundaries[i - 1] if i > 0 else -1
        next_start = boundaries[i + 2] if i + 2 < len(boundaries) else -1
        context = get_context_lines(lines, start, end, prev_end, next_start)

        # 写上下文文件
        if context:
            ctx_path = output_dir / f"_part_{part_num:02d}_context.json"
            ctx_path.write_text(json.dumps(context, ensure_ascii=False, indent=2),
                                encoding="utf-8")

        title_range = get_title_range(lines, start, end)

        # 大小超限警告
        if size_bytes > args.max_size:
            print(
                f"  警告：{part_filename} 大小 {size_bytes / 1024:.1f} kB 超出限制 "
                f"{args.max_size / 1024:.1f} kB（可能含超大代码块）",
                file=sys.stderr
            )

        parts.append({
            "file": part_filename,
            "start_line": start + 1,  # 转为 1-based
            "end_line": end,
            "lines": end - start,
            "size_bytes": size_bytes,
            "title_range": title_range,
        })

        print(f"  {part_filename}: 行 {start + 1}-{end} ({end - start} 行, {size_bytes / 1024:.1f} kB) [{title_range}]")

    # 生成 manifest
    manifest = {
        "source": input_path.name,
        "source_path": str(input_path),
        "total_lines": total_lines,
        "total_bytes": total_bytes,
        "parts_count": len(parts),
        "parts": parts,
    }

    manifest_path = output_dir / "_split_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2),
                             encoding="utf-8")

    print(f"\n拆分完成：{len(parts)} 个片段")
    print(f"清单文件：{manifest_path}")


if __name__ == "__main__":
    main()
