import os
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

def build_cst_command():
    cst_n = os.getenv('cst_n', '200')
    cst_t = os.getenv('cst_t', '4')
    cst_dn = os.getenv('cst_dn', '10')
    cst_dt = os.getenv('cst_dt', '10')
    cst_tp = os.getenv('cst_tp', '443')
    cst_url = os.getenv('cst_url', 'https://cf.xiu2.xyz/url')
    cst_httping = os.getenv('cst_httping', 'True')
    cst_httping_code = os.getenv('cst_httping_code', '200')
    cst_cfcolo = os.getenv('cst_cfcolo', '')
    cst_tl = os.getenv('cst_tl', '200')
    cst_tll = os.getenv('cst_tll', '40')
    cst_tlr = os.getenv('cst_tlr', '0.2')
    cst_sl = os.getenv('cst_sl', '5')
    cst_p = os.getenv('cst_p', '10')
    cst_f = os.getenv('cst_f', 'ip.txt')
    cst_o = os.getenv('cst_o', 'result.csv')

    cst_command = [
        'CloudflareST',
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

    return [arg for arg in cst_command if arg]

def run_cloudflare_st():
    cloudflare_st_dir = os.path.join(get_script_dir(), '..', 'config')
    cst_executable = os.path.join(cloudflare_st_dir, 'CloudflareST')

    if not os.path.exists(cst_executable):
        print(f"CloudflareST 可执行文件不存在: {cst_executable}")
        return

    print(f"CloudflareST 可执行文件路径: {cst_executable}")

    cst_command = build_cst_command()
    subprocess.Popen([cst_executable] + cst_command, cwd=cloudflare_st_dir)

    result_file_path = os.path.join(cloudflare_st_dir, 'result.csv')

    while not os.path.exists(result_file_path):
        print("等待 result.csv 文件生成...")
        time.sleep(2)

    print("检测到 result.csv 文件，脚本结束。")

def main():
    load_env_variables()
    run_cloudflare_st()

if __name__ == "__main__":
    main()