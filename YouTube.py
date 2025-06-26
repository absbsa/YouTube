import os
import subprocess
import sys
import re
import hashlib
from urllib.parse import urlparse, parse_qs
from datetime import datetime

# 设置环境变量，强制 subprocess 使用 UTF-8 编码
os.environ["PYTHONIOENCODING"] = "utf-8"

# 先检查 yt-dlp 是否可用
try:
    result = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True, encoding="utf-8")
    print(f"yt-dlp 版本: {result.stdout.strip()}")
except Exception as e:
    print(f"yt-dlp 未安装或不在 PATH 中: {e}")
    print("请使用命令安装: pip install yt-dlp")
    sys.exit(1)

# 检查 cookies 文件是否存在
cookies_path = r"C:\Users\替换成实际用户名称\Desktop\www.youtube.com_cookies.txt"
if not os.path.exists(cookies_path):
    print(f"cookies 文件不存在: {cookies_path}")
    print("下载将继续但可能无法访问需要登录的内容")
    use_cookies = False
else:
    use_cookies = True

# YouTube 视频链接列表
video_urls = [
    "https://www.youtube.com/watch?v=h3fnANJfV9I",
    # 添加更多链接
]

# 输出目录
output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "yt_clips")
os.makedirs(output_dir, exist_ok=True)

def get_video_id(url):
    """从YouTube URL中提取视频ID"""
    parsed_url = urlparse(url)
    if parsed_url.hostname in ('youtu.be', 'www.youtu.be'):
        return parsed_url.path[1:]
    if parsed_url.hostname in ('youtube.com', 'www.youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
    return hashlib.md5(url.encode()).hexdigest()[:10]

def download_video(url, index):
    # 提取视频ID作为文件名的一部分，防止覆盖
    video_id = get_video_id(url)
    output_video_path = os.path.join(output_dir, f"video_{index+1}_{video_id}.mp4")
    
    print(f"开始下载视频 {index+1}: {url}")
    print(f"将保存为: {output_video_path}")
    
    # 构建基本命令
    base_cmd = ["yt-dlp"]
    
    # 如果有cookies文件，则使用
    if use_cookies:
        base_cmd.extend(["--cookies", cookies_path])
    
    # 获取格式信息
    info_cmd = base_cmd + ["-F", url]
    
    try:
        # 明确指定 encoding='utf-8'
        result = subprocess.run(info_cmd, capture_output=True, text=True, encoding='utf-8')
        if result.stdout:
            print("格式信息获取成功")
        else:
            raise Exception("获取格式信息失败，输出为空")
    except Exception as e:
        print(f"获取视频格式失败: {e}")
        # 使用默认格式下载
        format_spec = "bestvideo[height>=1080]+bestaudio/best[height>=1080]/best"
        print(f"使用默认格式: {format_spec}")
        
        # 构建下载命令
        download_cmd = base_cmd + ["-f", format_spec, "-o", output_video_path, url]
        subprocess.run(download_cmd, check=True, encoding='utf-8')
        return
    
    # 解析格式信息
    lines = result.stdout.splitlines() if result.stdout else []
    best_format = None
    best_height = 0
    
    for line in lines:
        if "video only" not in line and "audio only" not in line:
            continue
        
        parts = line.strip().split()
        if len(parts) < 3:
            continue
            
        try:
            format_id = parts[0]
            
            # 查找分辨率信息
            resolution = None
            for part in parts:
                if "x" in part:
                    resolution = part
                    break
                    
            if not resolution:
                continue
                
            try:
                height = int(resolution.split('x')[1])
                
                if "video only" in line and height > best_height:
                    best_height = height
                    best_format = format_id
            except:
                continue
        except:
            continue
    
    # 设置格式
    if best_format:
        format_spec = f"{best_format}+bestaudio/best"
        print(f"检测到最佳格式: {format_spec}（分辨率约 {best_height}p）")
    else:
        format_spec = "bestvideo[height>=1080]+bestaudio/best[height>=1080]/best"
        print(f"未找到合适格式，使用默认: {format_spec}")
    
    # 执行下载
    try:
        download_cmd = base_cmd + ["-f", format_spec, "-o", output_video_path, url]
        print("执行命令: " + " ".join(download_cmd))
        # 不使用 verbose 模式，减少编码错误风险
        subprocess.run(download_cmd, encoding='utf-8')
        print(f"视频下载完成，保存到: {output_video_path}")
    except Exception as e:
        print(f"下载失败: {e}")

def main():
    for idx, url in enumerate(video_urls):
        try:
            download_video(url, idx)
        except Exception as e:
            print(f"处理视频 {idx+1} 时发生错误: {e}")

if __name__ == "__main__":
    main()