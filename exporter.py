import csv
import os
from config import OUTPUT_FILE

FIELDNAMES = [
    "Job ID", "Title", "Company", "Location", "Country",
    "Salary", "Category", "Contract Type", "Date Posted",
    "Description", "Apply Link", "Source",
]


def load_existing_ids(filepath):
    """Read all Job IDs already saved so we can skip duplicates."""
    if not os.path.exists(filepath):
        return set()
    seen = set()
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                jid = row.get("Job ID", "").strip()
                if jid:
                    seen.add(jid)
    except Exception:
        pass
    return seen


def export_to_csv(jobs, filepath=None):
    """
    Append new jobs to the CSV file, skipping duplicates by Job ID.
    Creates the file with a header row if it does not exist yet.
    Returns (new_count, skipped_count).
    """
    if filepath is None:
        filepath = OUTPUT_FILE

    existing_ids = load_existing_ids(filepath)
    file_exists = os.path.exists(filepath)

    new_count = 0
    skipped_count = 0

    with open(filepath, "a", newline="", encoding="utf-8-sig") as f:
        # utf-8-sig writes BOM so Excel opens it correctly without encoding issues
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()

        for job in jobs:
            jid = job.get("Job ID", "").strip()
            if jid and jid in existing_ids:
                skipped_count += 1
                continue
            writer.writerow(job)
            if jid:
                existing_ids.add(jid)
            new_count += 1

    return new_count, skipped_count
