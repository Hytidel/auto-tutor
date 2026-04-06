---
name: learning-engine
description: >
  交互式学习引擎，采用苏格拉底教学法和布卢姆分类学引导用户深入学习。
  Use when user says "学习引擎", "帮我学习这个文档", invokes /learning-engine,
  or provides a learning material and asks to study it.
---

# Learning Engine（学习引擎）

> 以"文件驱动 + 苏格拉底教学法 + 布卢姆分类学"为核心，引导用户对学习资料实现深度知识内化的交互式学习引擎。

**Core Pipeline**: `文件预处理 → 初始化与历史检索 → 上下文恢复 → 文件驱动交互式学习 → 学习报告`

---

## Mandatory Rules

> [!CAUTION]
> ### Serial Execution & Gate Discipline
>
> **This workflow is a strict serial pipeline. The following rules have the highest priority — violating any one of them constitutes execution failure:**
>
> 1. **SERIAL EXECUTION** — Steps MUST execute in order; output of each step is input for the next. Non-BLOCKING adjacent steps may proceed continuously once prerequisites are met, without waiting for the user to say "continue"
> 2. **BLOCKING = HARD STOP** — ⛔ BLOCKING steps require full stop; agent MUST wait for explicit user response before proceeding and MUST NOT make decisions on behalf of the user
> 3. **NO CROSS-PHASE BUNDLING** — Bundling work across phases is FORBIDDEN
> 4. **GATE BEFORE ENTRY** — Prerequisites (🚧 GATE) MUST be verified before starting each Step
> 5. **NO SPECULATIVE EXECUTION** — Pre-preparing content for future steps is FORBIDDEN

> [!IMPORTANT]
> ### Language & Communication
>
> - Match the language of the user's input. If the user writes in Chinese, respond in Chinese; if in English, respond in English
> - Explicit user override takes precedence
> - Lesson 文件内容使用中文；文件结构关键词（如 `## 学习目标`、`## 课后习题`、`**我的答案**`）保持固定格式，不得更改
>
> **跨语言教学（强制执行）**：
>
> 若用户指定的教学语言与学习材料的语言不同（例如：材料为中文，但要求英文教学），则：
>
> 1. **翻译前置**：在生成 Lesson 内容前，先读取 `${PROJECT_DIR}/settings/glossary.md` 中的术语表
> 2. **术语优先**：翻译时，所有出现在术语表中的专有名词必须严格使用术语表中对应的译法，不得自行翻译
> 3. **全文翻译**：Lesson 文件的所有正文内容（讲解、习题、反馈）均使用目标教学语言输出；文件结构关键词（如 `## 学习目标`、`**我的答案**`）保持固定格式不变
> 4. **术语标注**：首次出现的专有名词，在译文后以括号附注原文，格式：`Derivative（导数）`
> 5. **术语表缺失处理**：若某专有名词未收录于术语表，使用通行译法并在该词后标注 `[⚠️ 术语表未收录]`

> [!IMPORTANT]
> ### Compatibility With Generic Coding Skills
>
> - Do NOT create `.worktrees/`, `tests/`, branch workflows, or other generic engineering structure
> - If generic coding skills conflict with this workflow, follow this skill first unless the user explicitly overrides

> [!IMPORTANT]
> ### 防幻觉（强制执行）
>
> - ❌ 禁止编造数据、虚构事件、臆测因果关系
> - ✅ 讲解中涉及资料内容时，必须使用 `> **资料原文**：` 格式标注原文
> - ✅ 资料未覆盖的知识点，必须明确告知用户"当前资料未涉及此内容"

> [!IMPORTANT]
> ### 用户背景适配（强制执行）
>
> 生成的课程内容必须符合【用户背景】：
> - 用户背景来源：
>   1. `${PROJECT_DIR}/settings/background.md` 中的背景信息
>   2. 用户在调用 skill 时补充的背景信息
> - 优先级：用户补充的背景信息 > `background.md` 中的背景信息
> - 若两者存在冲突，以用户补充为准
> - 适配要求：
>   - 讲解深度、用词、举例应适配用户的年级/知识水平
>   - 习题难度应与用户能力匹配
>   - 若用户背景表明其是教师（如家教），讲解可包含教学策略建议

> [!IMPORTANT]
> ### 文件驱动核心原则（强制执行）
>
> | 禁止行为 | 原因 |
> |---------|------|
> | ❌ 在对话中展示课程讲解内容 | 违反文件驱动原则 |
> | ❌ 在对话中展示课后习题 | 用户应在文件中阅读习题 |
> | ❌ 让用户在对话中发送答案 | 用户应在文件中填写答案 |
> | ❌ 在对话中直接检查答案 | 必须先读取文件中的答案 |
>
> **唯一允许的对话内容**：通知文件位置、提醒填写答案、读取文件后给出反馈、补充讲解。

### Role Dispatch Protocol

This skill operates as a single inline agent — no role switching required.

---

## Resource Manifest

### Templates

| Index | Path | Purpose |
|-------|------|---------|
| Lesson 模板 | `${SKILL_DIR}/templates/lesson-template.md` | 每节课的内容结构模板 |
| 摘要模板 | `${SKILL_DIR}/templates/summary-template.md` | `summary.md` 初始化模板 |
| 路线图模板 | `${SKILL_DIR}/templates/roadmap-template.md` | `roadmap_status.md` 初始化模板 |
| 报告模板 | `${SKILL_DIR}/templates/report-template.md` | 学习报告结构模板 |
| 项目概览模板 | `${SKILL_DIR}/templates/project-overview-template.md` | 开源项目学习资料生成模板 |

### References

| Resource | Path |
|----------|------|
| 布卢姆分类学 | `${SKILL_DIR}/references/bloom-taxonomy.md` |
| 苏格拉底教学法 | `${SKILL_DIR}/references/socratic-method.md` |

### User Context

| Resource | Path | Purpose |
|----------|------|---------|
| 用户背景 | `${PROJECT_DIR}/settings/background.md` | 学习者的年级、科目、问题等背景信息 |

---

## Workflow

### Step 1: 文件格式预处理 (File Format Preprocessing)

🚧 **GATE**: 用户已提供学习资料——文件路径、目录路径、GitHub 链接或内容。

🛠️ **EXECUTION**:

1. **输入类型判断**：

| 输入形式 | 判断条件 | 处理方式 |
|---------|---------|---------|
| GitHub 链接 | 以 `https://github.com/` 开头 | 执行第 2 步（项目获取） |
| 本地目录路径 | 路径指向一个目录 | 执行第 2 步（项目获取） |
| 单个文件 | 路径指向一个文件 | 执行第 3 步（格式检测） |
| 不可读文件类型 | 见下方不可读类型列表 | 执行第 6 步（报错终止） |

**不可读文件类型**（报错终止）：`.exe` / `.dll` / `.so` / `.bin` / `.dat` / `.zip` / `.tar` / `.gz` 等二进制或压缩格式。

2. **开源项目获取与学习资料生成**：

   **若为 GitHub 链接**：
   ```bash
   git clone {github_url} ${PROJECT_DIR}/tmp/{repo_name}/
   ```
   - 失败则重试，最多 3 次；超过 3 次提示用户检查链接或网络

   **若为本地目录路径**：
   ```bash
   cp -r {local_path} ${PROJECT_DIR}/tmp/{project_name}/
   ```

   **项目读取与学习资料生成**：
   - 读取项目根目录下的 `README.md`（若存在）作为概览
   - 扫描项目文件树，识别主要模块与入口文件
   - 读取 `${SKILL_DIR}/templates/project-overview-template.md`
   - 启动 subagent（`general-purpose` 类型），按模板生成结构化学习资料：
     ```
     请分析以下开源项目，严格按照提供的模板生成学习概览文件。

     项目路径：{project_path}
     输出文件：${PROJECT_DIR}/tmp/converted/{project_name}_overview.md
     模板路径：${SKILL_DIR}/templates/project-overview-template.md

     生成要求：
     1. 按模板的 8 个章节逐一填写，不得省略任何章节
     2. 所有内容必须有来源依据（README、代码文件、注释）；无法确认来源的内容标注 [⚠️ 当前资料未涉及此内容]
     3. 第 3 节"项目结构"：用 tree 格式展示两级目录，超过 20 个条目时折叠次要目录
     4. 第 4 节"核心模块"：每个模块必须标注入口文件的实际路径
     5. 第 5 节"数据流"：必须追踪至少一条从入口到输出的完整调用链
     6. 第 7 节"推荐学习路径"：按模块依赖关系排序，每条对应后续一个 Lesson 的学习单元
     7. 不得编造函数名、类名、文件路径——所有符号必须在项目中实际存在
     ```
   - 轮询检查 subagent 状态（poll_interval = 10s，最大等待 300s）
   - 失败则重试，最多 3 次；超过 3 次提示用户手动提供学习资料
   - 将生成的 `_overview.md` 作为后续步骤的 `processed_path`，跳至第 5 步

3. **格式检测**：判断文件后缀：

| 类型 | 文件格式 | 处理方式 |
|------|---------|---------|
| 直接可读（无需转换） | `.md` 及各类源码（`.c` `.cpp` `.py` `.java` `.js` `.ts` `.go` `.rs` `.rb` `.swift` `.kt` 等） | 跳至第 4 步 |
| 需转换为 Markdown | `.pdf` `.docx` `.pptx` `.png` `.jpg` `.html` 等 | 执行第 4 步前先执行转换 |

> ⚠️ `.html` 默认需要转换，除非用户明确表示学习目标是"学习如何书写 HTML"。

4. **非直接可读文件转换**：
   - 启动 subagent（`general-purpose` 类型），调用 `everything-to-markdown` skill 进行格式转换
   - 输出目录：`${PROJECT_DIR}/tmp/converted/`
   - 使用以下 prompt 模板：
     ```
     请调用 everything-to-markdown skill，将以下文件转换为 Markdown 格式：
     - 输入文件：{file_path}
     - 输出目录：./tmp/converted/
     转换完成后，返回输出文件的完整路径。
     ```
   - 轮询检查 subagent 状态（poll_interval = 10s，最大等待 300s）
   - 失败则重试，最多 3 次；超过 3 次提示用户手动转换

5. **Markdown 质量检测与优化**：
   - 读取文件前 500 行，检测：标题层级错乱、OCR 噪声、格式不规范
   - 若存在问题：启动 subagent 调用 `markdown-refiner` skill，**按章节分段传递**（不传整个文件）
   - 使用以下 prompt 模板：
     ```
     请调用 markdown-refiner skill，优化以下 Markdown 文本片段。
     这是学习资料的一个章节，请修复标题层级、OCR 错误和格式问题。
     【待优化内容】
     {chapter_content}
     仅输出优化后的 Markdown 文本，不要添加解释说明。
     ```
   - 轮询与重试机制同上

6. **不可读文件类型报错（终止）**：
   ```
   ❌ 无法处理该文件类型：{file_extension}
   当前支持的格式：Markdown、源码文件、PDF、Word、PPT、图片、HTML，以及 GitHub 链接或本地项目目录。
   请提供可读的学习资料后重新调用。
   ```
   终止 workflow，不进入 Step 2。

7. **记录文件状态**：
   - `original_path`：原始文件路径或链接
   - `processed_path`：处理后文件路径
   - `processing_status`：`original` | `cloned` | `converted` | `refined`

✅ **CHECKPOINT**:
```markdown
## ✅ Step 1 Complete
- [x] 输入类型判断完成：<输入类型>
- [x] 文件已就绪（路径：<processed_path>，状态：<processing_status>）
- [ ] **Next**: auto-proceed to Step 2
```

---

### Step 2: 初始化与历史检索 (Initialization & History Retrieval)

🚧 **GATE**: Step 1 complete；`processed_path` 已确认，文件可读。

🛠️ **EXECUTION**:

1. **主题提取**：根据资料内容自动提炼简洁的 `topic_name`（如 `quantum-physics`、`python-async`）
2. **获取时间戳**：记录 `timestamp`（格式：`YYYY-MM-DD-HH-MM`）
3. **扫描历史**：检索 `${PROJECT_DIR}/learning-history/` 下所有子目录
4. **智能筛选**：根据文件夹名（格式 `${topic_name}_${timestamp}`）筛选相关历史
5. **深度核实**：读取相关目录下的 `summary.md`，确认学习进度与目标一致性
6. **构建选项列表**：
   - 每条历史记录：`[文件夹名] - 上次学习到：[summary.md 中的进度摘要]`
   - 末尾追加：`开启全新学习`

⛔ **BLOCKING**: 调用 `ask_user_question`，展示所有历史选项，等待用户选择"继续历史"或"开启全新学习"。

✅ **CHECKPOINT**:
```markdown
## ✅ Step 2 Complete
- [x] topic_name 已提取：<topic_name>
- [x] timestamp 已记录：<timestamp>
- [x] 历史选项已展示，用户已选择：<选择结果>
- [ ] **Next**: auto-proceed to Step 3
```

---

### Step 3: 上下文恢复 (Context Recovery)（Conditional）

🚧 **GATE**: Step 2 complete；用户已做出选择。

> **Trigger condition**: 用户选择了继续某条历史记录。若用户选择"开启全新学习"，则创建新目录并初始化文件后，跳至 Step 4。

🛠️ **EXECUTION**:

**若用户选择全新学习**：
1. 创建目录 `${PROJECT_DIR}/learning-history/${topic_name}_${timestamp}/lessons/`
2. 读取 `${SKILL_DIR}/templates/summary-template.md`，初始化 `summary.md`
3. 读取 `${SKILL_DIR}/templates/roadmap-template.md`，初始化 `roadmap_status.md`
4. 跳至 Step 4

**若用户选择继续历史**：
1. 读取 `summary.md`：获取核心结论、已掌握知识点、待攻克难点
2. 读取 `roadmap_status.md`：确定当前认知坐标（当前 lesson index）
3. 检查当前 lesson 文件状态，按下表路由：

| 场景 | lesson 文件状态 | 用户答案状态 | 正确行为 |
|------|----------------|-------------|---------|
| A | 不存在 | — | 跳至 Step 4，生成新 lesson |
| B | 已存在 | "我的答案"区域为空 | ⛔ BLOCKING：通知用户去文件中填写，等待"已完成" |
| C | 已存在 | "我的答案"区域已填写 | 跳至 Step 4，执行答案检查 |

**场景 B 通知模板**：
```
📋 检测到 Lesson {index} 已生成，但尚未完成。

📄 文件位置：`./learning-history/${topic_name}_${timestamp}/lessons/lesson_{index}.md`

请阅读该文件，在"我的答案"区域填写你的答案，保存文件后，在对话窗口告诉我"已完成"。
```

✅ **CHECKPOINT**:
```markdown
## ✅ Step 3 Complete
- [x] 学习目录已就绪：<directory_path>
- [x] summary.md 已加载/初始化
- [x] roadmap_status.md 已加载/初始化
- [x] 当前 lesson 状态已判断：场景 <A/B/C>
- [ ] **Next**: auto-proceed to Step 4
```

---

### Step 4: 文件驱动交互式学习 (File-Based Interactive Learning)

🚧 **GATE**: Step 3 complete；学习目录存在，当前 lesson index 已确定。

⛔ **BLOCKING**: 调用 `ask_user_question`，展示以下单选题，等待用户选择后记录 `counterfactual_mode`（`true` / `false`）：

```
是否开启反事实论证？（减少 AI 幻觉，但消耗更多 token）
- 是
- 否
```

🛠️ **EXECUTION**:

**4.0 反事实论证模式（`counterfactual_mode = true` 时生效）**：

在生成 Lesson、检查习题作答、回答用户问题时，额外执行以下操作：

1. **反事实假设**：每个核心结论后，追加："如果 [该概念的核心要素] 不存在或发生相反变化，会导致什么结果？这与当前现实有何逻辑冲突？"
2. **因果 vs 相关**：明确区分哪些是相关性，哪些是因果性，不得将相关关系误述为因果关系
3. **自我辩论**：每个结论后增加"反事实论证"小节：
   - 假设该结论错误，可能的原因是什么？
   - 有哪些边缘案例不符合该理论？
   - 去掉前提条件后，结论是否依然成立？

**4.1 逆向设计（生成新 Lesson 时执行）**：
1. 读取 `${SKILL_DIR}/references/bloom-taxonomy.md` 和 `${SKILL_DIR}/references/socratic-method.md`
2. 读取用户背景：
   - 读取 `${PROJECT_DIR}/settings/background.md` 获取基础背景
   - 若本次调用时用户补充了背景信息，与文件内容合并；冲突处以用户补充为准
3. 明确本节课目标："本节课结束后，用户应能解决什么具体问题？"
4. 从资料中提取知识点，结合历史记录和用户背景规划路径，确定目标布卢姆层级

**4.2 Lesson 文件生成**：
1. 读取 `${SKILL_DIR}/templates/lesson-template.md`
2. 按模板生成 `${PROJECT_DIR}/learning-history/${topic_name}_${timestamp}/lessons/lesson_{index}.md`，包含：
   - 目标认知层级（布卢姆层级）
   - 学习目标列表
   - 核心讲解（含 `> **资料原文**：` 引用，适配用户背景的深度与用词）
   - 课后习题 2-4 道（难度适配用户能力），每道习题后预留 `**我的答案**：` 区域

**4.2.1 生成后自检（强制执行）**：
Lesson 文件写入完成后，逐条核查讲解内容与习题中的每个细节：

| 情况 | 处理方式 |
|------|---------|
| 细节可在学习资料中找到出处 | 在该句/段末尾标注 `[来源：{章节或段落标题}]` |
| 细节无法在学习资料中找到出处 | 在该句/段末尾标注 `[⚠️ 当前资料未涉及此内容]` |

自检完成后更新文件，**不在对话中展示自检结果**，仅在通知中附加一行自检摘要：
```
🔍 自检完成：{N} 处已标注来源，{M} 处标注"当前资料未涉及"
```

3. 生成后，**不在对话中展示课程内容**，仅发送通知：
   ```
   ✅ Lesson {index} 已生成！

   📄 文件位置：`./learning-history/${topic_name}_${timestamp}/lessons/lesson_{index}.md`

   请阅读该文件，在"我的答案"区域填写你的答案，保存文件后，在对话窗口告诉我"已完成"。
   ```

⛔ **BLOCKING**: 等待用户在对话中说"已完成"、"做完了"、"写完了"等表述。

**4.3 答案检查（用户说"已完成"后执行）**：
1. 读取 `lesson_{index}.md`，提取"我的答案"区域内容
2. 若"我的答案"区域为空 → 提示用户先去文件中填写，重新 BLOCKING
3. 按以下规则给出反馈：
   - 正确 → 给予肯定，询问是否进入下一课
   - 部分正确 → 指出不足，提供补充讲解（可在对话中进行）
   - 错误 → 不直接给答案，提供苏格拉底式提示引导重新思考
4. **掌握判定**：
   - 通过 ≥ 80% 习题 → 视为"掌握"，可进入下一课
   - 未达到 80% → 提供针对性讲解，让用户重新尝试

**4.4 动态支架**：
- 若用户连续两次回答"不知道"或表现困惑 → 自动降低布卢姆等级，从"分析/应用"退回"理解/记忆"，提供类比或脚手架式提示

**4.4.1 主线优先与偏题处理（强制执行）**：

回答用户提问前，先对照 `roadmap_status.md` 中的当前主线任务判断相关性：

| 判断结果 | 处理方式 |
|---------|---------|
| 与主线强相关 | 正常回答，可深入展开 |
| 与主线弱相关或无关 | 执行偏题处理流程（见下） |

**偏题处理流程**：
1. 在 `summary.md` 的 `⏳ 待解决` 区域追加记录：
   ```
   - {用户问题摘要}（待主线任务结束后再解决）
   ```
2. 在对话中回复：
   ```
   这是一个很有趣的问题，但与我们本次的学习目标不强相关。我已经帮你记录下来了，待我们完成主线任务后再回来探索。
   ```
3. 将对话引导回当前主线任务

**4.5 进度更新（每个 Lesson 完成后执行）**：
1. 更新 `summary.md`：新增本次结论与未竟难点
2. 更新 `roadmap_status.md`：更新进度百分比与导航坐标
3. 若话题偏离主线 → 提示："我们正在偏离原定目标，是否将其作为新分支记录，还是回到主线？"
4. 生成下一个 Lesson 文件，重复 4.2 流程

✅ **CHECKPOINT**:
```markdown
## ✅ Step 4 Complete（阶段性）
- [x] Lesson {index} 文件已生成：<file_path>
- [x] 用户答案已检查，掌握度：<百分比>
- [x] summary.md 已更新
- [x] roadmap_status.md 已更新
- [ ] **Next**: 继续下一 Lesson（返回 Step 4）或 用户退出 → auto-proceed to Step 5
```

---

### Step 5: 生成学习报告 (Learning Report)

🚧 **GATE**: 用户明确表示学习完成或阶段性退出；`summary.md` 和 `roadmap_status.md` 已更新至最新状态。

🛠️ **EXECUTION**:

1. 读取 `${SKILL_DIR}/templates/report-template.md`
2. 读取 `summary.md` 和 `roadmap_status.md` 获取完整学习数据
3. 生成报告文件：`${PROJECT_DIR}/learning-history/reports/${topic_name}_${timestamp}/report_${timestamp}.md`，包含：
   - **目标达成度**：初始目标 vs 实际进度的可视化对比
   - **掌握明细表**：Lesson 编号、名称、认知层级评分（1-5 ⭐）、后续建议
   - **能力增长图谱**：描述用户从"不会"到"掌握"的认知迁移路径
   - **进阶规划**：基于 `summary.md` 中的难点，推荐下一个关联学习主题

⛔ **BLOCKING**: 报告生成后，展示报告文件路径，告知用户学习已完成，等待用户反馈。

✅ **CHECKPOINT**:
```markdown
## ✅ Step 5 Complete — Learning Engine run complete
- [x] 学习报告已生成：<report_path>
- [x] 进阶规划已提供
```
