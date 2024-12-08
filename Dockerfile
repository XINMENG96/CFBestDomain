# Using Ubuntu as the base image
FROM ubuntu:20.04

# Set the working directory
WORKDIR /app

# Install necessary dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    curl \
    unzip \
    tar \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Set the environment variable
ENV PYTHONUNBUFFERED=1

# Run the main script
ENTRYPOINT ["python3", "main.py"]