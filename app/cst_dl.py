import os
import platform
import requests
import zipfile
import tarfile
import shutil

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
    download_dir = os.path.join(script_dir, '..', 'config')  # 下载位置为 /config

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

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

        folder_name = os.path.splitext(zip_filename)[0]
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
    system = platform.system()
    arch = platform.architecture()[0]
    
    # 根据系统类型选择下载URL
    if system == 'Windows' and arch == '64bit':
        download_url = 'https://github.com/XIU2/CloudflareSpeedTest/releases/download/v2.2.5/CloudflareST_windows_amd64.zip'
    elif system == 'Linux' and arch == '64bit':
        download_url = 'https://github.com/XIU2/CloudflareSpeedTest/releases/download/v2.2.5/CloudflareST_linux_amd64.tar.gz'
    elif system == 'Darwin' and arch == '64bit':
        download_url = 'https://github.com/XIU2/CloudflareSpeedTest/releases/download/v2.2.5/CloudflareST_darwin_amd64.zip'
    else:
        print(f"不支持的操作系统或架构: {system} {arch}")
        return

    download_and_extract(download_url)

if __name__ == "__main__":
    main()
