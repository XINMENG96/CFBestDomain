import os
import platform
import requests
import zipfile
import tarfile
import shutil
from dotenv import load_dotenv

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

# Function to check if the file or folder already exists
def check_existing_files(download_dir, zip_filename):
    folder_name = os.path.splitext(zip_filename)[0]
    if os.path.exists(folder_name):
        print(f"解压文件夹已存在: {folder_name}，跳过解压")
        return True
    if os.path.exists(zip_filename):
        print(f"压缩包已存在: {zip_filename}，跳过下载")
        return False
    return False

# 解压文件的函数，处理zip和tar.gz
def extract_file(zip_filename, folder_name):
    if zip_filename.endswith(".zip"):
        try:
            with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                zip_ref.testzip()  # 测试文件完整性
                zip_ref.extractall(folder_name)
            print(f"文件解压完成: {folder_name}")
        except zipfile.BadZipFile:
            print(f"下载的文件不是一个有效的ZIP文件: {zip_filename}")
            return False
    elif zip_filename.endswith(".tar.gz"):
        try:
            with tarfile.open(zip_filename, "r:gz") as tar_ref:
                tar_ref.extractall(folder_name)
            print(f"文件解压完成: {folder_name}")
        except tarfile.TarError:
            print(f"下载的文件不是一个有效的TAR文件: {zip_filename}")
            return False
    else:
        print("不支持的文件格式")
        return False
    return True

# 下载并解压 CloudflareST
def download_and_extract(url):
    script_dir = get_script_dir()
    download_dir = script_dir  # 下载位置为脚本目录

    zip_filename = os.path.join(download_dir, url.split("/")[-1])

    if check_existing_files(download_dir, zip_filename):
        return  # 如果文件夹或压缩包已存在，则跳过下载

    print(f"开始下载: {url}")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(zip_filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"下载完成: {zip_filename}")

        # Remove any extensions like .zip, .tar, .gz from the folder name
        folder_name = zip_filename
        for ext in [".zip", ".tar", ".gz"]:
            folder_name = folder_name.replace(ext, "")
        
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # 尝试解压
        if not extract_file(zip_filename, folder_name):
            # 解压失败，删除压缩包并重新下载
            os.remove(zip_filename)
            print(f"重新下载: {zip_filename}")
            download_and_extract(url)
        else:
            # 删除压缩包
            os.remove(zip_filename)
            print(f"删除压缩包: {zip_filename}")
    else:
        print(f"下载失败，HTTP 状态码: {response.status_code}")

def main():
    load_dotenv(os.path.join(get_script_dir(), '..', 'config', 'app.env'))
    system = platform.system()
    arch = platform.machine()
    proxy = os.getenv('GITHUB_PROXY', '')

    print(f"系统类型: {system}, 架构: {arch}")
    
    # 根据系统类型选择下载URL
    if system == 'Windows':
        if arch == 'AMD64':
            download_url = 'https://github.com/XIU2/CloudflareSpeedTest/releases/download/v2.2.5/CloudflareST_windows_amd64.zip'
        elif arch == 'x86':
            download_url = 'https://github.com/XIU2/CloudflareSpeedTest/releases/download/v2.2.5/CloudflareST_windows_386.zip'
        elif arch == 'ARM64':
            download_url = 'https://github.com/XIU2/CloudflareSpeedTest/releases/download/v2.2.5/CloudflareST_windows_arm64.zip'
        else:
            print(f"不支持的架构: {arch}")
            return
    elif system == 'Linux':
        if arch == 'x86_64':
            download_url = 'https://github.com/XIU2/CloudflareSpeedTest/releases/download/v2.2.5/CloudflareST_linux_amd64.tar.gz'
        elif arch == 'x86':
            download_url = 'https://github.com/XIU2/CloudflareSpeedTest/releases/download/v2.2.5/CloudflareST_linux_386.tar.gz'
        elif arch == 'aarch64':
            download_url = 'https://github.com/XIU2/CloudflareSpeedTest/releases/download/v2.2.5/CloudflareST_linux_arm64.tar.gz'
        elif arch.startswith('arm'):
            if 'v5' in arch:
                download_url = 'https://github.com/XIU2/CloudflareSpeedTest/releases/download/v2.2.5/CloudflareST_linux_armv5.tar.gz'
            elif 'v6' in arch:
                download_url = 'https://github.com/XIU2/CloudflareSpeedTest/releases/download/v2.2.5/CloudflareST_linux_armv6.tar.gz'
            elif 'v7' in arch:
                download_url = 'https://github.com/XIU2/CloudflareSpeedTest/releases/download/v2.2.5/CloudflareST_linux_armv7.tar.gz'
            else:
                print(f"不支持的 ARM 架构: {arch}")
                return
        elif arch == 'mips':
            download_url = 'https://github.com/XIU2/CloudflareSpeedTest/releases/download/v2.2.5/CloudflareST_linux_mips.tar.gz'
        elif arch == 'mips64':
            download_url = 'https://github.com/XIU2/CloudflareSpeedTest/releases/download/v2.2.5/CloudflareST_linux_mips64.tar.gz'
        elif arch == 'mips64le':
            download_url = 'https://github.com/XIU2/CloudflareSpeedTest/releases/download/v2.2.5/CloudflareST_linux_mips64le.tar.gz'
        elif arch == 'mipsle':
            download_url = 'https://github.com/XIU2/CloudflareSpeedTest/releases/download/v2.2.5/CloudflareST_linux_mipsle.tar.gz'
        else:
            print(f"不支持的架构: {arch}")
            return
    elif system == 'Darwin':
        if arch == 'x86_64':
            download_url = 'https://github.com/XIU2/CloudflareSpeedTest/releases/download/v2.2.5/CloudflareST_darwin_amd64.zip'
        elif arch == 'arm64':
            download_url = 'https://github.com/XIU2/CloudflareSpeedTest/releases/download/v2.2.5/CloudflareST_darwin_arm64.zip'
        else:
            print(f"不支持的架构: {arch}")
            return
    else:
        print(f"不支持的操作系统: {system}")
        return

    if proxy:
        download_url = f"{proxy}/{download_url}"

    download_and_extract(download_url)

if __name__ == "__main__":
    main()
