# MinerU 单个文件解析 API 文档

## 概述

MinerU 精准解析 API 适用于通过 API 创建解析任务的场景，用户须先申请 Token。

**注意事项：**
- 单个文件大小不能超过 200MB，文件页数不超出 600 页
- 每个账号每天享有 2000 页最高优先级解析额度，超过 2000 页的部分优先级降低
- 因网络限制，github、aws 等国外 URL 会请求超时
- 该接口不支持文件直接上传
- header 头中需要包含 Authorization 字段，格式为 Bearer + 空格 + Token

**支持文件类型：**
- PDF 文档
- 图片：png, jpg, jpeg, jp2, webp, gif, bmp
- Office：doc, docx, ppt, pptx
- 网页：html

---

## 创建解析任务

### 接口地址

```
POST https://mineru.net/api/v4/extract/task
```

### 请求示例

**PDF/Doc/PPT/图片文件：**

```python
import requests

token = "官网申请的api token"
url = "https://mineru.net/api/v4/extract/task"
header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
data = {
    "url": "https://cdn-mineru.openxlab.org.cn/demo/example.pdf",
    "model_version": "vlm"
}
res = requests.post(url, headers=header, json=data)
print(res.status_code)
print(res.json())
print(res.json()["data"])
```

**HTML 文件：**

```python
import requests

token = "官网申请的api token"
url = "https://mineru.net/api/v4/extract/task"
header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
data = {
    "url": "https://****",
    "model_version": "MinerU-HTML"
}
res = requests.post(url, headers=header, json=data)
print(res.status_code)
print(res.json())
print(res.json()["data"])
```

### 请求参数

| 参数 | 类型 | 必选 | 默认值 | 描述 |
|------|------|------|--------|------|
| url | string | 是 | - | 文件 URL，支持 pdf/doc/docx/ppt/pptx/图片/html |
| model_version | string | 否 | pipeline | 模型版本：pipeline、vlm、MinerU-HTML。HTML 文件需指定 MinerU-HTML |
| is_ocr | bool | 否 | false | 是否启动 OCR，仅对 pipeline/vlm 有效 |
| enable_formula | bool | 否 | true | 是否开启公式识别，仅对 pipeline/vlm 有效 |
| enable_table | bool | 否 | true | 是否开启表格识别，仅对 pipeline/vlm 有效 |
| language | string | 否 | ch | 文档语言，可选值见 PaddleOCR 多语言列表 |
| page_ranges | string | 否 | - | 页码范围，如 "2,4-6" 或 "2--2"（倒数第二页） |
| extra_formats | [string] | 否 | - | 额外导出格式：docx、html、latex |
| no_cache | bool | 否 | false | 是否绕过缓存 |
| cache_tolerance | int | 否 | 900 | 缓存容忍时间（秒） |
| data_id | string | 否 | - | 业务数据 ID，用于标识 |
| callback | string | 否 | - | 回调通知 URL |
| seed | string | 否 | - | 回调签名随机字符串 |

### 响应参数

| 参数 | 类型 | 描述 |
|------|------|------|
| code | int | 状态码，0 表示成功 |
| msg | string | 处理信息 |
| trace_id | string | 请求 ID |
| data.task_id | string | 任务 ID，用于查询结果 |

### 响应示例

```json
{
  "code": 0,
  "data": {
    "task_id": "a90e6ab6-44f3-4554-b459-b62fe4c6b436"
  },
  "msg": "ok",
  "trace_id": "c876cd60b202f2396de1f9e39a1b0172"
}
```

---

## 获取任务结果

### 接口地址

```
GET https://mineru.net/api/v4/extract/task/{task_id}
```

### 请求示例

```python
import requests

token = "官网申请的api token"
task_id = "上一步创建任务返回的 task_id"
url = f"https://mineru.net/api/v4/extract/task/{task_id}"
header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
res = requests.get(url, headers=header)
print(res.status_code)
print(res.json())
print(res.json()["data"])
```

### 响应参数

| 参数 | 类型 | 描述 |
|------|------|------|
| code | int | 状态码，0 表示成功 |
| msg | string | 处理信息 |
| trace_id | string | 请求 ID |
| data.task_id | string | 任务 ID |
| data.state | string | 任务状态：done(完成)/pending(排队)/running(解析中)/failed(失败)/converting(转换中) |
| data.full_zip_url | string | 结果压缩包 URL，包含 full.md 等文件 |
| data.err_msg | string | 错误信息，state=failed 时有效 |
| data.extract_progress.extracted_pages | int | 已解析页数，state=running 时有效 |
| data.extract_progress.total_pages | int | 总页数，state=running 时有效 |
| data.extract_progress.start_time | string | 解析开始时间 |

### 响应示例

**处理中：**

```json
{
  "code": 0,
  "data": {
    "task_id": "47726b6e-46ca-4bb9-******",
    "state": "running",
    "err_msg": "",
    "extract_progress": {
      "extracted_pages": 1,
      "total_pages": 2,
      "start_time": "2025-01-20 11:43:20"
    }
  },
  "msg": "ok",
  "trace_id": "c876cd60b202f2396de1f9e39a1b0172"
}
```

**完成：**

```json
{
  "code": 0,
  "data": {
    "task_id": "47726b6e-46ca-4bb9-******",
    "state": "done",
    "full_zip_url": "https://cdn-mineru.openxlab.org.cn/pdf/018e53ad-d4f1-475d-b380-36bf24db9914.zip",
    "err_msg": ""
  },
  "msg": "ok",
  "trace_id": "c876cd60b202f2396de1f9e39a1b0172"
}
```

---

## 结果文件说明

下载 `full_zip_url` 后解压，包含以下文件：

| 文件 | 说明 |
|------|------|
| full.md | Markdown 解析结果 |
| layout.json | 中间处理结果 (middle.json) |
| *_model.json | 模型推理结果 |
| *_content_list.json | 内容列表 |

**HTML 文件解析结果略有不同：**
- full.md：Markdown 解析结果
- main.html：提取后正文 HTML

---

## 常见错误码

| 错误码 | 说明 | 解决建议 |
|--------|------|----------|
| A0202 | Token 错误 | 检查 Token 是否正确，是否有 Bearer 前缀 |
| A0211 | Token 过期 | 更换新 Token |
| -500 | 传参错误 | 确保参数类型及 Content-Type 正确 |
| -60005 | 文件大小超出限制 | 最大支持 200MB |
| -60006 | 文件页数超过限制 | 最大支持 600 页 |
| -60010 | 解析失败 | 请稍后重试 |
