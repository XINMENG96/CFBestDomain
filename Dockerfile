# 使用 Python 3.9 的官方 Alpine 镜像作为基础镜像
FROM python:3.9-alpine

# 设置作者信息
LABEL authors="qetesh"

# 设置工作目录
WORKDIR /app

# 安装必要的依赖
RUN apk update && apk add --no-cache \
    curl \
    unzip \
    tar \
    build-base \
    libffi-dev \
    openssl-dev \
    busybox-suid \
    shadow \
    bash \
    cronie

# 安装 Python 包
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/

# 复制项目文件
COPY . .

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 启动主脚本
CMD ["python3", "main.py"]