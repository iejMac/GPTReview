import os
import requests

# Get the PR comment author's name
comment_author = os.getenv("GITHUB_ACTOR")

# Get the repository owner and name
repo_parts = os.getenv("GITHUB_REPOSITORY").split("/")
repo_owner = repo_parts[0]
repo_name = repo_parts[1]

# Get the PR number
pr_number = os.getenv("GITHUB_EVENT_NUMBER")

# Set up the GitHub API base URL and access token
api_base_url = "https://api.github.com"
api_token = os.getenv("PERSONAL_ACCESS_TOKEN")

# Set up the headers for the API request
api_headers = {
    "Authorization": f"Bearer {api_token}",
    "Accept": "application/vnd.github+json",
}

# Set up the API endpoint for posting comments to the PR
api_endpoint = f"/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments"

# Set up the data for the API request
api_data = {
    "body": f"Thanks for commenting, {comment_author}!"
}

# Make the API request to post the comment
response = requests.post(
    f"{api_base_url}{api_endpoint}",
    headers=api_headers,
    json=api_data
)

# Print the response from the API
print(response.json())
