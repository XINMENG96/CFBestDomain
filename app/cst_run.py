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
    cst_n = os.getenv('cst_n')
    cst_t = os.getenv('cst_t')
    cst_dn = os.getenv('cst_dn')
    cst_dt = os.getenv('cst_dt')
    cst_tp = os.getenv('cst_tp')
    cst_url = os.getenv('cst_url')
    cst_httping = os.getenv('cst_httping')
    cst_httping_code = os.getenv('cst_httping_code')
    cst_cfcolo = os.getenv('cst_cfcolo')
    cst_tl = os.getenv('cst_tl')
    cst_tll = os.getenv('cst_tll')
    cst_tlr = os.getenv('cst_tlr')
    cst_sl = os.getenv('cst_sl')
    cst_p = os.getenv('cst_p')
    cst_f = os.getenv('cst_f')
    cst_o = os.getenv('cst_o')

    cst_command = ['CloudflareST']

    if cst_n: cst_command.extend(['-n', cst_n])
    if cst_t: cst_command.extend(['-t', cst_t])
    if cst_dn: cst_command.extend(['-dn', cst_dn])
    if cst_dt: cst_command.extend(['-dt', cst_dt])
    if cst_tp: cst_command.extend(['-tp', cst_tp])
    if cst_url: cst_command.extend(['-url', cst_url])
    if cst_httping == 'True': cst_command.append('-httping')
    if cst_httping_code: cst_command.extend(['-httping-code', cst_httping_code])
    if cst_cfcolo: cst_command.extend(['-cfcolo', cst_cfcolo])
    if cst_tl: cst_command.extend(['-tl', cst_tl])
    if cst_tll: cst_command.extend(['-tll', cst_tll])
    if cst_tlr: cst_command.extend(['-tlr', cst_tlr])
    if cst_sl: cst_command.extend(['-sl', cst_sl])
    if cst_p: cst_command.extend(['-p', cst_p])
    if cst_f: cst_command.extend(['-f', cst_f])
    if cst_o: cst_command.extend(['-o', cst_o])

    # Remove the first element if it's the only one, which means no parameters are set
    if len(cst_command) == 1:
        cst_command = []

    return cst_command

# 运行 CloudflareST
def run_cloudflare_st():
    system = platform.system()
    arch = platform.machine()
    
    if system == 'Windows':
        if arch == 'AMD64':
            cloudflare_st_dir = os.path.join(get_script_dir(), 'CloudflareST_windows_amd64')
            cst_executable = os.path.join(cloudflare_st_dir, 'CloudflareST.exe')
        elif arch == 'x86':
            cloudflare_st_dir = os.path.join(get_script_dir(), 'CloudflareST_windows_386')
            cst_executable = os.path.join(cloudflare_st_dir, 'CloudflareST.exe')
        elif arch == 'ARM64':
            cloudflare_st_dir = os.path.join(get_script_dir(), 'CloudflareST_windows_arm64')
            cst_executable = os.path.join(cloudflare_st_dir, 'CloudflareST.exe')
        else:
            print(f"不支持的架构: {arch}")
            return
    elif system == 'Linux':
        if arch == 'x86_64':
            cloudflare_st_dir = os.path.join(get_script_dir(), 'CloudflareST_linux_amd64')
        elif arch == 'x86':
            cloudflare_st_dir = os.path.join(get_script_dir(), 'CloudflareST_linux_386')
        elif arch == 'aarch64':
            cloudflare_st_dir = os.path.join(get_script_dir(), 'CloudflareST_linux_arm64')
        elif arch.startswith('arm'):
            if 'v5' in arch:
                cloudflare_st_dir = os.path.join(get_script_dir(), 'CloudflareST_linux_armv5')
            elif 'v6' in arch:
                cloudflare_st_dir = os.path.join(get_script_dir(), 'CloudflareST_linux_armv6')
            elif 'v7' in arch:
                cloudflare_st_dir = os.path.join(get_script_dir(), 'CloudflareST_linux_armv7')
            else:
                print(f"不支持的 ARM 架构: {arch}")
                return
        elif arch == 'mips':
            cloudflare_st_dir = os.path.join(get_script_dir(), 'CloudflareST_linux_mips')
        elif arch == 'mips64':
            cloudflare_st_dir = os.path.join(get_script_dir(), 'CloudflareST_linux_mips64')
        elif arch == 'mips64le':
            cloudflare_st_dir = os.path.join(get_script_dir(), 'CloudflareST_linux_mips64le')
        elif arch == 'mipsle':
            cloudflare_st_dir = os.path.join(get_script_dir(), 'CloudflareST_linux_mipsle')
        else:
            print(f"不支持的架构: {arch}")
            return
        cst_executable = os.path.join(cloudflare_st_dir, 'CloudflareST')
    elif system == 'Darwin':
        if arch == 'x86_64':
            cloudflare_st_dir = os.path.join(get_script_dir(), 'CloudflareST_darwin_amd64')
        elif arch == 'arm64':
            cloudflare_st_dir = os.path.join(get_script_dir(), 'CloudflareST_darwin_arm64')
        else:
            print(f"不支持的架构: {arch}")
            return
        cst_executable = os.path.join(cloudflare_st_dir, 'CloudflareST')
    else:
        print(f"不支持的操作系统: {system}")
        return

    if not os.path.exists(cst_executable):
        print(f"CloudflareST 可执行文件不存在: {cst_executable}")
        return

    cst_command = build_cst_command()

    if not cst_command:
        print(f"没有配置参数，直接运行: {cst_executable}")
        subprocess.Popen([cst_executable], cwd=cloudflare_st_dir)
    else:
        subprocess.Popen([cst_executable] + cst_command[1:], cwd=cloudflare_st_dir)

    # 检查 result.csv 是否生成
    result_file_path = os.path.join(cloudflare_st_dir, 'result.csv')

    while not os.path.exists(result_file_path):
        time.sleep(2)  # 每隔2秒检查一次

    print("检测到 result.csv 文件，脚本结束。")

def main():
    load_env_variables()
    run_cloudflare_st()

if __name__ == "__main__": 
    main()
