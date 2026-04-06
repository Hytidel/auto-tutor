# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**auto-tutor** is an interactive learning engine that uses AI to guide users through deep knowledge internalization. It combines the Socratic method and Bloom's taxonomy to create personalized, file-driven learning experiences.

The project is built around three core skills:
- **learning-engine**: Main interactive learning orchestrator
- **everything-to-markdown**: Document format conversion (PDF, DOCX, PPTX, images → Markdown)
- **glossary-collector**: Terminology extraction for cross-language learning

## Architecture

### Directory Structure

```
auto-tutor/
├── .claude/skills/              # Claude Code skills (primary)
│   ├── learning-engine/         # Main learning orchestrator
│   ├── everything-to-markdown/  # Document conversion
│   └── glossary-collector/      # Terminology extraction
├── settings/                    # User configuration
│   ├── background.md            # User profile (grade, subjects, problems)
│   └── glossary.md              # Terminology table for cross-language teaching
├── learning-history/            # Active learning sessions
│   └── {topic}_{timestamp}/
│       ├── summary.md           # Session summary & progress
│       ├── roadmap_status.md    # Learning roadmap & milestones
│       └── lessons/
│           ├── lesson_1.md      # Lesson content (file-driven)
│           └── ...
├── examples/learning-history/   # Example learning sessions (reference)
└── tmp/                         # Temporary files
```

### Core Concepts

**File-Driven Learning**: All lesson content, exercises, and answers live in files. Users read lessons from files, write answers in files, and Claude reads files to provide feedback. This prevents hallucination and ensures content consistency.

**Skill Workflow**: The learning-engine skill orchestrates a strict 5-step pipeline:
1. **File Format Preprocessing** — Convert input (PDF, DOCX, GitHub link, etc.) to readable Markdown
2. **Initialization & History Retrieval** — Extract topic, check for prior sessions, let user choose continue/new
3. **Context Recovery** — Load prior progress or initialize new session
4. **File-Based Interactive Learning** — Generate lessons, collect answers from files, provide feedback
5. **Learning Report** — Generate final report with mastery metrics and next steps

**Mandatory Rules** (from learning-engine SKILL.md):
- Serial execution: Steps must run in order; output of each step feeds the next
- Blocking gates: Some steps require explicit user response before proceeding
- No cross-phase bundling: Work cannot span multiple phases
- No speculative execution: Don't pre-generate content for future steps
- Language matching: Respond in the user's input language (Chinese or English)
- File-driven principle: Never show lesson content or exercises in chat; always reference file paths

## Common Commands

### Running the Learning Engine

```bash
# Invoke the learning-engine skill (primary workflow)
/learning-engine

# Provide a learning material (file, directory, or GitHub link)
# The skill will guide you through the 5-step pipeline
```

### Document Conversion

```bash
# Convert PDF, DOCX, PPTX, images to Markdown
/everything-to-markdown

# Requires MINERU_API_KEY in settings/.env
```

### Terminology Extraction

```bash
# Extract domain-specific terminology from learning materials
/glossary-collector

# Generates or appends to settings/glossary.md
```

### Configuration

Edit `settings/background.md` to provide user context:
- Grade level (e.g., university, K12)
- Subjects being studied
- Current problems or learning goals

This context is used to personalize lesson depth, vocabulary, and exercise difficulty.

## Key Implementation Details

### Learning Session Structure

Each learning session creates a directory: `learning-history/{topic}_{YYYY-MM-DD-HH-MM}/`

**summary.md** tracks:
- Core conclusions from each lesson
- Mastered knowledge points
- Unresolved difficulties
- Key notes

**roadmap_status.md** tracks:
- Overall progress percentage
- Knowledge point status (✅ Mastered / 🔄 In Progress / ⏳ To Learn)
- Milestones
- Learning history

**lessons/lesson_N.md** contains:
- Learning objectives (Bloom's level)
- Core explanation (with `> **资料原文**：` citations)
- 2-4 practice exercises
- `**我的答案**：` sections for user answers

### Answer Checking Workflow

When user says "已完成" (completed):
1. Read the lesson file and extract answers from `**我的答案**：` sections
2. Check against correct answers using Socratic method (guide, don't tell)
3. Mastery threshold: ≥80% exercises correct → proceed to next lesson
4. Below 80% → provide targeted explanation, let user retry

### Cross-Language Teaching

If teaching language differs from material language:
1. Read `settings/glossary.md` for terminology table
2. Use glossary terms for all domain-specific nouns (strict adherence)
3. Translate all lesson content to target language
4. Annotate first occurrence of specialized terms: `Derivative（导数）`

### Hallucination Prevention

- All lesson content must cite sources: `[来源：{section_title}]`
- Content not in materials: `[⚠️ 当前资料未涉及此内容]`
- Never invent function names, class names, or file paths
- Counterfactual reasoning mode (optional): Add "what if this were false?" analysis to each conclusion

## Debugging & Troubleshooting

### Common Issues

**"Lesson file not found"** → Check `learning-history/{topic}_{timestamp}/lessons/` directory exists and lesson_N.md is present

**"User answers not detected"** → Verify `**我的答案**：` section exists in lesson file and is filled in

**"API Key invalid"** → Ensure `settings/.env` contains valid `MINERU_API_KEY` for document conversion

**"History not found"** → Topic name extraction may differ; check `learning-history/` for similar folder names

### Debugging Workflow

1. Verify file paths match expected structure
2. Check file encoding (UTF-8 for Chinese content)
3. Read `summary.md` and `roadmap_status.md` to understand session state
4. Confirm user background in `settings/background.md` matches current context
