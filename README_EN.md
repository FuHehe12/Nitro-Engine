# Nitro Engine / 氮气引擎

[中文文档](./README.md)

> A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill — AI translation that doesn't read like a translation.

**Supports any language pair.** Currently tested on English → Chinese. Feedback on other pairs welcome.

---

## Maintenance Mode

Running `/translate` without a target file opens maintenance mode with four options:

- **Update glossary** — Manage domain-specific term mappings; the more you add, the more accurate translations become
- **Update translation samples** — Record translation styles you like so the AI learns your preferences
- **Translation discussion** — Review recent translations, discuss tricky terms and style trade-offs
- **Configuration** — View and modify translation settings

All changes take effect immediately — no restart needed.

---

## See the Difference

| Source | Typical AI Translation | Nitro Engine |
|--------|----------------------|--------------|
| The fact that the system is widely adopted by developers suggests that it addresses a genuine need. | 系统被开发者广泛采用的事实表明它解决了真正的需求。 | 既然这么多开发者都在用，说明它确实解决了实际问题。 |
| It is important to note that this approach may not be suitable for all use cases. | 重要的是要注意，这种方法可能不适用于所有用例。 | 值得一提的是，这套方法并非放之四海而皆准。 |
| The analysis of data was conducted using Python. | 数据的分析是使用 Python 进行的。 | 我们用 Python 分析了数据。 |

---

## Why This Skill

**Natural & Fluent** — Translation as writing, not word-for-word conversion. The output should read as if originally written in the target language.

**Domain Adaptable** — Custom glossaries and translation samples tailored to your industry, team, or personal preferences. The more you use it, the better it gets.

**Built for Scale** — Multi-agent parallel translation handles massive documents and batch folder translation with consistent style throughout.

---

## Quick Start

**Prerequisites**: [Claude Code](https://docs.anthropic.com/en/docs/claude-code) + subscription plan (Claude Max or similar).

**1. Install the skill**

```bash
# Copy the translate/ directory to your Claude Code skills directory
cp -r translate ~/.claude/skills/
```

**2. Start translating**

```
Translate path/to/document.md into Chinese.
```

Translate an entire folder:

```
Translate all Markdown files under path/to/folder/ into Chinese.
```

Translated files appear in the same directory with a language suffix (e.g., `document_zh.md`).

---

## Notes

- **Markdown and plain text only** — PDFs and other formats need conversion first (try [MinerU](https://github.com/opendatalab/MinerU))
- **High token usage** — multi-agent parallel translation; subscription plan strongly recommended over pay-per-use
- **Code blocks are preserved** as-is (comments can be translated)
- **Source files are never overwritten** — output always has a language suffix

---

## License

[CC BY 4.0](./LICENSE) — free to use, modify, and distribute, including commercially. Just keep attribution.

---

If you find this useful, please ⭐ the repo! This project is actively maintained and updated.
