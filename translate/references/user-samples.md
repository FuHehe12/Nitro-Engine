# Translation Samples

> Demonstrates the user's preferred translation style, used as a "tone anchor" by sub-agents.
> Each sample includes a source passage, a translated passage, and optional notes.
>
> **This file is never cleaned up** — it accumulates over time and is automatically loaded
> during translation.

---

## Sample 1: Technical Documentation

**Source**:
> When you deploy a model to production, it is important to note that latency can vary
> significantly depending on the batch size and the hardware configuration. Users should
> carefully monitor the inference throughput and adjust parameters accordingly.

**Translation**:
> 模型上线后，延迟会因批量大小和硬件配置而明显波动。需要持续监控推理吞吐量，及时调整参数。

**Notes**: Dropped filler structures like "it is important to note that" that carry no
information. "Users should" rendered as a direct imperative without subject rather than
"用户应该". The result is concise — each sentence lands its point cleanly.

---

## Sample 2: Blog Post

**Source**:
> I've been playing around with this new framework for about two weeks now, and honestly?
> It's kind of blown my mind. The developer experience is just *chef's kiss*. But — and
> this is a big but — the documentation is, well, let's just say it leaves something to
> be desired.

**Translation**:
> 这个新框架我折腾了差不多两周，说实话？有点上头。开发体验堪称绝了。但是——这个"但是"很关键——文档嘛，怎么说呢，只能说还有很大的进步空间。

**Notes**: Preserved the author's colloquial rhythm and the dramatic effect of the dashes.
"chef's kiss" rendered as "绝了" to convey the same admiration rather than a literal
translation. "leaves something to be desired" rendered with a hedged colloquial Chinese
expression.

---

## Sample 3: Academic / Research

**Source**:
> Our experiments demonstrate that the proposed method achieves state-of-the-art performance
> on three benchmark datasets, outperforming the previous best results by 2.3% on average.
> Notably, the improvement is most pronounced in low-resource scenarios, suggesting that the
> model's inductive biases are well-suited for data-scarce domains.

**Translation**:
> 实验表明，本文方法在三个基准数据集上均达到了最优性能，平均超出此前最佳结果 2.3%。值得关注的是，低资源场景下提升最为显著，这说明该模型的归纳偏置特别适合数据稀缺的领域。

**Notes**: Academic register maintained throughout. "state-of-the-art" rendered as "最优"
rather than "最先进的" (which reads more colloquially). "Notably" rendered as "值得关注的是"
rather than the overused "值得注意的是". Passive constructions retained where appropriate
for academic convention.

---

## Sample 4: Product / README

**Source**:
> Get started in under 5 minutes. No configuration required. Just install, import, and
> start building amazing things.

**Translation**:
> 5 分钟上手，零配置。安装、引入、开始构建。

**Notes**: Product copy demands maximum concision. Three short sentences create rhythm.
"amazing things" dropped — vague modifiers like this feel unprofessional in Chinese
product writing.
