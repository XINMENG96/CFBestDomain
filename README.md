# CFBestDomain
CFBestDomain 是一个自动优化 Cloudflare CDN IP 的工具，旨在提高网站访问速度和稳定性。该工具通过实时获取最佳的 Cloudflare CDN IP，并使用 DNS 解析技术生成优化后的域名，帮助用户实现更快的加载速度和更低的延迟。  主要功能： 自动优化 Cloudflare CDN IP：根据网络状况自动选择最快的 Cloudflare CDN IP。 DNS 解析：利用优选 IP 自动进行 DNS 解析，生成快速响应的域名。 易于配置：通过简单的配置文件即可设置定时任务，自动更新 CDN IP。 跨平台支持：支持 Windows、Linux 和 macOS 操作系统。

该项目使用 [CloudflareSpeedTest](https://github.com/XIU2/CloudflareSpeedTest) 项目来进行IP测速。

# CFBestDomain

**CFBestDomain** 是一个自动优化 Cloudflare CDN IP 的工具，它可以通过 DNS 解析生成优选域名。该项目旨在提供一个自动化解决方案，以提升 Cloudflare 的 CDN 性能，通过智能选择最适合的 IP 来加速网页访问。

## 功能

- 自动优选 Cloudflare CDN IP。
- 生成优化的域名。
- 自动更新 DNS 记录。
- 支持定时执行，用户可以通过环境变量配置任务执行间隔。

## 安装

1. **克隆仓库**：
   首先，你需要将仓库克隆到本地：

   ```bash
   git clone https://github.com/your-username/CFBestDomain.git
   cd CFBestDomain
安装依赖： 使用 pip 安装项目的依赖：

bash
复制代码
pip install -r requirements.txt
配置环境变量： 创建一个 .env 文件，配置以下变量：

text
复制代码
INTERVAL_MINUTES=120  # 设置定时执行间隔，单位为分钟
如果你不想设置定时任务，可以将 INTERVAL_MINUTES 设为 0 或注释掉该行。
运行脚本： 执行 main.py 脚本来启动项目：

bash
复制代码
python main.py
默认情况下，项目会执行一次。如果你设置了定时任务，它将根据配置的间隔时间进行循环执行。

目录结构
bash
复制代码
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
环境要求
Python 3.x
所需的 Python 库可以通过 requirements.txt 安装。
贡献
欢迎提出问题或提交 Pull Request！如果你有任何问题或建议，请随时在 GitHub 上创建 issue 或通过 PR 进行贡献。

License
本项目采用 MIT License 开源。

markdown
复制代码

---

### 说明
- **功能部分**：简要说明了项目的核心功能。
- **安装部分**：包含了安装、配置和运行的步骤，确保用户可以顺利启动项目。
- **目录结构**：展示了项目文件的组织方式，让用户了解每个文件的作用。
- **环境要求**：列出了项目所需要的基础环境。
- **贡献**：鼓励开源社区的参与。
- **License**：表明项目使用 MIT 许可证。

你可以根据具体情况进一步调整内容，尤其是 `功能` 和 `安装` 部分。
