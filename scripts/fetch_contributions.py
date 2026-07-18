import os
import json
import requests
from bs4 import BeautifulSoup

def fetch_contributions(username):
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html"
    }
    
    print(f"Fetching contributions for {username}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch. Status code: {response.status_code}")
        return
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    days = soup.select("td.ContributionCalendar-day")
    
    contributions = []
    for day in days:
        date = day.get('data-date')
        if not date:
            continue
        level = day.get('data-level', '0')
        count = 0
        text = day.text.strip()
        if "contribution" in text.lower():
            parts = text.split(" ")
            if parts[0] == "No":
                count = 0
            else:
                try:
                    count = int(parts[0].replace(",", ""))
                except ValueError:
                    pass
        
        contributions.append({
            "date": date,
            "level": int(level),
            "count": count
        })
        
    os.makedirs("data", exist_ok=True)
    
    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(contributions, f, indent=2)
        
    print(f"Saved {len(contributions)} days of data.")

if __name__ == "__main__":
    fetch_contributions("Adi-2903")
