import json
import os
import sys
from colorama import Fore, Style, init

from config import COUNTRY_CODES, OUTPUT_FILE
from fetcher import fetch_jobs
from exporter import export_to_csv

init(autoreset=True)

PREFS_FILE = os.path.join(os.path.dirname(__file__), "preferences.json")


def save_preferences(keyword, country_code, country_name, location):
    data = {
        "keyword": keyword,
        "country_code": country_code,
        "country_name": country_name,
        "location": location,
    }
    with open(PREFS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_preferences():
    if not os.path.exists(PREFS_FILE):
        return None
    try:
        with open(PREFS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def print_banner():
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + "       Job Listings Fetcher  (Adzuna)")
    print(Fore.CYAN + "=" * 50)


def select_country():
    print(Fore.YELLOW + "\nAvailable Countries:")
    for num, (name, _) in COUNTRY_CODES.items():
        print(f"  {num:>2}. {name}")

    while True:
        choice = input(Fore.WHITE + "\nEnter country number: ").strip()
        if choice in COUNTRY_CODES:
            return COUNTRY_CODES[choice]  # (country_name, country_code)
        print(Fore.RED + "  Invalid choice. Try again.")


def run_search(keyword=None, country_code=None, country_name=None, location=None, silent=False):
    """
    Core search logic. Called by both manual (main) and scheduler modes.
    When called from scheduler, keyword/country_code/country_name/location are passed directly.
    """
    if keyword is None:
        print_banner()

        # Show last preferences if available
        prefs = load_preferences()
        if prefs:
            print(Fore.CYAN + f"\nLast search: \"{prefs['keyword']}\" in {prefs['country_name']}"
                  + (f", {prefs['location']}" if prefs.get("location") else ""))
            reuse = input(Fore.WHITE + "Reuse last search? (y/n): ").strip().lower()
            if reuse == "y":
                keyword = prefs["keyword"]
                country_code = prefs["country_code"]
                country_name = prefs["country_name"]
                location = prefs.get("location", "")

        if keyword is None:
            keyword = input(Fore.WHITE + "\nJob title / keyword: ").strip()
            if not keyword:
                print(Fore.RED + "Keyword cannot be empty.")
                sys.exit(1)

            country_name, country_code = select_country()
            location = input(Fore.WHITE + "City / Location (press Enter to skip): ").strip()
            save_preferences(keyword, country_code, country_name, location)

    if not silent:
        print(Fore.GREEN + f"\nSearching: \"{keyword}\" | Country: {country_name}"
              + (f" | Location: {location}" if location else ""))
        print(Fore.GREEN + "-" * 50)

    jobs = fetch_jobs(keyword, country_code, location)

    if not jobs:
        if not silent:
            print(Fore.RED + "\nNo jobs found. Try a different keyword or location.")
        return 0

    new_count, skipped_count = export_to_csv(jobs)

    if not silent:
        print(Fore.GREEN + "-" * 50)
        print(Fore.CYAN + f"\n  Total fetched  : {len(jobs)}")
        print(Fore.GREEN + f"  New saved      : {new_count}")
        print(Fore.YELLOW + f"  Duplicates skipped: {skipped_count}")
        print(Fore.CYAN + f"  Output file    : {os.path.abspath(OUTPUT_FILE)}")
        print(Fore.CYAN + "\n  Open jobs.csv in Excel or Google Sheets (File > Import > CSV)")

    return new_count


if __name__ == "__main__":
    run_search()
