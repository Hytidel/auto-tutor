# auto-tutor — 能规划、能诊断、能动态调整的 AI 私人导师

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/Hytidel/auto-tutor.svg)](https://github.com/Hytidel/auto-tutor/stargazers)


[English](./README.md) | 中文

## 项目概述

### 简介

`auto-tutor` —— 一个能规划、能诊断、能动态调整的 AI 私人导师。



如果你是：
* 喜欢自学、钻研东西的人
* 希望借助 AI 提高学习效率的人
* 希望深度学习某些材料，并且希望一边看一边能跟 AI 导师讨论的人

那 `auto-tutor` 会给你带来全新的学习体验。



你要学的东西可能有各种类型的，比如人文社科的书籍、理科的教材、工科的论文、GitHub 开源项目……

不管你要学什么，
* 你把要学的东西丢给它，它为你规划学习路线、生成个性化的讲义。
* 你学习讲义中的内容并完成习题，它为你批改并诊断学习情况。
* 你觉得太慢/太快/太简单/太难了，它根据你的反馈自适应地调整接下来的学习计划。

这哪是什么聊天机器人，这简直就是请了一位无所不知且有无限耐心的私人导师回家。



此外还有一个很重要的应用场景 —— 「把学习材料"读活"」。
* 当我们对某个领域有了一定的基础之后，再去阅读领域内的书，可能会阅读到一些重复的部分。比如说我们刚学完概率论，然后去看随机过程，而随机过程第一章又是概率论基础，这样重复了。而我又担心第一章错过了一些东西，这个时候就可以用 `auto-tutor` —— 先用几道习题检验一下你是否已完全掌握第一章的内容，如果已完全掌握则直接跳过，否则缺啥补啥。
* 有时候我们阅读一本书并非是打算从头看到尾，而是打算筛选并阅读其中我们感兴趣的部分。这个时候就可以用 `auto-tutor` 实现"跳读"，同时又不错过跳过的部分中对我们感兴趣的部分有用的信息。



项目已开源，欢迎 Star ⭐ / PR。

后续还会加入新功能，敬请期待。

### 灵感来源

这个项目的灵感来源于 dontbesilent 讲的「交互式学习」。

我结合他的视频的评论区反馈和我的使用体会做了一些补充：
* 适配多种学习材料格式。
* 加入了反事实论证等尽量减少 AI 幻觉的提示词。
* 支持传入的学习材料与教学使用不同的语言，并加入了可自定义的术语表，提高学科专业名词翻译的准确度。
* 加入了学习的 roadmap，防止用户在学习过程中"钻牛角尖"，关注了与本次的学习目标弱相关或无关的内容而将学习路线带偏。
* 加入了自动笔记功能，在学习过程中 AI 会自动记录要点、重点、用户掌握不佳的点。

---

## 📦 安装

### 1. 克隆仓库

```bash
git clone https://github.com/Hytidel/auto-tutor.git
cd auto-tutor
```

### 2. 配置 API Key

将 `./settings/.env.example` 复制一份至 `./settings/.env`，并填入你的 `MINERU_API_KEY`：

```bash
cp settings/.env.example settings/.env
```

然后编辑 `settings/.env`：

```env
MINERU_API_KEY=your_api_key
```

MinerU API Key 获取方式：[https://mineru.net/apiManage/token](https://mineru.net/apiManage/token)

> `MINERU_API_KEY` 仅在使用 `everything-to-markdown` skill 转换 PDF、Word、PPT 等格式时需要。如果你的学习材料已经是 Markdown 或源码格式，可以跳过此步骤。

---

## 🚀 快速开始

将要学习的材料放在 `./tmp/` 下（或该项目的其他文件夹下，确保 Claude Code 可访问即可）。

在 Claude Code 中调用 `learning-engine` skill：

```
/learning-engine

学习 `/path/to/your/learning/material`
```

支持的学习材料类型：

| 类型 | 示例 |
|------|------|
| Markdown 文件 | `./tmp/my-notes.md` |
| PDF 文档 | `./tmp/textbook.pdf` |
| Word / PPT | `./tmp/slides.pptx` |
| 图片 | `./tmp/handwritten-notes.jpg` |
| 源码文件 | `./tmp/main.py` |
| 本地项目目录 | `./tmp/my-project/` |
| GitHub 链接 | `https://github.com/user/repo` |

---

## ⚙️ 个性化配置

编辑 `./settings/background.md`，填入你的背景信息，AI 会据此调整讲解深度、用词和习题难度：

```markdown
## 正在读的年级
大学二年级

## 正在学习的科目、知识等
概率论与数理统计

## 目前遇到的问题
对条件期望的理解不够直观
```

---

## 🛠️ 其他 Skills

### `everything-to-markdown`

将其他格式的文件转化为 Markdown 格式（需要配置 MinerU API Key）。

```
/everything-to-markdown

转换 `./tmp/my-document.pdf`
```

### `glossary-collector`

从学习资料中提取学科专业词汇，生成中英文术语对照表，保存至 `./settings/glossary.md`。在跨语言教学时，AI 会优先使用术语表中的译法。

```
/glossary-collector

从 `./tmp/my-paper.pdf` 中提取术语
```

---

## 📁 目录结构

```
auto-tutor/
├── .claude/skills/              # Claude Code skills
│   ├── learning-engine/         # 学习引擎（主 skill）
│   ├── everything-to-markdown/  # 文档格式转换
│   └── glossary-collector/      # 术语表提取
├── settings/                    # 用户配置
│   ├── .env                     # API Keys（不提交到 git）
│   ├── .env.example             # API Keys 模板
│   ├── background.md            # 用户背景信息
│   └── glossary.md              # 术语表
├── learning-history/            # 学习记录（自动生成）
│   └── {topic}_{timestamp}/
│       ├── summary.md           # 学习摘要
│       ├── roadmap_status.md    # 学习路线图状态
│       └── lessons/
│           └── lesson_N.md      # 第 N 课内容
├── examples/learning-history/   # 示例学习记录
└── tmp/                         # 临时文件 / 学习材料存放处
```

---

## 🤝 贡献指南

欢迎贡献！

1. Fork 本仓库
2. 创建分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 开源协议

本项目采用 MIT 协议。
