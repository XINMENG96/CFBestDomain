import csv
import os
import platform
import requests
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 获取脚本目录并指定历史记录文件的路径
def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

# 读取 .env 文件并加载环境变量
def load_env_variables():
    env_file = os.path.join(get_script_dir(), '..', 'config', 'app.env')
    if os.path.exists(env_file):
        load_dotenv(env_file)
        print("zone_id:", os.getenv('zone_id'))  # 调试输出
        print("email:", os.getenv('email'))  # 调试输出
        print("api_key:", os.getenv('api_key'))  # 调试输出
        print("record_name:", os.getenv('record_name'))  # 调试输出
    else:
        print("没有找到 app.env 文件，直接运行 CloudflareST")

# 获取 Cloudflare DNS 记录 ID
def get_dns_record_id():
    dns_record_id = os.getenv('zone_id')  # 使用 app.env 中的变量
    if not dns_record_id:
        print("未找到 zone_id 配置，请检查 app.env 文件。")
        return None
    return dns_record_id

# 更新 DNS 记录
def update_dns_record(ip):
    dns_record_id = get_dns_record_id()
    if dns_record_id:
        url = f'https://api.cloudflare.com/client/v4/zones/{dns_record_id}/dns_records/{dns_record_id}'
        headers = {
            'X-Auth-Email': os.getenv('email'),  # 使用 app.env 中的邮箱配置
            'X-Auth-Key': os.getenv('api_key'),  # 使用 app.env 中的 API 密钥
            'Content-Type': 'application/json'
        }
        data = {
            'type': 'A',
            'name': os.getenv('record_name'),
            'content': ip,
            'ttl': 120,
            'proxied': False
        }
        response = requests.put(url, json=data, headers=headers)
        if response.status_code == 200:
            print(f"DNS 记录更新成功: {ip}")
        else:
            print(f"更新 DNS 记录失败: {response.text}")
    else:
        print("未找到 DNS 记录 ID")

# 处理 CSV 文件并返回有效 IP 地址列表
def process_csv(file_path):
    valid_ips = []

    # 获取下载速度阈值，默认值为 10
    download_speed_threshold = float(os.getenv('cst_download_speed_threshold', 10))

    # 使用 utf-8 编码打开 CSV 文件
    with open(file_path, 'r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            ip_address = row['IP 地址']
            download_speed = float(row['下载速度 (MB/s)'])  # 转换为浮动数值
            if download_speed >= download_speed_threshold:
                valid_ips.append(ip_address)
                print(f"找到有效 IP: {ip_address}，下载速度 {download_speed}MB/s")
            else:
                print(f"跳过 IP {ip_address}，下载速度 {download_speed}MB/s 小于 {download_speed_threshold}")
    
    # 执行 DNS 更新
    update_dns_records(valid_ips)

# 从历史文件中读取记录时间
def get_last_updated(ip):
    history_file = os.path.join(get_script_dir(), '..', 'config', 'dns_history.csv')
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                if row['IP 地址'] == ip:
                    return datetime.strptime(row['更新时间'], '%Y-%m-%d %H:%M:%S')
    return None

# 更新本地历史记录
def update_history(ip):
    history_file = os.path.join(get_script_dir(), '..', 'config', 'dns_history.csv')
    
    with open(history_file, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # 如果历史记录文件为空，则写入标题
        if os.stat(history_file).st_size == 0:
            writer.writerow(['IP 地址', '更新时间'])
        # 添加当前时间的解析记录
        writer.writerow([ip, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

# 更新 DNS 记录
def update_dns_records(csv_ips):
    dns_records = get_dns_records()
    if dns_records:
        # 获取当前所有 'cdn1.decastar.us.kg' 的 IP 地址
        current_ips = [record['content'] for record in dns_records if record['name'] == os.getenv('record_name')]

        # 删除现有记录中不在 CSV 中的 IP 地址，且解析时间超过 3 天
        for ip in current_ips:
            if ip not in csv_ips:
                # 从历史记录中获取解析时间
                last_updated = get_last_updated(ip)
                if last_updated and (datetime.now() - last_updated).days >= 3:
                    print(f"删除当前 DNS 记录 IP: {ip}，因为它不在 CSV 中的有效 IP 列表中且已经解析超过 3 天")
                    record_id = next(record['id'] for record in dns_records if record['content'] == ip)
                    delete_dns_record(record_id)

        # 添加 CSV 中的新 IP 地址
        for ip in csv_ips:
            if ip not in current_ips:
                print(f"添加新的 DNS 记录: {ip}")
                create_dns_record(ip)
                update_history(ip)

        # 检查当前解析的 IP 数量是否超过 10 个，超过则从旧的开始删除
        if len(current_ips) > 10:
            sorted_ips = sorted(current_ips, key=lambda ip: get_last_updated(ip) or datetime.min)
            for ip in sorted_ips[:-10]:
                print(f"删除旧的 DNS 记录 IP: {ip}，已解析 IP 数量超过 10 个")
                record_id = next(record['id'] for record in dns_records if record['content'] == ip)
                delete_dns_record(record_id)

# 获取 Cloudflare DNS 记录
def get_dns_records():
    dns_record_id = get_dns_record_id()
    if not dns_record_id:
        return []
    
    url = f'https://api.cloudflare.com/client/v4/zones/{dns_record_id}/dns_records'
    headers = {
        'X-Auth-Email': os.getenv('email'),
        'X-Auth-Key': os.getenv('api_key'),
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['result']
    else:
        print(f"获取 DNS 记录失败: {response.status_code} {response.text}")
    return []

# 删除 DNS 记录
def delete_dns_record(record_id):
    url = f'https://api.cloudflare.com/client/v4/zones/{get_dns_record_id()}/dns_records/{record_id}'
    headers = {
        'X-Auth-Email': os.getenv('email'),
        'X-Auth-Key': os.getenv('api_key'),
        'Content-Type': 'application/json'
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print(f"DNS 记录删除成功")
    else:
        print(f"删除 DNS 记录失败: {response.text}")

# 创建新的 DNS 记录
def create_dns_record(ip):
    url = f'https://api.cloudflare.com/client/v4/zones/{get_dns_record_id()}/dns_records'
    headers = {
        'X-Auth-Email': os.getenv('email'),
        'X-Auth-Key': os.getenv('api_key'),
        'Content-Type': 'application/json'
    }
    data = {
        'type': 'A',
        'name': os.getenv('record_name'),
        'content': ip,
        'ttl': 120,
        'proxied': False
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"DNS 记录创建成功: {ip}")
    else:
        print(f"创建 DNS 记录失败: {response.text}")

# 获取 CloudflareST 结果文件的路径
def get_result_csv_path():
    system = platform.system()
    arch = platform.machine()
    
    if system == 'Windows':
        if arch == 'AMD64':
            return os.path.join(get_script_dir(), 'CloudflareST_windows_amd64', 'result.csv')
        elif arch == 'x86':
            return os.path.join(get_script_dir(), 'CloudflareST_windows_386', 'result.csv')
        elif arch == 'ARM64':
            return os.path.join(get_script_dir(), 'CloudflareST_windows_arm64', 'result.csv')
    elif system == 'Linux':
        if arch == 'x86_64':
            return os.path.join(get_script_dir(), 'CloudflareST_linux_amd64', 'result.csv')
        elif arch == 'x86':
            return os.path.join(get_script_dir(), 'CloudflareST_linux_386', 'result.csv')
        elif arch == 'aarch64':
            return os.path.join(get_script_dir(), 'CloudflareST_linux_arm64', 'result.csv')
        elif arch.startswith('arm'):
            if 'v5' in arch:
                return os.path.join(get_script_dir(), 'CloudflareST_linux_armv5', 'result.csv')
            elif 'v6' in arch:
                return os.path.join(get_script_dir(), 'CloudflareST_linux_armv6', 'result.csv')
            elif 'v7' in arch:
                return os.path.join(get_script_dir(), 'CloudflareST_linux_armv7', 'result.csv')
        elif arch == 'mips':
            return os.path.join(get_script_dir(), 'CloudflareST_linux_mips', 'result.csv')
        elif arch == 'mips64':
            return os.path.join(get_script_dir(), 'CloudflareST_linux_mips64', 'result.csv')
        elif arch == 'mips64le':
            return os.path.join(get_script_dir(), 'CloudflareST_linux_mips64le', 'result.csv')
        elif arch == 'mipsle':
            return os.path.join(get_script_dir(), 'CloudflareST_linux_mipsle', 'result.csv')
    elif system == 'Darwin':
        if arch == 'x86_64':
            return os.path.join(get_script_dir(), 'CloudflareST_darwin_amd64', 'result.csv')
        elif arch == 'arm64':
            return os.path.join(get_script_dir(), 'CloudflareST_darwin_arm64', 'result.csv')
    return None

def main():
    # 加载环境变量
    load_env_variables()

    # 获取 result.csv 文件路径
    file_path = get_result_csv_path()
    
    if file_path and os.path.exists(file_path):
        print(f"找到文件: {file_path}")
        process_csv(file_path)
    else:
        print("未找到 result.csv 文件，请确保 CloudflareSpeedTest 正常运行")

if __name__ == '__main__':
    main()
