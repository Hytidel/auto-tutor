#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Everything to Markdown Converter
使用 MinerU API 将各种文档格式转换为 Markdown
"""

import os
import sys
import time
import requests
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv

# API 配置
API_BASE_URL = "https://mineru.net/api/v4"
SUPPORTED_EXTENSIONS = {
    'pdf', 'png', 'jpg', 'jpeg', 'jp2', 'webp', 'gif', 'bmp', 
    'doc', 'docx', 'ppt', 'pptx', 'html'
}


def get_api_key(project_root: str = None) -> str:
    """
    从项目 settings 目录的 .env 文件读取 MINERU_API_KEY
    
    Args:
        project_root: 项目根目录路径
    
    Returns:
        API Key 字符串
    
    Raises:
        ValueError: API Key 未配置或无效
    """
    if project_root is None:
        # 尝试找到项目根目录（包含 settings/.env 的目录）
        current_dir = Path(__file__).resolve()
        while current_dir.parent != current_dir:
            settings_env_path = current_dir / "settings" / ".env"
            if settings_env_path.exists():
                project_root = str(current_dir)
                break
            current_dir = current_dir.parent
        else:
            project_root = os.getcwd()
    
    # 加载 settings/.env 文件
    env_path = os.path.join(project_root, "settings", ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
    
    api_key = os.getenv("MINERU_API_KEY")
    
    if not api_key:
        raise ValueError(
            f"未找到 MINERU_API_KEY 环境变量\n"
            f"请在 {env_path} 中添加:\n"
            "MINERU_API_KEY=your-api-key"
        )
    
    if api_key == "TODO" or api_key == "your-api-key":
        raise ValueError(
            "API Key 无效，请在 .env 中设置有效的 MINERU_API_KEY\n"
            "申请地址: https://mineru.net"
        )
    
    return api_key


def is_url(text: str) -> bool:
    """判断输入是否为 URL"""
    try:
        result = urlparse(text)
        return all([result.scheme, result.netloc])
    except:
        return False


def get_file_extension(file_path: str) -> str:
    """获取文件扩展名"""
    if is_url(file_path):
        # 从 URL 中提取扩展名
        path = urlparse(file_path).path
        ext = Path(path).suffix.lstrip('.').lower()
    else:
        ext = Path(file_path).suffix.lstrip('.').lower()
    return ext


def create_task_from_url(api_key: str, url: str) -> str:
    """
    通过 URL 创建解析任务
    
    Args:
        api_key: MinerU API Key
        url: 文件 URL
    
    Returns:
        task_id
    """
    ext = get_file_extension(url)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # 根据 URL 类型选择模型版本
    data = {"url": url}
    if ext == 'html':
        data["model_version"] = "MinerU-HTML"
    else:
        data["model_version"] = "vlm"
    
    response = requests.post(
        f"{API_BASE_URL}/extract/task",
        headers=headers,
        json=data
    )
    
    if response.status_code != 200:
        raise Exception(f"创建任务失败: HTTP {response.status_code} - {response.text}")
    
    result = response.json()
    if result.get("code") != 0:
        raise Exception(f"创建任务失败: {result.get('msg')}")
    
    return result["data"]["task_id"]


def create_task_from_file(api_key: str, file_path: str) -> tuple:
    """
    通过本地文件创建解析任务
    
    Args:
        api_key: MinerU API Key
        file_path: 本地文件路径
    
    Returns:
        (batch_id, task_id 或 None)
    """
    file_name = os.path.basename(file_path)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    ext = get_file_extension(file_path)
    
    # 根据 URL 类型选择模型版本
    data = {
        "files": [{"name": file_name}],
    }
    if ext == 'html':
        data["model_version"] = "MinerU-HTML"
    else:
        data["model_version"] = "vlm"
    
    # 1. 获取上传 URL
    response = requests.post(
        f"{API_BASE_URL}/file-urls/batch",
        headers=headers,
        json=data
    )
    
    if response.status_code != 200:
        raise Exception(f"获取上传 URL 失败: HTTP {response.status_code} - {response.text}")
    
    result = response.json()
    if result.get("code") != 0:
        raise Exception(f"获取上传 URL 失败: {result.get('msg')}")
    
    batch_id = result["data"]["batch_id"]
    upload_url = result["data"]["file_urls"][0]
    
    print(f"上传 URL 已获取，batch_id: {batch_id}")
    
    # 2. 上传文件
    with open(file_path, 'rb') as f:
        upload_response = requests.put(upload_url, data=f)
    
    if upload_response.status_code != 200:
        raise Exception(f"文件上传失败: HTTP {upload_response.status_code}")
    
    print(f"文件上传成功: {file_name}")
    
    return batch_id


def poll_task_result(api_key: str, task_id: str = None, batch_id: str = None, 
                     timeout: int = 300, interval: int = 5) -> dict:
    """
    轮询获取任务结果
    
    Args:
        api_key: MinerU API Key
        task_id: 单个任务 ID
        batch_id: 批量任务 ID
        timeout: 超时时间（秒）
        interval: 轮询间隔（秒）
    
    Returns:
        任务结果数据
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    if batch_id:
        url = f"{API_BASE_URL}/extract-results/batch/{batch_id}"
    else:
        url = f"{API_BASE_URL}/extract/task/{task_id}"
    
    state_labels = {
        "pending": "排队中",
        "running": "解析中",
        "converting": "格式转换中",
        "waiting-file": "等待文件上传",
        "uploading": "文件下载中"
    }
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"查询任务失败: HTTP {response.status_code}")
        
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"查询任务失败: {result.get('msg')}")
        
        data = result["data"]
        
        # 处理批量任务结果
        if batch_id and "extract_result" in data:
            extract_result = data["extract_result"][0]
            state = extract_result.get("state")
            full_zip_url = extract_result.get("full_zip_url")
            err_msg = extract_result.get("err_msg")
        else:
            state = data.get("state")
            full_zip_url = data.get("full_zip_url")
            err_msg = data.get("err_msg")
        
        elapsed = int(time.time() - start_time)
        
        if state == "done":
            print(f"\n解析完成！耗时 {elapsed} 秒")
            return {"full_zip_url": full_zip_url}
        
        if state == "failed":
            raise Exception(f"解析失败: {err_msg}")
        
        # 显示进度
        state_text = state_labels.get(state, state)
        
        # 显示解析进度
        if batch_id and "extract_result" in data:
            progress = data["extract_result"][0].get("extract_progress", {})
        else:
            progress = data.get("extract_progress", {})
        
        if progress:
            extracted = progress.get("extracted_pages", 0)
            total = progress.get("total_pages", 0)
            print(f"\r{state_text}... ({extracted}/{total} 页, {elapsed}s)", end="", flush=True)
        else:
            print(f"\r{state_text}... ({elapsed}s)", end="", flush=True)
        
        time.sleep(interval)
    
    raise TimeoutError(f"解析超时（{timeout}秒）")


def download_markdown(zip_url: str, output_dir: str, base_name: str = None) -> str:
    """
    下载并解压 Markdown 文件
    
    Args:
        zip_url: 结果压缩包 URL
        output_dir: 输出目录
        base_name: 输出文件基础名称
    
    Returns:
        保存的 Markdown 文件路径（解压目录中的 full.md）
    """
    import zipfile
    import io
    from datetime import datetime
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"正在下载结果...")
    
    response = requests.get(zip_url)
    if response.status_code != 200:
        raise Exception(f"下载失败: HTTP {response.status_code}")
    
    # 确定解压目录名（添加时间戳）
    if base_name:
        extract_name = base_name
    else:
        extract_name = "converted"
    
    # 添加时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    extract_dir = os.path.join(output_dir, f"{extract_name}_{timestamp}")
    
    # 解压 zip 文件
    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        os.makedirs(extract_dir, exist_ok=True)
        zf.extractall(extract_dir)
    
    # 查找 full.md 文件路径
    md_path = os.path.join(extract_dir, "full.md")
    if not os.path.exists(md_path):
        raise Exception("解压后未找到 full.md 文件")
    
    print(f"Markdown 已保存: {md_path}")
    print(f"完整结果已解压到: {extract_dir}")
    
    return md_path


def convert_to_markdown(input_path: str, output_dir: str = None, 
                        project_root: str = None) -> str:
    """
    将文件转换为 Markdown
    
    Args:
        input_path: 输入文件路径或 URL
        output_dir: 输出目录，默认为 ./tmp/
        project_root: 项目根目录
    
    Returns:
        保存的 Markdown 文件路径
    """
    # 获取 API Key
    api_key = get_api_key(project_root)
    print(f"API Key 已加载")
    
    # 设置输出目录
    if output_dir is None:
        if project_root:
            output_dir = os.path.join(project_root, "tmp")
        else:
            output_dir = "./tmp"
    
    # 获取基础文件名
    if is_url(input_path):
        base_name = Path(urlparse(input_path).path).stem
    else:
        base_name = Path(input_path).stem
    
    print(f"正在处理: {input_path}")
    
    # 创建任务
    if is_url(input_path):
        print("检测到 URL，使用 URL 解析模式...")
        task_id = create_task_from_url(api_key, input_path)
        print(f"任务已创建: {task_id}")
        
        # 轮询结果
        result = poll_task_result(api_key, task_id=task_id)
    else:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"文件不存在: {input_path}")
        
        ext = get_file_extension(input_path)
        if ext not in SUPPORTED_EXTENSIONS:
            raise ValueError(f"不支持的文件类型: {ext}\n支持的类型: {', '.join(SUPPORTED_EXTENSIONS)}")
        
        print("检测到本地文件，使用文件上传模式...")
        batch_id = create_task_from_file(api_key, input_path)
        
        # 轮询结果
        result = poll_task_result(api_key, batch_id=batch_id)
    
    # 下载 Markdown
    return download_markdown(result["full_zip_url"], output_dir, base_name)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python convert_to_markdown.py <file_path_or_url> [output_dir]")
        print("\n支持的文件类型:")
        print("  - PDF 文档")
        print("  - 图片: png, jpg, jpeg, jp2, webp, gif, bmp")
        print("  - Office: doc, docx, ppt, pptx")
        print("  - 网页: HTML URL")
        print("\n示例:")
        print("  python convert_to_markdown.py document.pdf")
        print("  python convert_to_markdown.py https://example.com/document.pdf")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        output_path = convert_to_markdown(input_path, output_dir)
        print(f"\n转换成功: {output_path}")
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
