import requests
from typing import List, Dict

GITHUB_API_URL = "https://api.github.com/repos/kubernetes/kubernetes/issues"


def fetch_github_issues(state: str = "open", per_page: int = 10) -> List[Dict[str, str]]:
    """
    Fetch GitHub issues from the Kubernetes repo.
    Returns a list of dicts with title, body, number, and url.
    """
    params = {
        "state": state,
        "per_page": per_page
    }
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "cognops-agent"
    }

    response = requests.get(GITHUB_API_URL, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(
            f"GitHub API error: {response.status_code} - {response.text}")

    issues = []
    for issue in response.json():
        if not issue.get("pull_request"):  # skip pull requests
            issues.append({
                "title": issue.get("title", ""),
                "body": issue.get("body", ""),
                "number": str(issue.get("number")),
                "url": issue.get("html_url", "")
            })

    return issues
