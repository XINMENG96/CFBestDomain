import subprocess
import sys
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import schedule
import platform
from croniter import croniter

# 加载环境变量
def load_env_variables():
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "app.env")
    if os.path.exists(env_file):
        load_dotenv(env_file)
    else:
        print("警告: app.env 文件未找到。使用默认配置。")

# 从 INTERVAL_MINUTES 获取间隔时间（秒）
def get_interval():
    try:
        interval_minutes = os.getenv("INTERVAL_MINUTES", None)
        if interval_minutes is not None:
            interval = int(interval_minutes) * 60  # 转换为秒
            print(f"任务间隔时间（秒）: {interval}")
            return interval
        return None
    except ValueError:
        print("无效的 INTERVAL_MINUTES 值在 .env 文件中。默认单次执行。")
        return None

# 执行子脚本
def run_script(script_name):
    try:
        subprocess.check_call([sys.executable, script_name])
    except subprocess.CalledProcessError as e:
        print(f"运行 {script_name} 时出错: {e}")
        sys.exit(1)

# 基于 cron 表达式调度任务
def schedule_task(cron_expr):
    base_time = datetime.now()
    iter = croniter(cron_expr, base_time)
    next_run = iter.get_next(datetime)
    while True:
        now = datetime.now()
        if now >= next_run:
            main()
            next_run = iter.get_next(datetime)
        time.sleep(1)

# 主工作流
def main():
    print("开始工作流...")

    # 步骤 1: 检查 result.csv 是否是最新的
    print("步骤 1: 检查 result.csv...")
    check_csv_script = os.path.join("app", "check_csv.py")
    try:
        subprocess.check_call([sys.executable, check_csv_script])
        print("result.csv 是最新的。终止工作流。")
        return  # 如果 CSV 是最新的则退出
    except subprocess.CalledProcessError:
        print("result.csv 已过期。继续工作流...")

    # 步骤 2: 下载 CloudflareST
    print("步骤 2: 下载 CloudflareST...")
    run_script(os.path.join("app", "cst_dl.py"))

    # 步骤 3: 如果不存在则生成 app.env
    print("步骤 3: 生成 app.env...")
    run_script(os.path.join("app", "gen_env.py"))

    # 步骤 4: 运行 CloudflareST
    print("步骤 4: 运行 CloudflareST...")
    run_script(os.path.join("app", "cst_run.py"))

    # 步骤 5: 更新 DNS 记录
    print("步骤 5: 更新 DNS 记录...")
    run_script(os.path.join("app", "dns_refresh.py"))

    print("工作流成功完成。")

def display_next_run_time(interval):
    """显示下次运行时间"""
    next_run_time = datetime.now() + timedelta(seconds=interval)
    print(f"下次运行时间: {next_run_time.strftime('%Y/%m/%d %H:%M')}")

if __name__ == "__main__":
    # 加载环境变量
    load_env_variables()

    # 获取 cron 表达式
    cron_expr = os.getenv("CRON_EXPR", None)

    if platform.system() == 'Windows':
        # 从 INTERVAL_MINUTES 获取间隔时间（秒）
        interval = get_interval()

        if interval:
            print(f"每 {interval // 60} 分钟运行一次")
            # 按指定间隔执行任务
            while True:
                main()
                display_next_run_time(interval)
                print(f"休眠 {interval // 60} 分钟直到下次执行...")
                time.sleep(interval)
        else:
            print("将只执行任务一次")
            main()
    else:
        # 对于 Linux，优先使用 CRON_EXPR 而不是 INTERVAL_MINUTES
        if cron_expr:
            print(f"使用 cron 表达式调度任务: {cron_expr}")
            schedule_task(cron_expr)
        else:
            # 从 INTERVAL_MINUTES 获取间隔时间（秒）
            interval = get_interval()

            if interval:
                print(f"每 {interval // 60} 分钟运行一次")
                # 按指定间隔执行任务
                while True:
                    main()
                    display_next_run_time(interval)
                    print(f"休眠 {interval // 60} 分钟直到下次执行...")
                    time.sleep(interval)
            else:
                print("将只执行任务一次")
                main()