import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = os.getenv("GITHUB_REPO_OWNER")
REPO_NAME = os.getenv("GITHUB_REPO_NAME")

def get_issues(state="all"):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    params = {"state": state}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        issues = response.json()
        issues = [issue for issue in issues if "pull_request" not in issue]
        
        issues_data = []
        for issue in issues:
            issue_number = issue["number"]
            title = issue["title"]
            issue_state = issue["state"]
            assignees = [a["login"] for a in issue.get("assignees", [])]
            labels = [label["name"].lower() for label in issue.get("labels", [])]
            
            issues_data.append({
                "number": issue_number,
                "title": title,
                "state": issue_state,
                "assignees": assignees,
                "labels": labels
            })
        
        return issues_data
    else:
        print(f"Error: {response.status_code} {response.text}")
        return []

def categorize_issues(issues):
    todo = []
    in_progress = []
    done = []

    for issue in issues:
        if issue["state"] == "closed" or "done" in issue["labels"]:
            done.append(issue)
        elif "in progress" in issue["labels"]:
            in_progress.append(issue)
        else:
            todo.append(issue)
    
    return todo, in_progress, done

if __name__ == "__main__":
    all_issues = get_issues("all")
    
    todo, in_progress, done = categorize_issues(all_issues)

    print("=== TO DO ===")
    for issue in todo:
        assignees_str = ", ".join(issue['assignees']) if issue['assignees'] else "No one"
        print(f"#{issue['number']}: {issue['title']} (Assigned to: {assignees_str})")

    print("\n=== IN PROGRESS ===")
    for issue in in_progress:
        assignees_str = ", ".join(issue['assignees']) if issue['assignees'] else "No one"
        print(f"#{issue['number']}: {issue['title']} (Assigned to: {assignees_str})")

    print("\n=== DONE ===")
    for issue in done:
        assignees_str = ", ".join(issue['assignees']) if issue['assignees'] else "No one"
        print(f"#{issue['number']}: {issue['title']} (Assigned to: {assignees_str})")
