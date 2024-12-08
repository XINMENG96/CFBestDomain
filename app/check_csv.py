import os
import sys
import platform
from datetime import datetime, timedelta


def is_file_recent(file_path, max_age_minutes=30):
    """Check if a file is created/modified within the last `max_age_minutes`."""
    if os.path.exists(file_path):
        file_mod_time = os.path.getmtime(file_path)
        file_mod_datetime = datetime.fromtimestamp(file_mod_time)
        if datetime.now() - file_mod_datetime < timedelta(minutes=max_age_minutes):
            return True
    return False

# 获取脚本目录并指定历史记录文件的路径
def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def main():
    csv_path = os.path.join(get_script_dir(), 'CloudflareST_windows_amd64', 'result.csv') if platform.system() == "Windows" else os.path.join(get_script_dir(), 'config', 'CloudflareST_linux_amd64', 'result.csv')
    if is_file_recent(csv_path):
        print(f"{csv_path} is up-to-date.")
        sys.exit(0)  # Exit with status 0 (indicates success)
    else:
        print(f"{csv_path} is outdated.")
        sys.exit(1)  # Exit with status 1 (indicates failure)


if __name__ == "__main__":
    main()
