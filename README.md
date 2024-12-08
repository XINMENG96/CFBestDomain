# CFBestDomain

CFBestDomain 是一个自动优化 Cloudflare CDN IP 的工具，旨在提高网站访问速度和稳定性。该工具通过实时获取最佳的 Cloudflare CDN IP，并使用 DNS 解析技术生成优化后的域名，帮助用户实现更快的加载速度和更低的延迟。

该项目使用 [CloudflareSpeedTest](https://github.com/XIU2/CloudflareSpeedTest) 项目来进行IP测速。

## 主要功能

- **自动优化 Cloudflare CDN IP**：根据网络状况自动选择最快的 Cloudflare CDN IP。
- **DNS 解析**：利用优选 IP 自动进行 DNS 解析，生成快速响应的域名。
- **易于配置**：通过简单的配置文件即可设置定时任务，自动更新 CDN IP。
- **跨平台支持**：支持 Windows、Linux 和 macOS 操作系统。

## 安装

1. **克隆仓库**：
   首先，你需要将仓库克隆到本地：

   ```bash
   git clone https://github.com/XINMENG96/CFBestDomain.git
   cd CFBestDomain
   ```

2. **安装依赖**：
   使用 pip 安装项目的依赖：

   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**：
   在 `.env` 文件中设置任务的执行间隔时间，单位为分钟。例如，设置每隔 120 分钟执行一次：

   ```text
   INTERVAL_MINUTES=120 
   ```

   > 设置定时执行间隔，单位为分钟
   > 如果你不想设置定时任务，可以将 INTERVAL_MINUTES 设为 0 或注释掉该行。

4. **运行脚本**：
   执行 `main.py` 脚本来启动项目：

   ```bash
   python main.py
   ```

   默认情况下，项目会执行一次。如果你设置了定时任务，它将根据配置的间隔时间进行循环执行。

## 目录结构

```bash
CFBestDomain/
│
├── app/                 # 存放所有脚本的目录
│   ├── check_csv.py     # 检查 CSV 文件是否最新
│   ├── cst_dl.py        # 下载并解压 CloudflareST
│   ├── gen_env.py       # 生成 app.env 配置文件
│   ├── cst_run.py       # 运行 CloudflareST
│   ├── dns_refresh.py   # 更新 DNS 记录
│
├── config/              # 配置文件目录
│   ├── app.env          # 环境变量配置文件
│
├── requirements.txt     # 项目依赖
└── main.py              # 主脚本，启动项目流程
```

## 环境要求

- Python 3.x
- 所需的 Python 库可以通过 `requirements.txt` 安装。

## 贡献

欢迎提出问题或提交 Pull Request！如果你有任何问题或建议，请随时在 GitHub 上创建 issue 或通过 PR 进行贡献。

## License

本项目采用 MIT License 开源。
