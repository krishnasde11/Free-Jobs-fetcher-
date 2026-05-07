# Job Listings Fetcher

A powerful and automated python tool to fetch, manage, and export job listings directly from the **Adzuna API**. 

This application allows you to search for jobs by title/keyword, country, and city, automatically handles pagination to gather hundreds of jobs at once, skips duplicate listings, and exports clean data to a CSV file. It even includes a daily scheduler to automate your job hunt!

## Features

- **Global Search:** Search jobs across 17+ countries using Adzuna.
- **Bulk Fetching:** Automatically paginates through results (up to 500 jobs per run).
- **Duplicate Prevention:** Keeps track of "Job IDs" you've already saved and ensures no duplicate rows are added to your CSV.
- **Interactive UI:** Provides a clean command-line interface, plus a native Windows popup dialog to easily choose where your exported CSV gets saved.
- **Smart Preferences:** Remembers your last search (keyword, location, country, and output folder) so you don't have to type it every time.
- **Daily Automation (Scheduler):** Run the `scheduler.py` script in the background to automatically fetch the newest jobs matching your preferences every single day at a specified time!

## Setup and Installation

1. **Clone the repository** (or download the files).
2. **Install dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```
3. **Get an Adzuna API Key:**
   - Go to [Adzuna Developer Portal](https://developer.adzuna.com/) and create a free account.
   - Get your unique `APP_ID` and `APP_KEY`.
4. **Configure your environment variables:**
   - Create a file named `.env` in the root directory.
   - Add your keys into the `.env` file like this:
     ```env
     ADZUNA_APP_ID=your_app_id_here
     ADZUNA_APP_KEY=your_app_key_here
     ```
     *(Note: Your `.env` file is safely ignored by Git to prevent security issues).*

## How to Use

### 1. Manual Search (`main.py`)
Run the main script to start fetching jobs interactively:
```bash
python main.py
```
- The app will prompt you for a job keyword, country, and optional city.
- A popup folder selection dialog will appear—choose where you want to save `jobs.csv`.
- The tool will pull down all jobs, filter duplicates, and append them to your CSV!

### 2. Daily Automation (`scheduler.py`)
Once you have run `main.py` at least once (which saves your preferences), you can start the scheduler:
```bash
python scheduler.py
```
- This will keep a background process running that fetches fresh jobs at a set time every day (default is `08:00`, which you can change in `config.py`).
- All new jobs will seamlessly append to the exact folder you selected previously.

## Configuration

If you'd like to tweak some default behavior, you can open `config.py`:
- `SCHEDULE_TIME`: Change the daily fetch time (e.g., `"09:00"`).
- `MAX_PAGES`: Change how many pages the scraper fetches at maximum.

## Data Export

The exported `jobs.csv` file includes the following columns:
`Job ID`, `Title`, `Company`, `Location`, `Country`, `Salary`, `Category`, `Contract Type`, `Date Posted`, `Description`, `Apply Link`, `Source`

To get the best experience, open the `jobs.csv` file in Microsoft Excel or Google Sheets!
