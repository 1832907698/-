# 网易云用户评论爬虫

这是一个用于爬取网易云音乐用户在歌曲下方评论的 Python 脚本。你只需要输入用户 ID，即可抓取该用户在网易云所有听过歌曲下的评论。

## ✅ 功能
- 支持查找用户所有歌曲评论
- 自动保存到本地 `results.txt`
- 使用加密接口，支持获取更多评论

## 📦 依赖
- Python 3.x
- requests
- pycryptodome （用于 AES 加密）

## 🚀 使用方法
1. 安装依赖：`pip install requests pycryptodome`
2. 运行脚本：`python NEMComments.py`
3. 输入用户 ID 开始爬取

## ⚠️ 注意事项
- 如果接口变动或网易云增加反爬机制，本项目可能失效
- 请勿用于非法用途，仅供学习交流

## 🙋‍♂️ 作者
MillerD（原始代码）  
由我做了整理与分享，欢迎点赞 🌟
