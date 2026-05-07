"""
scheduler.py — Run this once to start the daily auto-fetch.
It reads your saved preferences (from last manual run) and fetches
new jobs every day at the time set in config.py (default 08:00).

Keep this running in a terminal or set it up as a Windows startup task.
"""

import schedule
import time
import os
import json
from datetime import datetime
from colorama import Fore, Style, init

from config import SCHEDULE_TIME
from main import run_search, load_preferences, PREFS_FILE

init(autoreset=True)


def scheduled_run():
    prefs = load_preferences()
    if not prefs:
        print(Fore.RED + f"[{datetime.now():%Y-%m-%d %H:%M}] No saved preferences found.")
        print(Fore.YELLOW + "  Run main.py first to perform a manual search and save your preferences.")
        return

    keyword = prefs["keyword"]
    country_code = prefs["country_code"]
    country_name = prefs["country_name"]
    location = prefs.get("location", "")

    print(Fore.CYAN + f"\n[{datetime.now():%Y-%m-%d %H:%M}] Scheduled fetch started")
    print(Fore.CYAN + f"  Keyword : {keyword}")
    print(Fore.CYAN + f"  Country : {country_name}")
    if location:
        print(Fore.CYAN + f"  Location: {location}")

    new_count = run_search(
        keyword=keyword,
        country_code=country_code,
        country_name=country_name,
        location=location,
        silent=True,
    )

    print(Fore.GREEN + f"[{datetime.now():%Y-%m-%d %H:%M}] Done — {new_count} new jobs saved.")


def main():
    prefs = load_preferences()

    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + "   Job Scheduler — Daily Auto-Fetch")
    print(Fore.CYAN + "=" * 50)

    if prefs:
        print(Fore.GREEN + f"\n  Saved search  : \"{prefs['keyword']}\" in {prefs['country_name']}"
              + (f", {prefs['location']}" if prefs.get("location") else ""))
    else:
        print(Fore.YELLOW + "\n  No saved preferences found.")
        print(Fore.YELLOW + "  Run main.py first, then start the scheduler.")
        return

    print(Fore.CYAN + f"\n  Scheduled time : {SCHEDULE_TIME} daily")
    print(Fore.CYAN + "  Keep this window open to let the scheduler run.")
    print(Fore.YELLOW + "\n  Press Ctrl+C to stop.\n")

    schedule.every().day.at(SCHEDULE_TIME).do(scheduled_run)

    # Also run immediately on start so you get results right away
    run_now = input(Fore.WHITE + "Fetch jobs now as well? (y/n): ").strip().lower()
    if run_now == "y":
        scheduled_run()

    print(Fore.GREEN + f"\nScheduler running. Next auto-fetch at {SCHEDULE_TIME}...\n")

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\nScheduler stopped.")
