import requests
from config import APP_ID, APP_KEY, MAX_PAGES

BASE_URL = "https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"

HEADERS = {
    "User-Agent": "JobFetcher/1.0"
}


def fetch_jobs(keyword, country_code, location=""):
    """
    Fetch all paginated job results from Adzuna for a given keyword and country.
    Returns a list of cleaned job dicts.
    """
    all_jobs = []
    seen_ids = set()

    for page in range(1, MAX_PAGES + 1):
        url = BASE_URL.format(country=country_code, page=page)
        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "results_per_page": 50,
            "what": keyword,
            "content-type": "application/json",
        }
        if location:
            params["where"] = location

        try:
            response = requests.get(url, params=params, headers=HEADERS, timeout=15)
        except requests.exceptions.RequestException as e:
            print(f"  [Network Error] Page {page}: {e}")
            break

        if response.status_code == 400:
            # Adzuna returns 400 when page exceeds available results
            break
        if response.status_code == 401:
            print("  [Auth Error] Check your APP_ID and APP_KEY in config.py")
            break
        if response.status_code != 200:
            print(f"  [API Error] Status {response.status_code} on page {page}")
            break

        data = response.json()
        results = data.get("results", [])

        if not results:
            break

        for job in results:
            job_id = job.get("id", "")
            if job_id in seen_ids:
                continue
            seen_ids.add(job_id)

            salary_min = job.get("salary_min", "")
            salary_max = job.get("salary_max", "")
            salary = ""
            if salary_min and salary_max:
                salary = f"{int(salary_min):,} - {int(salary_max):,}"
            elif salary_min:
                salary = f"{int(salary_min):,}+"
            elif salary_max:
                salary = f"Up to {int(salary_max):,}"

            description = job.get("description", "").replace("\n", " ").strip()
            if len(description) > 400:
                description = description[:397] + "..."

            all_jobs.append({
                "Job ID":       job_id,
                "Title":        job.get("title", "").strip(),
                "Company":      job.get("company", {}).get("display_name", "").strip(),
                "Location":     job.get("location", {}).get("display_name", "").strip(),
                "Country":      country_code.upper(),
                "Salary":       salary,
                "Category":     job.get("category", {}).get("label", "").strip(),
                "Contract Type":job.get("contract_type", "").strip(),
                "Date Posted":  job.get("created", "")[:10],
                "Description":  description,
                "Apply Link":   job.get("redirect_url", "").strip(),
                "Source":       "Adzuna",
            })

        print(f"  Page {page}: fetched {len(results)} jobs (total so far: {len(all_jobs)})")

        # Stop early if last page had fewer than 50 (no more pages)
        if len(results) < 50:
            break

    return all_jobs
