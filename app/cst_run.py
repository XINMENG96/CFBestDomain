import os
import platform
import subprocess
import time
from dotenv import load_dotenv

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def load_env_variables():
    env_file = os.path.join(get_script_dir(), '..', 'config', 'app.env')
    if os.path.exists(env_file):
        load_dotenv(env_file)
    else:
        print("没有找到 app.env 文件，直接运行 CloudflareST")

# 根据配置构建 CloudflareST 的命令行参数
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

# 运行 CloudflareST
def run_cloudflare_st():
    system = platform.system()
    cloudflare_st_dir = os.path.join(get_script_dir(), '..', 'config', 'CloudflareST_windows_amd64') if system == "Windows" else os.path.join(get_script_dir(), '..', 'config', 'CloudflareST_linux_amd64')
    cst_executable = os.path.join(cloudflare_st_dir, 'CloudflareST.exe') if system == "Windows" else os.path.join(cloudflare_st_dir, 'CloudflareST')

    if not os.path.exists(cst_executable):
        print(f"CloudflareST 可执行文件不存在: {cst_executable}")
        return

    print(f"CloudflareST 可执行文件路径: {cst_executable}")

    cst_command = build_cst_command()

    if not cst_command:
        print(f"没有配置参数，直接运行: {cst_executable}")
        subprocess.Popen([cst_executable], cwd=cloudflare_st_dir)
    else:
        print(f"运行命令: {cst_executable} {' '.join(cst_command)}")
        subprocess.Popen([cst_executable] + cst_command, cwd=cloudflare_st_dir)

    # 检查 result.csv 是否生成
    result_file_path = os.path.join(cloudflare_st_dir, 'result.csv')

    while not os.path.exists(result_file_path):
        print("等待 result.csv 文件生成...")
        time.sleep(2)  # 每隔2秒检查一次

    print("检测到 result.csv 文件，脚本结束。")

def main():
    load_env_variables()
    run_cloudflare_st()

if __name__ == "__main__":
    main()
