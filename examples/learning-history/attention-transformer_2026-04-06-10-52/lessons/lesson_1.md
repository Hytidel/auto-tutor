# Lesson 1: 背景与动机——为什么需要 Transformer

**时间**: 2026-04-06-10-52
**主题**: attention-transformer（Attention Is All You Need）
**目标认知层级**: 理解（布卢姆 L2）

---

## 学习目标

本节课结束后，你应该能够：
- 解释 RNN/LSTM 在序列建模中的核心局限性
- 描述注意力机制在 Transformer 出现之前的角色
- 用自己的话说明 Transformer 的核心创新是什么

---

## 讲解内容

### 1. 序列建模的"老方法"：RNN 家族

在 Transformer 出现之前，处理语言翻译、文本生成等"序列到序列"任务的主流方法是**循环神经网络（RNN）**，尤其是它的两个变体：**LSTM**（长短期记忆网络）和 **GRU**（门控循环单元）。

> **资料原文**：
> "Recurrent neural networks, long short-term memory [13] and gated recurrent [7] neural networks in particular, have been firmly established as state of the art approaches in sequence modeling and transduction problems such as language modeling and machine translation."
> [来源：1 Introduction]

**RNN 的工作方式**：想象你在逐字阅读一句话，每读一个词，你都要把"之前读过的所有内容的记忆"和"当前这个词"合并，生成新的记忆状态。RNN 就是这样工作的——它按位置一步一步地处理序列，每一步的输出 $h_t$ 依赖于上一步的隐藏状态 $h_{t-1}$。

> **资料原文**：
> "Recurrent models typically factor computation along the symbol positions of the input and output sequences. Aligning the positions to steps in computation time, they generate a sequence of hidden states $h_t$, as a function of the previous hidden state $h_{t-1}$ and the input for position $t$."
> [来源：1 Introduction]

---

### 2. RNN 的致命弱点：无法并行

这种"一步一步"的计算方式带来了一个严重问题：**无法并行化**。

你必须先算完第 1 步，才能算第 2 步；算完第 2 步，才能算第 3 步……这就像流水线上只有一个工人，无论你有多少台机器，都只能排队等待。

> **资料原文**：
> "This inherently sequential nature precludes parallelization within training examples, which becomes critical at longer sequence lengths, as memory constraints limit batching across examples."
> [来源：1 Introduction]

**为什么这是大问题？** 现代 GPU 的强大之处在于可以同时执行数千个并行计算。RNN 的顺序依赖让 GPU 的并行能力大打折扣，导致训练速度极慢，尤其是处理长句子时。

---

### 3. 注意力机制：好帮手，但还不够

注意力机制（Attention Mechanism）在 Transformer 之前就已经存在，它被用来解决 RNN 的另一个问题：**长距离依赖**。

比如翻译"The animal didn't cross the street because **it** was too tired"，"it"指代的是"animal"还是"street"？这需要模型在处理"it"时，能"回头看"很远之前的词。RNN 在这方面表现不佳，因为信息在传递过程中会逐渐衰减。

注意力机制允许模型在处理每个词时，直接"关注"输入序列中任意位置的词，不受距离限制。

> **资料原文**：
> "Attention mechanisms have become an integral part of compelling sequence modeling and transduction models in various tasks, allowing modeling of dependencies without regard to their distance in the input or output sequences."
> [来源：1 Introduction]

**但关键问题是**：在 Transformer 之前，注意力机制几乎总是作为 RNN 的"附件"使用，而不是独立存在。

> **资料原文**：
> "In all but a few cases [27], however, such attention mechanisms are used in conjunction with a recurrent network."
> [来源：1 Introduction]

---

### 4. Transformer 的核心创新：完全抛弃 RNN

这篇论文的核心贡献是：**提出了一个完全基于注意力机制的架构，彻底去掉了 RNN 和卷积**。

> **资料原文**：
> "In this work we propose the Transformer, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism to draw global dependencies between input and output."
> [来源：1 Introduction]

这带来了两个直接好处：
1. **可并行化**：没有了顺序依赖，所有位置可以同时计算
2. **训练更快**：论文中提到，仅用 8 块 P100 GPU 训练 12 小时，就达到了当时最先进的翻译质量

> **资料原文**：
> "The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being trained for as little as twelve hours on eight P100 GPUs."
> [来源：1 Introduction]

---

### 5. 背景中的其他尝试（了解即可）

在 Transformer 之前，也有人尝试用卷积神经网络（CNN）来替代 RNN，比如 ByteNet 和 ConvS2S。CNN 可以并行，但它有一个问题：要让两个距离很远的词"互相看到对方"，需要堆叠很多层卷积，路径很长。

> **资料原文**：
> "In these models, the number of operations required to relate signals from two arbitrary input or output positions grows in the distance between positions, linearly for ConvS2S and logarithmically for ByteNet."
> [来源：2 Background]

Transformer 用注意力机制把这个路径缩短到了常数级别（O(1)），这是它相比 CNN 方案的优势。[来源：2 Background]

---

### ⚡ 反事实论证（Counterfactual Reasoning）

**核心结论**：Transformer 抛弃 RNN 是因为 RNN 无法并行化。

**反事实假设**：如果 RNN 可以完全并行化，Transformer 还有存在的必要吗？

- 如果 RNN 能并行，训练速度的劣势消失，但**长距离依赖**问题仍然存在（信息在长链中衰减）
- 注意力机制的"全局视野"（任意两个位置直接交互）仍然是 RNN 无法复制的特性
- 因此，即使 RNN 能并行，Transformer 的注意力机制在建模能力上仍有优势

**边缘案例**：对于极短的序列（如 2-3 个词），RNN 的顺序依赖问题几乎不存在，Transformer 的优势会大幅缩小。这也解释了为什么 Transformer 在长文本任务上优势更明显。

---

## 课后习题

> 请在每道题的"我的答案"区域填写答案，保存文件后在对话窗口告诉我"已完成"。

### 习题 1：用自己的话解释

RNN 为什么"天生"无法并行化？请用一个生活中的类比来解释这个问题。

[来源：1 Introduction]

**我的答案**：

---

### 习题 2：概念辨析

在 Transformer 出现之前，注意力机制是如何被使用的？它解决了什么问题，又有什么局限？

[来源：1 Introduction]

**我的答案**：

---

### 习题 3：推理题

论文摘要中提到，Transformer 在 WMT 2014 英德翻译任务上取得了 28.4 BLEU 分，仅用了 3.5 天训练。而之前最好的模型（如 GNMT + RL Ensemble）训练成本是 $1.8 \times 10^{20}$ FLOPs，Transformer (big) 只用了 $2.3 \times 10^{19}$ FLOPs。

根据本节学到的内容，**从架构设计角度**解释：为什么 Transformer 能用更少的计算量达到更好的效果？

[来源：Abstract, 1 Introduction, 2 Background]

**我的答案**：

---

## Reflection

完成本节后，请回答：

1. **认知难度** (1-5)：[ ] 1-太简单 [ ] 2-刚好 [ ] 3-有点难 [ ] 4-很困难 [ ] 5-完全不懂
2. **哪些部分还需要澄清？**：

---

## 本节要点总结

- RNN 按位置顺序计算，$h_t$ 依赖 $h_{t-1}$，导致无法并行，训练慢
- 注意力机制在 Transformer 前已存在，但只是 RNN 的"附件"，用于解决长距离依赖
- Transformer 的核心创新：**完全抛弃 RNN，仅用注意力机制**，实现并行化 + 全局依赖建模
- 相比 CNN 方案（ByteNet/ConvS2S），Transformer 将任意两位置的交互路径缩短至 O(1)

---

## 下一课预告

**Lesson 2：注意力机制核心——Scaled Dot-Product Attention & Multi-Head Attention**

我们将深入 Transformer 的"心脏"：注意力函数的数学形式是什么？为什么要"缩放"？Multi-Head 的意义是什么？
