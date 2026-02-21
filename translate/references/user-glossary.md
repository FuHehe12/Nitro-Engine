# User Domain Glossary

> A glossary that accumulates over time through use. Automatically loaded during translation
> and merged with terms extracted from the current document into a temporary `_glossary.md`.
> After translation, the primary Agent will ask whether to write new terms from this session
> back to this file.
>
> **This file is never cleaned up** — it is your persistent asset.

---

## 1. Keep As-Is (Do Not Translate)

> Proper nouns, brand names, technical abbreviations, etc. — used as-is in the target text.

| Term | Description | Example Usage |
|------|-------------|---------------|
| API | Application programming interface | Call the API to fetch data |
| Docker | Container platform | Deploy services using Docker |
| GitHub | Code hosting platform | Code is hosted on GitHub |
| Kubernetes | Container orchestration system | Running on a Kubernetes cluster |
| GraphQL | Query language | Query through the GraphQL interface |
| OAuth | Authorization protocol | Integrate OAuth 2.0 authentication |
| WebSocket | Bidirectional communication protocol | Establish a WebSocket connection |

## 2. Unified Renderings (Consistent Throughout)

> Terms that must be translated but kept consistent across the entire text.

| Source | Rendering (zh-CN) | Avoid | Notes |
|--------|-------------------|-------|-------|
| agent | 智能体 | 代理、代理人 | AI context |
| pipeline | 流水线 | 管道、管线 | CI/CD context |
| token | token | 令牌 | Keep as-is in LLM context |
| fine-tune | 微调 | 精调 | |
| prompt | 提示词 | 提示、指令 | LLM context |
| inference | 推理 | 推断 | Model inference |
| deploy | 部署 | 布署 | |
| benchmark | 基准测试 | 标杆 | |
| latency | 延迟 | 时延、潜伏期 | Performance context |
| throughput | 吞吐量 | 通量 | |
| context window | 上下文窗口 | 语境窗口 | LLM context |
| hallucination | 幻觉 | 臆造 | LLM context |
| embedding | 嵌入 / embedding | 嵌套 | Keep as-is or translate depending on context |
| retrieval | 检索 | 取回 | RAG context |

## 3. Polysemous Terms

> Terms with different renderings depending on context.

| Source | Context | Rendering | Example |
|--------|---------|-----------|---------|
| model | Machine learning | 模型 | Train a model |
| model | Design pattern | 模式 | MVC pattern |
| model | Database | 模型 | Data model |
| state | Program state | 状态 | Application state |
| state | Geography/politics | 州/国家 | US states |
| run | Execute program | 运行 | Run a script |
| run | Experiment | 一轮/一次 | Third run of experiment |
| scale | Verb | 扩展 | Horizontal scaling |
| scale | Noun | 规模 | Large-scale deployment |
| serve | Deploy service | 部署 / 提供服务 | Deploy model to production |
| serve | Networking | 分发 | Serve static files |
