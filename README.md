# auto-tutor — An AI Personal Tutor That Plans, Diagnoses, and Dynamically Adapts

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/Hytidel/auto-tutor.svg)](https://github.com/Hytidel/auto-tutor/stargazers)


English | [中文](./README_CN.md)

## Project Overview

### Introduction

`auto-tutor` — An AI personal tutor that can plan learning paths, diagnose knowledge gaps, and dynamically adjust to your needs.

If you are:
* Someone who enjoys self-learning and exploring new topics
* Someone who wants to leverage AI to improve learning efficiency
* Someone who wants to deeply study materials while discussing with an AI tutor in real-time

Then `auto-tutor` will give you a brand new learning experience.

The materials you want to learn can be of various types: humanities and social science books, science textbooks, engineering papers, GitHub open-source projects, and more.

No matter what you want to learn:
* You provide the material, and it plans your learning path and generates personalized lessons.
* You study the lessons and complete exercises, and it grades your work and diagnoses your learning progress.
* If you feel the pace is too slow/fast or the difficulty is too easy/hard, it adapts the learning plan based on your feedback.

This isn't just a chatbot—it's like having a knowledgeable and infinitely patient personal tutor at home.

Additionally, there's an important use case — "bringing learning materials to life":
* After building foundational knowledge in a field, when reading domain-specific books, you might encounter repetitive content. For example, after learning probability theory, when studying stochastic processes, the first chapter covers probability basics again. You worry about missing something, but don't want to re-read everything. `auto-tutor` can help: use a few exercises to verify if you've mastered the content, and if so, skip it; otherwise, fill in the gaps.
* Sometimes you don't plan to read a book cover-to-cover, but want to selectively read parts that interest you. `auto-tutor` enables "selective reading" while ensuring you don't miss relevant information in the skipped sections.

The project is open-source. We welcome Stars ⭐ and PRs.

More features coming soon!

### Inspiration

This project was inspired by dontbesilent's concept of "interactive learning."

I've added enhancements based on feedback from his video's comments and my own experience:
* Support for multiple learning material formats.
* Integrated counterfactual reasoning and other techniques to minimize AI hallucinations.
* Support for teaching in a different language than the source material, with a customizable glossary table to improve accuracy of domain-specific term translations.
* Added learning roadmaps to prevent users from getting sidetracked by weakly-related or unrelated content during learning.
* Added automatic note-taking: the AI automatically records key points, important concepts, and areas where you need improvement.

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Hytidel/auto-tutor.git
cd auto-tutor
```

### 2. Configure API Key

Copy `./settings/.env.example` to `./settings/.env` and fill in your `MINERU_API_KEY`:

```bash
cp settings/.env.example settings/.env
```

Then edit `settings/.env`:

```env
MINERU_API_KEY=your_api_key
```

Get your MinerU API Key here: [https://mineru.net/apiManage/token](https://mineru.net/apiManage/token)

> `MINERU_API_KEY` is only needed when using the `everything-to-markdown` skill to convert PDFs, Word documents, PPTs, etc. If your learning materials are already in Markdown or source code format, you can skip this step.

---

## 🚀 Quick Start

Place the material you want to learn in `./tmp/` (or any other folder in this project that Claude Code can access).

Invoke the `learning-engine` skill in Claude Code:

```
/learning-engine

Learn `/path/to/your/learning/material`
```

Supported learning material types:

| Type | Example |
|------|---------|
| Markdown files | `./tmp/my-notes.md` |
| PDF documents | `./tmp/textbook.pdf` |
| Word / PPT | `./tmp/slides.pptx` |
| Images | `./tmp/handwritten-notes.jpg` |
| Source code files | `./tmp/main.py` |
| Local project directories | `./tmp/my-project/` |
| GitHub links | `https://github.com/user/repo` |

---

## ⚙️ Personalization

Edit `./settings/background.md` to provide your background information. The AI will adjust explanation depth, vocabulary, and exercise difficulty accordingly:

```markdown
## Current Grade Level
University Year 2

## Subjects / Topics Being Studied
Probability Theory and Mathematical Statistics

## Current Challenges
Lack of intuitive understanding of conditional expectation
```

---

## 🛠️ Other Skills

### `everything-to-markdown`

Convert files in other formats to Markdown (requires MinerU API Key configuration).

```
/everything-to-markdown

Convert `./tmp/my-document.pdf`
```

### `glossary-collector`

Extract domain-specific terminology from learning materials and generate a bilingual terminology table, saved to `./settings/glossary.md`. During cross-language teaching, the AI will prioritize using translations from the terminology table.

```
/glossary-collector

Extract terminology from `./tmp/my-paper.pdf`
```

---

## 📁 Directory Structure

```
auto-tutor/
├── .claude/skills/              # Claude Code skills
│   ├── learning-engine/         # Learning engine (main skill)
│   ├── everything-to-markdown/  # Document format conversion
│   └── glossary-collector/      # Terminology extraction
├── settings/                    # User configuration
│   ├── .env                     # API Keys (not committed to git)
│   ├── .env.example             # API Keys template
│   ├── background.md            # User background information
│   └── glossary.md              # Terminology table
├── learning-history/            # Learning records (auto-generated)
│   └── {topic}_{timestamp}/
│       ├── summary.md           # Learning summary
│       ├── roadmap_status.md    # Learning roadmap status
│       └── lessons/
│           └── lesson_N.md      # Lesson N content
├── examples/learning-history/   # Example learning records
└── tmp/                         # Temporary files / learning materials storage
```

---

## 🤝 Contributing

Contributions are welcome!

1. Fork this repository
2. Create a branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.
