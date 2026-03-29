# 氮气引擎 / Nitro Engine

[English](./README.md)

> 一个 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 技能——让 AI 翻译读起来不像翻译。

**支持任意语言对**，目前在英→中上测试验证，其他语言对欢迎反馈。

---

## 维护模式

不带翻译目标直接调用 `/translate` 会进入维护模式，提供四个选项：

- **更新词汇表** — 管理领域术语对照，越用越准
- **更新翻译样本** — 记录喜欢的翻译风格，让 AI 学习你的偏好
- **翻译讨论** — 回顾近期翻译质量，讨论难译词汇和风格取舍
- **配置管理** — 查看和修改翻译设置

所有修改即时生效，无需重启。

---

## 效果对比

| 原文 | 普通 AI 翻译 | 氮气引擎 |
|------|-------------|---------|
| The fact that the system is widely adopted by developers suggests that it addresses a genuine need. | 系统被开发者广泛采用的事实表明它解决了真正的需求。 | 既然这么多开发者都在用，说明它确实解决了实际问题。 |
| It is important to note that this approach may not be suitable for all use cases. | 重要的是要注意，这种方法可能不适用于所有用例。 | 值得一提的是，这套方法并非放之四海而皆准。 |
| The analysis of data was conducted using Python. | 数据的分析是使用 Python 进行的。 | 我们用 Python 分析了数据。 |

---

## 为什么用这个

**流畅自然** — 翻译即写作，不是逐词转换。读译文应该感觉原文就是用母语写的。

**领域适配** — 自定义术语表和翻译样本，适配你的行业、团队或个人偏好，用得越多越懂你。

**大规模处理** — 多 Agent 并发翻译，轻松应对超长文档和整个文件夹的批量翻译，且风格始终如一。

---

## 快速上手

**前置条件**：[Claude Code](https://docs.anthropic.com/en/docs/claude-code) + 订阅套餐。

**1. 安装技能**

```bash
# 将 translate/ 目录复制到 Claude Code 技能目录
cp -r translate ~/.claude/skills/
```

**2. 开始翻译**

```
翻译 path/to/document.md 为中文
```

翻译整个文件夹：

```
将 path/to/folder/ 下所有 Markdown 文件翻译为中文
```

译文自动生成在同目录下，带语言后缀（如 `document_zh.md`）。

---

## 注意事项

- **仅支持 Markdown 和纯文本**，PDF 等格式需先转为 Markdown（推荐 [MinerU](https://github.com/opendatalab/MinerU)）
- **Token 消耗较高**，使用多 Agent 并行翻译，强烈建议订阅套餐而非按量付费
- **代码块保持原样**，不会被翻译（注释可翻译）
- **永远不覆盖源文件**，输出带语言后缀

---

## 许可证

[CC BY 4.0](./LICENSE) — 自由使用、修改、分发，包括商用，保留署名即可。

---

如果觉得好用，请给个 ⭐ 支持一下！这个项目会持续更新优化。
