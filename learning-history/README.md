# Learning History 目录

本目录用于存放学习历史记录，追踪学习进度和知识掌握情况。

## 目录结构

```
learning-history/
└── {topic}_{timestamp}/
    ├── summary.md              # 学习摘要
    ├── roadmap_status.md       # 学习路线图状态
    └── lessons/                # 课程目录
        ├── lesson_1.md         # 第 1 课内容
        ├── lesson_2.md         # 第 2 课内容
        └── ...
```

## 说明

- 每个学习主题存放在独立的项目目录中
- 目录名称格式：`{主题}_{时间戳}`，例如 `yiyuan-hanshu-weifen-xue_2026-04-02`

### 文件说明

| 文件 | 说明 |
|------|------|
| `summary.md` | 学习摘要，记录已掌握知识点、待攻克难点、学习进度、关键笔记 |
| `roadmap_status.md` | 学习路线图状态，追踪整体进度、知识点状态、里程碑、学习历史 |
| `lessons/lesson_N.md` | 第 N 课的学习内容，包含学习目标、核心讲解、课后习题 |

### 学习进度追踪

`roadmap_status.md` 中使用以下状态标记：

- `✅ 已掌握` - 知识点已完全掌握
- `🔄 进行中` - 正在学习
- `⏳ 待学习` - 尚未开始
