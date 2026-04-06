---
name: everything-to-markdown
description: 将 PDF、图片（png/jpg/jpeg/jp2/webp/gif/bmp）、Doc、Docx、Ppt、PPTx、网页转换为 Markdown 格式。当用户说"转 markdown"、"转换为 markdown"、"解析文件"、"提取文本"时使用。
---

# Everything to Markdown

使用 MinerU API 将各种文档格式转换为 Markdown。

## 支持的文件类型

- **PDF** 文档
- **图片**: png, jpg, jpeg, jp2, webp, gif, bmp
- **Office 文档**: doc, docx, ppt, pptx
- **网页**: HTML URL

## 使用方法

调用脚本处理文件：

```bash
python scripts/convert_to_markdown.py <file_path_or_url>
```

## 工作流程

1. 从项目 settings 目录的 `.env` 文件读取 `MINERU_API_KEY`
2. 若 API Key 无效，报错并停止
3. 根据输入类型调用 MinerU API：
   - 本地文件 → 批量上传 API → PUT 上传 → 轮询结果
   - URL → 直接提交解析任务 → 轮询结果
4. 下载结果并解压到 `./tmp/{filename}/` 目录

## API Key 配置

API Key 从项目 settings 目录的 `.env` 文件中读取：

```env
MINERU_API_KEY=your-api-key
```

申请地址：https://mineru.net

## 输出结构

```
tmp/
└── {filename}_{timestamp}/
    ├── full.md          # Markdown 解析结果
    ├── images/          # 提取的图片
    ├── layout.json      # 布局信息
    └── ...              # 其他中间文件
```

## API 文档

详细的 MinerU API 文档请参考 [references/mineru-api.md](references/mineru-api.md)，包含：

- 创建解析任务接口
- 获取任务结果接口
- 请求/响应参数说明
- 常见错误码
