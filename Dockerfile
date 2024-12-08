# Using Python 3.9 as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install necessary dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    tar \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download and extract CloudflareST
RUN curl -L -o CloudflareST_linux_amd64.tar.gz https://github.com/XIU2/CloudflareSpeedTest/releases/download/v2.2.5/CloudflareST_linux_amd64.tar.gz \
    && tar -xzf CloudflareST_linux_amd64.tar.gz -C /app/config/ \
    && rm CloudflareST_linux_amd64.tar.gz

# Copy the project files
COPY . .

# Set the environment variable
ENV PYTHONUNBUFFERED=1

# Run the main script
ENTRYPOINT ["python", "main.py"]