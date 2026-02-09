import os
import re
import json
import urllib.request
from datetime import datetime

GITHUB_USERNAME = "ADI-2903"
README_FILE = "README.md"
MAX_EVENTS = 10

def fetch_activity():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/events/public"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        print(f"Error fetching activity: {e}")
        return []

def format_activity(activity):
    lines = []
    for event in activity[:MAX_EVENTS]:
        event_type = event["type"]
        repo_name = event["repo"]["name"]
        repo_url = f"https://github.com/{repo_name}"
        
        action = ""
        icon = ""
        
        if event_type == "PushEvent":
            commits = len(event["payload"]["commits"])
            action = f"Pushed {commits} commit{'s' if commits > 1 else ''} to"
            icon = "⚡"
        elif event_type == "WatchEvent":
            action = "Starred"
            icon = "⭐"
        elif event_type == "CreateEvent":
            ref_type = event["payload"]["ref_type"]
            action = f"Created {ref_type}"
            icon = "🎉"
        elif event_type == "ForkEvent":
            action = "Forked"
            icon = "🔱"
        elif event_type == "PullRequestEvent":
            action = f"Opened PR in"
            icon = "🚀"
        elif event_type == "IssuesEvent":
            action = f"Opened issue in"
            icon = "🐛"
        else:
            continue # Skip other events for clean lines
            
        lines.append(f"- {icon} **{action}** [{repo_name}]({repo_url})")
        
    return "\n".join(lines)

def update_readme(content):
    with open(README_FILE, "r", encoding="utf-8") as f:
        readme_content = f.read()
    
    start_marker = "<!--START_SECTION:activity-->"
    end_marker = "<!--END_SECTION:activity-->"
    
    pattern = f"{start_marker}.*?{end_marker}"
    replacement = f"{start_marker}\n{content}\n{end_marker}"
    
    new_content = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)
    
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    print("Fetching activity...")
    activity = fetch_activity()
    if activity:
        print(f"Found {len(activity)} events.")
        formatted_content = format_activity(activity)
        print("Updating README...")
        update_readme(formatted_content)
        print("Done.")
    else:
        print("No activity found or error occurred.")
