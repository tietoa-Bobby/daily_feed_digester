import argparse
import sys
import os
import yaml
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from modules.aggregator import aggregate_all_sources
from modules.summarizer import summarise_posts
from modules.notifier import send_digest


def load_config(config_path):
    if not os.path.exists(config_path):
        example_path = config_path.replace('.yaml', '.example.yaml')
        if os.path.exists(example_path):
            with open(example_path, 'r') as src, open(config_path, 'w') as dst:
                dst.write(src.read())
            print(f"[Daily Feed Digester] '{config_path}' not found. Created from '{example_path}'. Please edit it with your details and run again.")
            sys.exit(1)
        else:
            print(f"[Daily Feed Digester] '{config_path}' not found and no example config available. Please create it manually.")
            sys.exit(1)
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def run_digest(config):
    posts = aggregate_all_sources(config)
    summary = summarise_posts(posts)
    send_digest(summary, config)


def main():
    parser = argparse.ArgumentParser(description="Daily Feed Digester")
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to config file')
    parser.add_argument('--run-now', action='store_true', help='Run the digest immediately and exit')
    args = parser.parse_args()
    config = load_config(args.config)

    if args.run_now:
        run_digest(config)
        sys.exit(0)

    schedule_cfg = config.get('schedule', {})
    hour = schedule_cfg.get('hour', 8)
    minute = schedule_cfg.get('minute', 0)
    timezone = schedule_cfg.get('timezone', 'UTC')

    scheduler = BackgroundScheduler(timezone=timezone)
    scheduler.add_job(lambda: run_digest(config), 'cron', hour=hour, minute=minute)
    scheduler.start()

    print(f"[Daily Feed Digester] Scheduled digest at {hour:02d}:{minute:02d} {timezone}. Press Ctrl+C to exit.")
    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("\n[Daily Feed Digester] Exiting.")


if __name__ == "__main__":
    main() 