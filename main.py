import subprocess
import sys
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import platform
from croniter import croniter

# Load environment variables
def load_env_variables():
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "app.env")
    if (os.path.exists(env_file)):
        load_dotenv(env_file)
    else:
        print("警告: app.env 文件未找到。使用默认配置。")

# Get interval in seconds from INTERVAL_MINUTES
def get_interval():
    try:
        interval_minutes = os.getenv("INTERVAL_MINUTES", None)
        if (interval_minutes is not None):
            interval = int(interval_minutes) * 60  # Convert to seconds
            print(f"任务间隔时间（秒）: {interval}")
            return interval
        return None
    except ValueError:
        print("无效的 INTERVAL_MINUTES 值在 .env 文件中。默认单次执行。")
        return None

# Execute sub-script
def run_script(script_name):
    try:
        subprocess.check_call([sys.executable, script_name])
    except subprocess.CalledProcessError as e:
        print(f"运行 {script_name} 时出错: {e}")
        sys.exit(1)

# Schedule tasks based on cron expression
def schedule_task(cron_expr):
    base_time = datetime.now()
    iter = croniter(cron_expr, base_time)
    next_run = iter.get_next(datetime)
    
    # Immediately execute once
    main()
    display_next_run_time(next_run)
    
    # Continue to run according to the CRON_EXPR
    while True:
        now = datetime.now()
        if (now >= next_run):
            main()
            next_run = iter.get_next(datetime)
            display_next_run_time(next_run)
        time.sleep(1)

# Main workflow
def main():
    print("开始工作流...")

    # Step 1: Check if result.csv is recent
    print("步骤 1: 检查 result.csv...")
    check_csv_script = os.path.join("app", "check_csv.py")
    try:
        subprocess.check_call([sys.executable, check_csv_script])
        print("result.csv 是最新的。终止工作流。")
        return  # Exit if CSV is recent
    except subprocess.CalledProcessError:
        print("result.csv 已过期。继续工作流...")

    # Step 2: Download CloudflareST
    print("步骤 2: 下载 CloudflareST...")
    run_script(os.path.join("app", "cst_dl.py"))

    # Step 3: Generate app.env if it doesn't exist
    print("步骤 3: 生成 app.env...")
    run_script(os.path.join("app", "gen_env.py"))

    # Step 4: Run CloudflareST
    print("步骤 4: 运行 CloudflareST...")
    run_script(os.path.join("app", "cst_run.py"))

    # Step 5: Update DNS records
    print("步骤 5: 更新 DNS 记录...")
    run_script(os.path.join("app", "dns_refresh.py"))

    print("工作流成功完成。")

def display_next_run_time(next_run_time):
    """显示下次运行时间"""
    print(f"下次运行时间: {next_run_time.strftime('%Y/%m/%d %H:%M')}")

if __name__ == "__main__":
    # Load environment variables
    load_env_variables()

    # Get the cron expression
    cron_expr = os.getenv("CRON_EXPR", None)

    if (platform.system() == 'Windows'):
        # Get interval in seconds from INTERVAL_MINUTES
        interval = get_interval()

        if (interval):
            print(f"每 {interval // 60} 分钟运行一次")
            # Execute tasks at the specified interval
            while True:
                main()
                next_run_time = datetime.now() + timedelta(seconds=interval)
                display_next_run_time(next_run_time)
                print(f"休眠 {interval // 60} 分钟直到下次执行...")
                time.sleep(interval)
        else:
            print("将只执行任务一次")
            main()
    else:
        # For Linux, prioritize CRON_EXPR over INTERVAL_MINUTES
        if (cron_expr):
            print(f"使用 cron 表达式调度任务: {cron_expr}")
            schedule_task(cron_expr)
        else:
            # Get interval in seconds from INTERVAL_MINUTES
            interval = get_interval()

            if (interval):
                print(f"每 {interval // 60} 分钟运行一次")
                # Execute tasks at the specified interval
                while True:
                    main()
                    next_run_time = datetime.now() + timedelta(seconds=interval)
                    display_next_run_time(next_run_time)
                    print(f"休眠 {interval // 60} 分钟直到下次执行...")
                    time.sleep(interval)
            else:
                print("将只执行任务一次")
                main()