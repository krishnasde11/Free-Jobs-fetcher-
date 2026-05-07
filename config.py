import os
from dotenv import load_dotenv

load_dotenv()

APP_ID  = os.getenv("ADZUNA_APP_ID", "")
APP_KEY = os.getenv("ADZUNA_APP_KEY", "")

if not APP_ID or not APP_KEY:
    raise EnvironmentError(
        "Missing API keys.\n"
        "Copy .env.example to .env and fill in your ADZUNA_APP_ID and ADZUNA_APP_KEY.\n"
        "Get free keys at: https://developer.adzuna.com/"
    )

# Scheduler settings
SCHEDULE_TIME = "08:00"       # Daily fetch time (24hr format)
MAX_PAGES = 10                 # Pages per search (50 jobs/page = 500 jobs max per run)
OUTPUT_FILE = "jobs.csv"       # All results append to this single file

COUNTRY_CODES = {
    "1":  ("United States",   "us"),
    "2":  ("United Kingdom",  "gb"),
    "3":  ("India",           "in"),
    "4":  ("Canada",          "ca"),
    "5":  ("Australia",       "au"),
    "6":  ("Germany",         "de"),
    "7":  ("France",          "fr"),
    "8":  ("Netherlands",     "nl"),
    "9":  ("Singapore",       "sg"),
    "10": ("South Africa",    "za"),
    "11": ("New Zealand",     "nz"),
    "12": ("Poland",          "pl"),
    "13": ("Brazil",          "br"),
    "14": ("Mexico",          "mx"),
    "15": ("Austria",         "at"),
    "16": ("Belgium",         "be"),
    "17": ("Switzerland",     "ch"),
}
