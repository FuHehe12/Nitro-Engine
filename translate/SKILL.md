---
name: translate
description: "Accurately and fluently translates source text into another language, supporting any language pair. Default target language is Chinese. Use this skill when the user requests translation of Markdown files, batch document translation, or text content translation. Trigger phrases: translate, 翻译, translate markdown, translate document, Chinese translation, batch translate."
allowed-tools: Read, Write, Edit, Task, Glob, Grep, Bash
---

This skill provides guidelines for accurate, fluent translation, with agent-based parallel processing for large files and multi-file batches.

## On Translation

> **Translation is writing across languages** — rendering content expressed in one language into another, minimizing the gap between them.

Good translation goes beyond conveying information accurately. It re-expresses that information in language that is beautiful and natural, capturing the spirit of the original author. When readers encounter the translation, they should feel the piece was written in their language from the start — not carried over from a foreign one. Through parallel processing, this standard is maintained even for long texts and multi-file batches.

**Core anchor**: Translation is writing — not conversion, but re-expression.

---

## Core Principles

> **Imagination brings something into presence; translation gives what has come into presence a voice in another language.**

### The Nature of Translation: Reconstruct → Negotiate → Write

Translation is not word-for-word conversion. It is a three-step process:

**Step 1: Reconstruct — Build the Imaginative Space**

After reading the source text, construct a complete "imaginative space" — you should be able to answer: **who is speaking, to whom, in what setting, and what the entire piece is about**.

The imaginative space has two layers:

**Scene awareness** — different text types correspond to different scenes:

- Fiction → a world of characters, scenes, and emotions that you inhabit
- Technical documentation → an expert explaining to a student, and you are listening in
- Academic paper → a rigorous argument unfolding, and you are tracking the chain of reasoning
- Blog post → a friend talking to you, sharing experience and insight
- Product copy → someone demonstrating the value of something to you

**Content overview** — trace the full text's core arc: what the topic is, how the argument or narrative progresses, where the key turns are, and what the piece ultimately conveys. A short text may need only a few sentences; a long one may need a paragraph or more — length is not constrained, but the skeleton and trajectory of the piece must be clear. This overview ensures that translation never loses sight of the forest for the trees — every paragraph's translation should serve the overall direction of the text.

The quality of this imaginative space sets the ceiling for the translation. Great translations share something with novels that move you to tears: when the author puts pen to paper, what lives in their mind is not a pile of textual information but a vivid, complete world. Translation works the same way — you should be able to "see" the scenes the source describes, "hear" the author's voice, and grasp the rhythm and trajectory of the whole piece. When you are truly "present" inside the world of the source, the right expressions in the target language surface naturally, rather than being squeezed out through word-by-word matching.

The output of reconstruction must be crystallized into the "translation tone" field of the translation brief: surface features such as person and register, and deeper features such as emotional register, narrative rhythm, lexical preferences, signature expressions, the movement of thought, and a sketch of the original "voice." These fields serve as the style baseline for all subsequent translation and sub-agent alignment.

**Step 2: Negotiate — Enter into Dialogue with the Source**

Once inside the imaginative space, you are not a passive observer but an interlocutor who can "question the author":

- What is this word actually trying to express in this context?
- What is the closest way for my readers to understand this concept?
- Is the author's tone here serious or ironic?
- Does this metaphor have an equivalent in the target language's world?

This step is the "negotiation" phase of translation — where the translator exercises judgment and brings their own interpretive subjectivity to bear on the source. The glossary fixes unified renderings for key terms; the translation brief captures key challenges and strategies. The more thorough the negotiation, the more fluent the writing that follows.

**Step 3: Write — Compose in the Target Language** (executed by sub-agents)

Writing is the ceiling of translation — when comprehension is sound and negotiation is thorough, all remaining quality differences come down to craft. The primary agent does not execute writing directly in this step; its role is to ensure the translation brief provides sub-agents with a sufficient style baseline. The five dimensions of writing (precision, rhythm, register, naturalness, locale) and their specific requirements are detailed in the "Five Elements of Writing" section of `references/subagent-prompt.md`.

### Strategy Must Be Adaptive

Hard-coded rules cannot cover every scenario. The same "rule" may be exactly inverted across different text types:

- Passive voice: eliminate in technical docs → standard practice in academic papers
- Rhetorical devices: avoid in technical docs → essential in literary works
- Domestication vs. foreignization: user manuals favor domestication → cultural texts may call for strategic foreignization
- Cognitive load: minimize aggressively in technical docs → literary works may legitimately challenge the reader
- Linguistic economy: pursue maximum concision in technical docs → prose may require elaboration and texture
- Regional vocabulary: mainland China uses "软件、程序、网络" → Taiwan uses "軟體、程式、網路" → Hong Kong is more heavily influenced by Cantonese

Accordingly, writing craft (precision, rhythm, register, naturalness), translation techniques (domestication/foreignization, cognitive load management, long-sentence restructuring), and locale positioning (the target region's lexical system and expressive conventions) are not treated as fixed rules. They are **strategic dimensions** that are adaptively determined during the preparation step based on the characteristics of the source text and the target audience. The preparation step produces two temporary files: a **glossary** (`_glossary.md`) to standardize renderings of core terms, and a **translation brief** (`_translation_brief.md`) to capture text type, translation tone, target locale, key challenges, and targeted strategies.

---

## Translation Workflow

### Path Conventions

> `SKILL_DIR` = the directory containing this skill (the path following "Base directory for this skill:" in the system prompt).

| Type | Location | Notes |
|------|----------|-------|
| Skill resources (read-only) | `{SKILL_DIR}/references/` | User-persisted files that accumulate over time |
| Temporary files | Same directory as source file | `_glossary.md`, `_translation_brief.md`, `_tone_sample.md` |
| Split segments | `{source_dir}/_parts/{source_stem}/` | Each source file gets its own subdirectory to avoid naming conflicts |
| Output file | Same directory as source file | `{filename}_zh.md` |

All files follow the same flow: split → translate → merge. Scale logic is handled by the scripts; the AI makes no branching decisions.

---

### Step 1: Preparation

> **The foundation of translation quality.** The full text must be understood before any translation begins.

1. **Input analysis**:
   - This skill handles **Markdown and plain text**; other formats must be converted to Markdown first
   - Source language is detected automatically; default target language is Chinese (zh-CN); the user may specify a different target language or locale
   - Report the translation plan to the user (file count, total line count, target language) and wait for confirmation

2. **Read through the full text**: Understand the topic, argument structure, and writing style to form a holistic impression

3. **Load user-persisted files** (paths relative to `SKILL_DIR`; must be loaded using the Read tool):
   - `{SKILL_DIR}/references/user-glossary.md` — the user's accumulated domain glossary
   - `{SKILL_DIR}/references/user-samples.md` — the user's preferred translation style samples
   - Load each file if it exists; skip without error if it does not (these files accumulate gradually over time)

4. **Extract the glossary** (write to temporary `_glossary.md`):
   - Ground primarily in your read-through understanding, with `user-glossary.md` as a supplementary reference
   - From `user-glossary.md`, **import only entries relevant to the current document's domain**; ignore unrelated domain terminology
   - Extract new terms from the current document and merge with the filtered user-accumulated entries
   - Three sections: terms to preserve as-is, standardized renderings, polysemous term handling
   > Once `_glossary.md` is generated, the user may pause at this point to review and revise the glossary — adjusting entries, adding terms, or removing entries that do not apply. All subsequent translation will use the final version as the baseline. If the user makes no adjustments, proceed directly.

5. **Generate the translation brief** (following the template at `{SKILL_DIR}/references/translation-brief-template.md`; write to temporary `_translation_brief.md`):
   - **Text type**: Technical documentation / Academic paper / Blog / Tutorial / Product copy / Other
   - **Translation tone**: Surface features (person, formality, tense preference) + deep features (emotional register, narrative rhythm, rhetorical density, author-reader relationship, lexical preferences, signature expressions, the movement of thought, a sketch of the original "voice")
   - **Language pair**: Source language (auto-detected) → target language (default: Chinese)
   - **Target locale**: Determine the locale (default: zh-CN), which governs lexical choices, terminology, and expressive conventions. Regional differences are documented in `references/locale-styles.md`
   - **Reader profile**: Who the translation is for, which affects vocabulary and depth of expression
   - **Key translation challenges**: Difficulties specific to this text
   - **Targeted strategies**: Concrete approaches for the challenges identified above
   - **Cross-file consistency** (multi-file scenarios): Shared glossary, shared brief, cross-file linkage

> ⚠️ **Steps 3–5 must be executed regardless of file size.** For small files, the output can be brief — but it cannot be skipped. The purpose of the temporary files is to make translation decisions auditable and to give sub-agents an inheritable style baseline. `_glossary.md` and `_translation_brief.md` are created in the **source file's directory**.

6. **Split the file**:
   ```bash
   python {SKILL_DIR}/scripts/split_md.py {source_file} --force --max-lines 600 --max-size 20000 --output-dir {source_dir}/_parts/{source_stem}/
   ```
   `--force` ensures a manifest is produced even for small files (single-segment output). Each source file's segments go into their own subdirectory to avoid naming conflicts during multi-file splits. The script automatically generates: `_part_NN.md` (segments), `_part_NN_context.json` (bridging context containing the last 5 lines of the preceding segment as `preceding_lines` and the first 3 lines of the following segment as `following_lines`), and `_split_manifest.json` (the manifest).

### Step 2: Translation

> ⚠️ Except for tone anchoring, **all segments are translated by sub-agents**. The primary agent does not directly translate. The primary agent's responsibilities are preparation, dispatch, and verification.

1. **Tone anchoring**: Select a content-rich, stylistically representative passage from the source (300–500 lines); the primary agent translates it against the glossary and translation brief, producing a tone sample written to `_tone_sample.md`, which is passed to all sub-agents alongside `user-samples.md` as a style anchor

2. **Dispatch sub-agents**: Dispatch a sub-agent for each segment using the template in `references/subagent-prompt.md`
   - `subagent_type`: "general-purpose"
   - `model`: "sonnet" (quality-first)
   - Multiple sub-agents launched in parallel
   - Each sub-agent receives: source segment, glossary, translation brief, bridging context, translation samples, tone sample
   - **Output requirements**: Output must go to the designated `{part}_zh.md` file; generating merged files (e.g., `_part_47-50_zh.md`) is not permitted; translating beyond the assigned source range is not permitted
   - **Multi-file parallel strategy**: Use TaskCreate/TaskList to track translation progress for each file/segment

3. **Health check** (executed after all sub-agents complete): Confirm that all segments have a corresponding `_zh.md` file; if any segment is missing, proceed to error recovery

**Error recovery** (with failure criteria):

A sub-agent is considered to have failed if any of the following conditions is met:
1. The output file does not exist
2. The output line count is less than 30% of the source line count
3. The output filename does not match expectations (e.g., a merged file was generated instead of individual segment files)

Handling procedure:
- Sub-agent failure or missing segment → retry once with sonnet
- **Still failing → compile all failed segments, report the failure reasons and a list of affected segments to the user, and let the user decide how to proceed**
- The primary agent must not take over translation unless explicitly requested by the user

### Step 3: Merge

1. **Pre-merge verification**:
   - **Filename check**: Confirm there are no unexpected merged files (e.g., `_part_47-50_zh.md`)
   - **Scope check**: Spot-check several segments to confirm none extends beyond the source range
   - Problems found → compile a list and report to the user; execute corrections or re-translation after user confirmation

2. **Execute merge**:
   ```bash
   python {SKILL_DIR}/scripts/merge_md.py --manifest {source_dir}/_parts/{source_stem}/_split_manifest.json --output {source_dir}/{filename}_zh.md
   ```
   The merge script automatically checks heading hierarchy continuity, code block closure, and link integrity, and will report any issues found in the output.

3. **Post-merge review**:
   - Multi-segment: quickly inspect segment boundaries (5 lines on each side) to ensure contextual continuity
   - Multiple files: run a cross-file terminology consistency scan

4. **Cleanup**:
   - Confirm the output file (`{filename}_zh.md`; the source file is never overwritten)
   - Clean up temporary files:
     ```bash
     rm -f {source_dir}/_glossary.md {source_dir}/_translation_brief.md {source_dir}/_tone_sample.md
     rm -rf {source_dir}/_parts/
     ```
   - Ask the user whether they want to: sync terms to `references/user-glossary.md` / record style samples to `references/user-samples.md`

---

## Important Notes

- **Never overwrite the source file**: Output files receive a language suffix (default: `_zh`).
- **Do not translate code blocks**: This includes both inline code and fenced code blocks; comments within code may be translated.
- **Preserve original formatting**: Heading hierarchy, list indentation, table alignment, and blank line separation.
- **Link handling**: Translate link text; leave URLs unchanged.
- **YAML frontmatter**: Preserve as-is without translating.
- **Default target locale**: Defaults to Chinese mainland readers (zh-CN); other locales may be specified in the translation brief.
- **Glossary takes precedence**: Renderings specified in the glossary must be followed consistently throughout the entire text.
- **Source language is unrestricted**: Any source language is supported; the detected language is recorded in the translation brief.
