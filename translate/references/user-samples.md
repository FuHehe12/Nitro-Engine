# 典型翻译样本

> 展示用户偏好的翻译风格，供子 Agent 作为"基调锚点"。
> 每条样本包含原文片段、译文片段和说明（可选）。
>
> **此文件不会被清理**——随使用逐步积累，翻译时自动加载。

---

## 样本 1：技术文档

**原文**：
> When you deploy a model to production, it is important to note that latency can vary significantly depending on the batch size and the hardware configuration. Users should carefully monitor the inference throughput and adjust parameters accordingly.

**译文**：
> 模型部署到生产环境后，批量大小和硬件配置不同，延迟差异可能很大。要持续关注推理吞吐量，随情况调整参数。

**说明**："it is important to note that"不承载信息，直接删。"vary significantly depending on"拆成因果两截——先说条件再说结果，符合中文先因后果的语序。"Users should carefully"不译为"用户应该仔细"，转成无主语祈使，干脆利落。

---

## 样本 2：博客文章

**原文**：
> I've been playing around with this new framework for about two weeks now, and honestly? It's kind of blown my mind. The developer experience is just *chef's kiss*. But — and this is a big but — the documentation is, well, let's just say it leaves something to be desired.

**译文**：
> 这个新框架我折腾了差不多两周，说实话？有点上头。开发体验堪称绝了。但是——这个"但是"很关键——文档嘛，怎么说呢，只能说还有很大的进步空间。

**说明**：保留作者口语化的节奏感和破折号的戏剧效果。"chef's kiss"不直译而是用"绝了"传递同样的赞叹情绪。"leaves something to be desired"用委婉的中文口语化表达，语气轻松但意思到位。

---

## 样本 3：学术/研究

**原文**：
> Our experiments demonstrate that the proposed method achieves state-of-the-art performance on three benchmark datasets, outperforming the previous best results by 2.3% on average. Notably, the improvement is most pronounced in low-resource scenarios, suggesting that the model's inductive biases are well-suited for data-scarce domains.

**译文**：
> 实验表明，本文方法在三个基准数据集上达到当前最优水平，平均超出已有最佳结果 2.3%。尤其在低资源场景下提升最为显著，说明该模型的归纳偏置对数据稀缺领域具有良好的适配性。

**说明**：学术文体保持严谨克制。"state-of-the-art"译为"当前最优水平"而非"最先进"。"Notably"用"尤其"自然过渡，不必每次都堆"值得注意/关注的是"——中文学术写作更多靠语序衔接而非标记词。"suggesting"译为"说明"而非"表明"，对应 suggest 弱于 demonstrate 的语气差。

---

## 样本 4：产品/README

**原文**：
> Get started in under 5 minutes. No configuration required. Just install, import, and start building amazing things.

**译文**：
> 5 分钟就能上手，不需要任何配置。装好依赖、引入模块，直接开始写你想要的东西。

**说明**：英文产品文案常用极短碎片句，但中文里这种节奏反而显得生硬。译文保留简洁感的同时让句子有完整的骨架，读起来像正常人在跟你说话。"amazing things"原文本身就是泛指，译为"你想要的东西"比直接砍掉更自然，也保留了原文鼓励动手的语气。
