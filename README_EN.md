# Nitro Engine / 氮气引擎

[中文文档](./README.md)

> Translation is writing — not conversion, but re-expression.

A Claude Code skill for translating Markdown documents with a focus on **natural, fluent prose**.

**Version**: `v1.0.0`

**Supports any language pair.** Currently tested on English → Chinese. Community testing and feedback for other language pairs are welcome.

---

## The Problem with "Accurate" Translations

Machine translation is fast. AI translation is faster. But the output often reads like... a translation.

Compare:

| Source | Typical Translation | What This Skill Aims For |
|--------|---------------------|--------------------------|
| The fact that the system is widely adopted by developers suggests that it addresses a genuine need. | 系统被开发者广泛采用的事实表明它解决了真正的需求。 | 既然这么多开发者都在用，说明它确实解决了实际问题。 |
| It is important to note that this approach may not be suitable for all use cases. | 重要的是要注意，这种方法可能不适用于所有用例。 | 值得一提的是，这套方法并非放之四海而皆准。 |
| The analysis of data was conducted using Python. | 数据的分析是使用 Python 进行的。 | 我们用 Python 分析了数据。 |

All three "accurate" translations are grammatically correct. But they read like translations — passive, Europeanized, stiff.

This skill takes a different approach: **translation as writing**. The goal isn't to convert words — it's to let the same meaning find its natural voice in the target language.

---

## Core Philosophy

> **翻译即写作** — Translation is writing across languages.

Not conversion. Re-expression.

A good translation should feel like the original author wrote it in the target language. Readers shouldn't sense they're reading something that was "carried over" from another tongue.

This is hard to achieve. This skill is an attempt to apply AI capabilities in service of that ideal.

---

## How It Works

### Three-Step Process

Most translation tools skip straight to "convert." This skill follows a different path:

**1. Reconstruct** — Build a mental model of the source text
- Who's speaking? To whom? In what context?
- A technical doc feels like "an expert walking you through something"
- A blog post feels like "a friend sharing experience"
- This "imaginative space" sets the ceiling for translation quality

**2. Negotiate** — Make judgment calls
- What does this word *actually* mean in this context?
- How would a native speaker naturally express this concept?
- Decisions are captured in a glossary and translation brief

**3. Write** — Compose in the target language
- Not word-for-word substitution
- Speaking from inside the imaginative space, in the target language

### Consistency at Scale

Long documents get split into segments and translated in parallel. But unlike naive parallelization:

- A **translation brief** captures the document's tone, style, and key decisions *before* any translation begins
- A **tone sample** anchors all agents to the same stylistic baseline
- A **shared glossary** ensures terminology consistency across all segments

Result: a 10,000-line document reads like one person wrote it, not ten.

### Customizable for Your Domain

Different fields have different terminology standards. This skill supports:

- **User glossary** (`user-glossary.md`) — Define how specific terms should be translated. The skill respects your choices consistently across all documents.
- **Translation samples** (`user-samples.md`) — Provide examples of translations you like. The skill uses them as a style reference.

Over time, these files accumulate and the skill becomes increasingly aligned with your domain's conventions.

### Locale-Aware (Chinese)

Chinese isn't just Chinese. This skill differentiates between regions:

| English | Mainland (zh-CN) | Taiwan (zh-TW) | Hong Kong (zh-HK) |
|---------|------------------|----------------|-------------------|
| software | 软件 | 軟體 | 軟體 |
| program | 程序 | 程式 | 程式 |
| network | 网络 | 網路 | 網路 |
| database | 数据库 | 資料庫 | 資料庫 |

Specify the target locale in the translation brief, and the skill adjusts accordingly.

---

## Workflow

```
Phase 0: Input Analysis
├── Detect language, assess scale, choose strategy
│
Phase 1: Read-Through & Preparation
├── Generate glossary (_glossary.md)
├── Generate translation brief (_translation_brief.md)
├── Split large files if needed (>1000 lines)
│
Phase 1.5: Tone Anchoring (large files only)
├── Translate a representative passage as style reference
│
Phase 2: Translation Execution
├── Small files: primary agent translates directly
├── Large files: sub-agents translate in parallel
│
Phase 3: Verification & Merge
├── Format check, terminology consistency
├── Merge segments, smooth boundaries
│
Phase 4: Output Cleanup
├── Write new terms back to user glossary
├── Clean up temporary files
```

---

## Quick Start

**Prerequisites**: [Claude Code](https://github.com/anthropics/claude-code) CLI with a Coding subscription plan.

1. Copy the skill to your Claude Code skills directory:

```bash
cp -r translate ~/.claude/skills/
```

2. Invoke the skill with natural language:

```
Translate path/to/document.md into Chinese.
```

Or translate all Markdown files in a folder:

```
Translate all Markdown files under path/to/folder/ into Chinese.
```

3. Translated files appear with language suffix (e.g., `document_zh.md`) in the same directory.

---

## What's Included

```
translate/
├── SKILL.md                          # Main skill file
├── scripts/
│   ├── split_md.py                   # Split at semantic boundaries
│   └── merge_md.py                   # Merge with format validation
└── references/
    ├── locale-styles.md              # Regional Chinese differences
    ├── refinement-guide.md           # Optional post-translation polish
    ├── subagent-prompt.md            # Template for parallel agents
    ├── translation-brief-template.md # Style/tone documentation
    ├── user-glossary.md              # Your accumulated terms (persists)
    └── user-samples.md               # Your translation samples (persists)
```

---

## Important Notes

### Token Consumption

This skill uses a primary agent with sub-agents for parallel translation. It's a **token killer**.

- For long documents (>1000 lines), multiple sub-agents are dispatched simultaneously
- **Claude Code** is required (this is a Claude Code skill)
- A **Coding subscription plan** is strongly recommended (Claude Max, GLM Coding, or similar)
- Pay-per-use API will get expensive quickly for large documents

### Concurrency Limits (GLM Coding Plan)

During peak hours, GLM Coding plans may have insufficient resources. Before starting:

1. Tell Claude to limit concurrent sub-agents based on your plan:
   ```
   Limit concurrent sub-agents to N (adjust N based on your subscription tier).
   ```

2. For very large documents during peak hours, request smaller segment splits:
   ```
   Split into smaller segments (e.g., 300 lines each) instead of default 600 lines.
   ```

This prevents "resource exhausted" errors and improves success rates.

### Model Compatibility

Tested on **GLM5**. Other models are untested.

- Theoretically, Opus should produce better writing quality
- If you test on other models, feedback is welcome

### Translating PDFs

This skill only handles Markdown. For PDFs:

1. Convert PDF to Markdown using [MinerU](https://github.com/opendatalab/MinerU)
2. Run `/clear` to reset context
3. Translate the converted Markdown
4. Run `/clear` again
5. Ask Claude to fix formatting issues:

```
Check and fix heading hierarchy issues in XXX_zh.md, and repair Markdown formatting.
```

**Why `/clear` between steps?** Each step involves significant context. Clearing ensures optimal performance and prevents context pollution from affecting translation quality.

MinerU's output often has incorrect heading levels and minor Markdown syntax issues that need manual cleanup.

---

## Limitations

- **Input formats**: Markdown and plain text only. PDFs, Word docs, and web pages must be converted to Markdown first.
- **Language coverage**: Supports any language pair. Currently tested on English → Chinese; other pairs await community verification.
- **Code blocks**: Contents of code blocks are preserved as-is (inline code comments may be translated).
- **Quality ceiling**: The skill provides structure and process, but final quality depends on the underlying model's writing ability.

---

## Who This Is For

- People translating long technical documents who care about readability
- People frustrated by "technically correct but unnatural" translations
- People willing to invest a bit more time for significantly better output

---

## Background

Standard machine translation often produces output that's "accurate but painful to read" — grammatically correct, yet stiff and unnatural. The problem isn't accuracy; it's that translation is treated as word conversion rather than re-expression.

This skill applies a different philosophy: translation as writing. The goal is to produce text that feels like it was originally written in the target language.

Built for Claude Code, it leverages agent capabilities to maintain consistency across long documents while respecting domain-specific terminology and style preferences.

---

## License

MIT License with Attribution Requirement.

You are free to use, modify, and distribute this software. For **proprietary or commercial use**, please include attribution in your documentation or about page:

```
Translation skill based on: https://github.com/FuHehe12/Nitro-Engine
```

For open-source projects, standard MIT terms apply (just keep the license file).
