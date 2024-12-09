# CFBestDomain
[![CFBestDomain docker image](https://github.com/XINMENG96/CFBestDomain/actions/workflows/docker-image.yml/badge.svg)](https://github.com/XINMENG96/CFBestDomain/actions/workflows/docker-image.yml)

CFBestDomain 是一个自动优选 Cloudflare CDN IP 的工具，于当前网络下对 CDN 优选。该工具通过实时获取最佳的 Cloudflare CDN IP，并自动更新域名解析，帮助实现更快的加载速度和更低的延迟。

该项目使用 [CloudflareSpeedTest](https://github.com/XIU2/CloudflareSpeedTest) 项目来进行 Cloudflare CDN IP 测速。

## 主要功能

- **自动优选 Cloudflare CDN IP**：根据网络状况自动选择最快的 Cloudflare CDN IP。
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

## 使用 Docker

你也可以使用 Docker 来运行该项目。以下是使用 Docker 的步骤：

1. **构建 Docker 镜像**：

   ```bash
   docker build -t cfbestdomain .
   ```

2. **运行 Docker 容器**：

   ```bash
   docker run -d --name cfbestdomain -v $(pwd)/config:/app/config cfbestdomain
   ```

   这将启动一个 Docker 容器，并将本地的 `config` 目录挂载到容器内的 `/app/config` 目录。

3. **使用编译好的 Docker 镜像**：

   你也可以使用已经编译好的 Docker 镜像来运行该项目：

   ```bash
   docker run -d \
     --name cfbestdomain \
     -v ./config:/app/config \
     -e PYTHONUNBUFFERED=1 \
     xinmeng96/cfbestdomain:latest \
     python main.py
   ```

## 使用 Docker Compose

你也可以使用 Docker Compose 来管理和运行该项目。以下是使用 Docker Compose 的步骤：

1. **创建 `docker-compose.yml` 文件**：

   在项目根目录下创建一个 `docker-compose.yml` 文件，并添加以下内容：

   ```yaml
   version: '3'
   services:
     cfbestdomain:
       build: .
       volumes:
         - ./config:/app/config
       environment:
         - INTERVAL_MINUTES=120
   ```

   你也可以参考 [docker-compose.yml 示例](https://github.com/XINMENG96/CFBestDomain/blob/main/docker-compose.yml)。

2. **启动服务**：

   使用以下命令启动 Docker Compose 服务：

   ```bash
   docker-compose up -d
   ```

   这将构建并启动服务，并根据 `docker-compose.yml` 文件中的配置进行设置。

## 目录结构

```
CFBestDomain/
├── config/               # 配置文件目录
│   └── config.yaml       # 配置文件示例
├── scripts/              # 脚本目录
│   └── update_ip.py      # 更新 IP 的脚本
├── tests/                # 测试目录
│   └── test_main.py      # 主脚本的测试文件
├── .env                  # 环境变量配置文件
├── Dockerfile            # Docker 配置文件
├── README.md             # 项目说明文件
├── main.py               # 主脚本文件
└── requirements.txt      # 依赖包列表
```

## 环境要求

- Python 3.x
- 所需的 Python 库可以通过 `requirements.txt` 安装。

## 贡献

欢迎提出问题或提交 Pull Request！如果你有任何问题或建议，请随时在 GitHub 上创建 issue 或通过 PR 进行贡献。

## License

本项目采用 MIT License 开源。
