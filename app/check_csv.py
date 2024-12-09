import os
import sys
from datetime import datetime, timedelta

def get_script_dir():
    """Get the directory of the current script."""
    return os.path.dirname(os.path.abspath(__file__))

def is_file_recent(file_path, max_age_minutes=30):
    """Check if a file is created/modified within the last `max_age_minutes`."""
    if os.path.exists(file_path):
        file_mod_time = os.path.getmtime(file_path)
        file_mod_datetime = datetime.fromtimestamp(file_mod_time)
        if datetime.now() - file_mod_datetime < timedelta(minutes=max_age_minutes):
            return True
    return False

def main():
    # 使用 get_script_dir 来构建文件路径
    history_file = os.path.join(get_script_dir(), '..', 'config', 'dns_history.csv')
    if is_file_recent(history_file):
        print(f"{history_file} is up-to-date.")
        sys.exit(0)  # Exit with status 0 (indicates success)
    else:
        print(f"{history_file} is outdated.")
        sys.exit(1)  # Exit with status 1 (indicates failure)

if __name__ == "__main__":
    main()
