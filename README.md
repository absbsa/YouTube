# YouTube 自动化工具

这是一个自动化脚本项目，支持批量采集高清 YouTube 视频，适用于运营矩阵、素材收集等场景。

## 📥 下载源码

- [点击下载本项目 ZIP 包](https://github.com/absbsa/YouTube/archive/refs/heads/main.zip)

---

## ✨ 功能介绍

- 批量轮流采集 1080P 和 2160P 视频；
- 支持通过浏览器插件导出 cookies 自动登录；
- 支持配置多个视频链接轮流下载；
- 使用 `yt-dlp` 实现高质量无水印下载；
- 可扩展模块化结构，便于后续功能扩展。

---

## 🧰 使用准备

1. **安装浏览器插件获取 cookies：**  
   安装插件 [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc?hl=zh-CN&utm_source=ext_sidebar)  
   登录 YouTube 后点击导出 cookies，保存至桌面，记住路径。

2. **设置 cookies 路径：**  
   修改脚本中的路径为你实际导出的 cookies 文件位置：

   ```python
   cookies_path = r"C:\Users\你的用户名\Desktop\www.youtube.com_cookies.txt"

注意浏览器清理后需要更新cookies文件

3.设置待下载链接：
video_urls = [
    "https://www.youtube.com/watch?v=示例1",
    "https://www.youtube.com/watch?v=示例2",
    ...
]
4.安装最新版 yt-dlp：pip install -U yt-dlp

项目结构
/YouTube
├── main.py                     # 主程序入口
├── config.py                   # 配置项定义（如 cookies_path、video_urls）
├── downloader/                 # 下载模块
│   └── youtube_downloader.py   # yt-dlp 调用封装
├── utils/                      # 工具函数（如日志、路径处理）
│   └── logger.py
├── requirements.txt            # 项目依赖列表
├── .gitignore                  # Git 忽略配置
└── README.md                   # 项目说明文档

🚀 快速开始
git clone https://github.com/absbsa/YouTube.git
cd YouTube
pip install -U yt-dlp
python main.py

 ⚠️注意事项
确保下载源链接可访问，必要时配合代理工具；

cookies 有效期有限，建议定期更新；

下载 2160P 视频需源视频本身支持此清晰度；

脚本默认使用 yt-dlp 的 bestvideo+bestaudio 格式自动组合下载。

📌 TODO（后续规划）
 视频处理自动化（裁剪、封面生成）

 多账号登录切换

 下载历史记录过滤

 错误日志与断点续传支持

本项目由 @absbsa 维护，如有建议或需求欢迎提 Issue / PR。

---



