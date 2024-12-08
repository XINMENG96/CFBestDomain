# 使用多阶段构建
# 第一阶段：基础镜像和依赖安装
FROM alpine:3.20 as base

# 设置工作目录
WORKDIR /app

# 安装必要的依赖
RUN apk update && apk add --no-cache \
    curl \
    unzip \
    tar \
    python3 \
    py3-pip \
    build-base \
    libffi-dev \
    openssl-dev

# 安装 Python 包
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt || { cat /root/.cache/pip/log/debug.log; exit 1; }

# 第二阶段：复制代码并执行
FROM base as builder

# 复制项目文件
COPY . .

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 运行主程序
ENTRYPOINT ["python3", "main.py"]

# 第三阶段：处理不同架构的下载和配置
FROM builder as downloader

# 设置工作目录
WORKDIR /app/config

# 下载并解压 CloudflareST
RUN python3 app/cst_dl.py

# 生成默认的 app.env 文件
RUN python3 app/gen_env.py

# 第四阶段：最终镜像
FROM base

# 复制基础镜像和下载文件
COPY --from=downloader /app /app

# 设置工作目录
WORKDIR /app

# 运行主程序
ENTRYPOINT ["python3", "main.py"]