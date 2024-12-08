import subprocess
import sys
import os
import time
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
def load_env_variables():
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "app.env")
    if os.path.exists(env_file):
        load_dotenv(env_file)
    else:
        print("Warning: app.env file not found. Using default configuration.")

# Get task execution interval in seconds
def get_interval():
    try:
        interval_minutes = os.getenv("INTERVAL_MINUTES", None)
        if interval_minutes is not None:
            return int(interval_minutes) * 60  # Convert to seconds
        return None
    except ValueError:
        print("Invalid INTERVAL_MINUTES value in .env file. Defaulting to single execution.")
        return None

# Run a script
def run_script(script_name):
    try:
        subprocess.check_call([sys.executable, script_name])
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        sys.exit(1)

# Main workflow
def main():
    print("Starting the workflow...")

    # Step 1: Run cst_dl.py to download CloudflareST
    print("Step 1: Downloading CloudflareST...")
    run_script(os.path.join("app", "cst_dl.py"))

    # Step 2: Check if result.csv is recent
    print("Step 2: Checking result.csv...")
    check_csv_script = os.path.join("app", "check_csv.py")
    try:
        subprocess.check_call([sys.executable, check_csv_script])
        print("result.csv is up-to-date. Terminating workflow.")
        return  # Exit if CSV is recent
    except subprocess.CalledProcessError:
        print("result.csv is outdated. Proceeding with workflow...")

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
    """Output the next run time"""
    next_run_time = datetime.now() + timedelta(seconds=interval)
    print(f"Next run time: {next_run_time.strftime('%Y/%m/%d %H:%M')}")

if __name__ == "__main__":
    # Load environment variables
    load_env_variables()

    # Get task interval in seconds
    interval = get_interval()

    if interval:
        print(f"Running every {interval // 60} minutes")
        # Loop to execute the task at intervals
        while True:
            main()
            display_next_run_time(interval)
            print(f"Sleeping for {interval // 60} minutes until the next execution...")
            time.sleep(interval)
    else:
        print("Running a single task")
        main()
