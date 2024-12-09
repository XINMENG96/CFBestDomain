import csv
import ipaddress
import os
import platform
import shlex
import subprocess
import time
import geoip2.database
import requests
from dotenv import load_dotenv

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def load_env_variables():
    env_file = os.path.join(get_script_dir(), '..', 'config', 'app.env')
    if os.path.exists(env_file):
        load_dotenv(env_file)
    else:
        print("没有找到 app.env 文件，直接运行 CloudflareST")

def get_ips():
    cdn = 'cloudflare'  # 固定使用 cloudflare
    countryList = os.getenv('country_list', 'JP,KR,SG,US,HK,None').split(',')
    CloudflareSTDir = os.path.join(get_script_dir(), 'CloudflareST_windows_amd64') if platform.system() == "Windows" else os.path.join(get_script_dir(), 'CloudflareST_linux_amd64')

    print(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()), '获取' + cdn + '最新IP')
    cf_online_url = 'https://api.cloudflare.com/client/v4/ips'
    response = requests.get(cf_online_url, headers={'Content-Type': 'application/json'})
    ips_json_ip = response.json()['result']['ipv4_cidrs']

    ip_list = []
    try:
        os.remove(CloudflareSTDir + '/ip.txt')
        os.remove(CloudflareSTDir + '/result.csv')
    except FileNotFoundError:
        pass
    except Exception as e:
        print(e)

    print(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()), '过滤' + '、'.join(str(x) for x in countryList) + '国家地区IP')
    with geoip2.database.Reader(os.path.join(get_script_dir(), '..', 'config', 'GeoLite2-Country.mmdb')) as reader:
        for ips in ips_json_ip:
            ip = ipaddress.ip_network(ips)[0]
            response = reader.country(ip)
            if response.country.iso_code in countryList:
                ip_list = ip_list + [ips]

    # 更新IP列表至文件
    with open(CloudflareSTDir + '/ip.txt', 'w') as f:
        for ip in ip_list:
            f.write(ip + '\r\n')

def build_cst_command():
    cst_n = os.getenv('cst_n', '200')  # 延迟测速线程
    cst_t = os.getenv('cst_t', '4')    # 延迟测速次数
    cst_dn = os.getenv('cst_dn', '10')  # 下载测速数量
    cst_dt = os.getenv('cst_dt', '10')  # 下载测速时间
    cst_tp = os.getenv('cst_tp', '443')  # 测速端口
    cst_url = os.getenv('cst_url', 'https://cf.xiu2.xyz/url')  # 测速地址
    cst_httping = os.getenv('cst_httping', 'True')  # 是否使用 HTTPing 模式
    cst_httping_code = os.getenv('cst_httping_code', '200')  # HTTPing 有效状态码
    cst_cfcolo = os.getenv('cst_cfcolo', '')  # 匹配指定地区
    cst_tl = os.getenv('cst_tl', '200')  # 平均延迟上限
    cst_tll = os.getenv('cst_tll', '40')  # 平均延迟下限
    cst_tlr = os.getenv('cst_tlr', '0.2')  # 丢包几率上限
    cst_sl = os.getenv('cst_sl', '5')  # 下载速度下限
    cst_p = os.getenv('cst_p', '10')  # 显示结果数量
    cst_f = os.getenv('cst_f', 'ip.txt')  # IP段数据文件
    cst_o = os.getenv('cst_o', 'result.csv')  # 写入结果文件

    cst_command = [
        'CloudflareST',  # 假设 CloudflareST 已经解压
        '-n', cst_n,
        '-t', cst_t,
        '-dn', cst_dn,
        '-dt', cst_dt,
        '-tp', cst_tp,
        '-url', cst_url,
        '-httping' if cst_httping == 'True' else '',
        '-httping-code', cst_httping_code,
        '-cfcolo', cst_cfcolo,
        '-tl', cst_tl,
        '-tll', cst_tll,
        '-tlr', cst_tlr,
        '-sl', cst_sl,
        '-p', cst_p,
        '-f', cst_f,
        '-o', cst_o
    ]
    
    cst_command = [arg for arg in cst_command if arg]
    
    return cst_command

def get_fastest_ip():
    CloudflareSTDir = os.path.join(get_script_dir(), 'CloudflareST_windows_amd64') if platform.system() == "Windows" else os.path.join(get_script_dir(), 'CloudflareST_linux_amd64')
    cst_executable = os.path.join(CloudflareSTDir, 'CloudflareST.exe') if platform.system() == "Windows" else os.path.join(CloudflareSTDir, 'CloudflareST')
    
    if not os.path.exists(cst_executable):
        raise FileNotFoundError(f"CloudflareST 可执行文件不存在: {cst_executable}")

    if platform.system() != "Windows":
        os.chmod(cst_executable, 0o755)

    print(f"可执行文件路径: {cst_executable}")

    stUrl = os.getenv('stUrl', 'https://speed.cloudflare.com/__down?bytes=200000000')
    sturl_none_shell = [cst_executable, '-f', 'ip.txt', '-tl', '150', '-p', '0', '-dd', '-o', 'result.csv']
    sturl_shell = [cst_executable, '-f', 'ip.txt', '-tl', '150', '-p', '0', '-url', stUrl, '-o', 'result.csv']

    print(f"Executing command: {sturl_none_shell if stUrl == 'https://speed.cloudflare.com/__down?bytes=200000000' else sturl_shell}")

    if stUrl == 'https://speed.cloudflare.com/__down?bytes=200000000':
        st = subprocess.Popen(sturl_none_shell, cwd=CloudflareSTDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        st = subprocess.Popen(sturl_shell, cwd=CloudflareSTDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, error = st.communicate()
    st.wait()

def run_cloudflare_st():
    load_env_variables()
    get_ips()
    get_fastest_ip()

def main():
    run_cloudflare_st()

if __name__ == "__main__":
    main()