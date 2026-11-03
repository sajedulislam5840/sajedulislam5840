import json
import requests
from bs4 import BeautifulSoup

def fetch_contributions(username="sajedulislam5840", output_path="data/contributions.json"):
    url = f"https://github.com/users/{username}/contributions"
    print(f"[*] Fetching contributions from {url}...")
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch contributions: HTTP {resp.status_code}")
        
    soup = BeautifulSoup(resp.text, "html.parser")
    days = []
    total = 0
    
    # Extract contribution days
    for td in soup.find_all("td", class_="ContributionCalendar-day"):
        date = td.get("data-date")
        level = td.get("data-level", "0")
        if date:
            days.append({"date": date, "level": int(level)})
            
    # Parse total contributions text
    h2 = soup.find("h2", class_="f4 text-normal mb-2")
    if h2:
        parts = h2.text.split()
        for p in parts:
            if p.replace(",", "").isdigit():
                total = int(p.replace(",", ""))
                break
                
    data = {"total": total, "days": days}
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[+] Contributions saved to {output_path} (Total: {total})")

if __name__ == "__main__":
    fetch_contributions()
