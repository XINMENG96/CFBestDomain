import subprocess
import sys
import os
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta

# 加载环境变量
def load_env_variables():
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "app.env")
    if os.path.exists(env_file):
        load_dotenv(env_file)
    else:
        print("Warning: app.env file not found. Using default configuration.")

# 获取任务执行间隔时间（单位：秒）
def get_interval():
    try:
        interval_minutes = os.getenv("INTERVAL_MINUTES", None)
        if interval_minutes is not None:
            return int(interval_minutes) * 60  # 转换为秒
        return None
    except ValueError:
        print("Invalid INTERVAL_MINUTES value in .env file. Defaulting to single execution.")
        return None

# 执行子脚本
def run_script(script_name):
    try:
        subprocess.check_call([sys.executable, script_name])
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        sys.exit(1)

# 主流程
def main():
    print("Starting the workflow...")

    # Step 1: Check if result.csv is recent
    print("Step 1: Checking result.csv...")
    check_csv_script = os.path.join("app", "check_csv.py")
    try:
        subprocess.check_call([sys.executable, check_csv_script])
        print("result.csv is up-to-date. Terminating workflow.")
        return  # Exit if CSV is recent
    except subprocess.CalledProcessError:
        print("result.csv is outdated. Proceeding with workflow...")

    # Step 2: Download CloudflareST
    print("Step 2: Downloading CloudflareST...")
    run_script(os.path.join("app", "cst_dl.py"))

    # Step 3: Generate app.env if it doesn't exist
    print("Step 3: Generating app.env...")
    run_script(os.path.join("app", "gen_env.py"))

    # Step 4: Run CloudflareST
    print("Step 4: Running CloudflareST...")
    run_script(os.path.join("app", "cst_run.py"))

    # Step 5: Update DNS records
    print("Step 5: Updating DNS records...")
    run_script(os.path.join("app", "dns_refresh.py"))

    print("Workflow completed successfully.")

def display_next_run_time(interval):
    """输出下次运行的时间"""
    next_run_time = datetime.now() + timedelta(seconds=interval)
    print(f"Next run time: {next_run_time.strftime('%Y/%m/%d %H:%M')}")

if __name__ == "__main__":
    # 加载环境变量
    load_env_variables()

    # 获取任务间隔时间（秒）
    interval = get_interval()

    if interval:
        print(f"每{interval // 60}分钟运行一次")
        # 按间隔时间循环执行任务
        while True:
            main()
            display_next_run_time(interval)
            print(f"Sleeping for {interval // 60} minutes until the next execution...")
            time.sleep(interval)
    else:
        print("将只执行一次任务")
        main()
