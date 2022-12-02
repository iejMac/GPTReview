import os
import requests

base_url = "https://api.github.com"
auth_token = os.environ["GITHUB_TOKEN"]
repo = os.environ["GITHUB_REPOSITORY"]
pull_request_number = os.environ["GITHUB_PULL_REQUEST"]
comment_body = "<comment_body>"

url = f"{base_url}/repos/{repo}/issues/{pull_request_number}/comments"
headers = {
    "Authorization": f"Bearer {auth_token}",
    "Content-Type": "application/json",
}

response = requests.post(url, json={"body": comment_body}, headers=headers)

if response.status_code == 201:
    print("Comment posted successfully")
else:
    print(f"Error posting comment: {response.status_code} {response.reason}")
