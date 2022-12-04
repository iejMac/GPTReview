# GPTReview 🤖🔍

Get OpenAI GPT models to summarize your PR's and suggest changes by calling it in the pull request comments!

## Usage:

If you want a PR summarized and you are a whitelisted user, go to the chat of the given PR and comment anything that starts with "openai"

## How to integrate into your repo:

1. Add the following workflow
```yaml
name: Review PR with OpenAI GPT model

on:
  issue_comment:
    types: [created]

jobs:
  pr_commented:
    if: |
      github.event.issue.pull_request &&
      startsWith(github.event.comment.body, 'openai')
    name: Review PR
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python 3.8
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      - name: Install
        run: |
          sudo apt-get update
          python3 -m venv .env
          source .env/bin/activate
          python -m pip install -U pip
          pip install -r requirements.txt
      - name: Review PR and make comment
        run: |
          source .env/bin/activate
          echo "LINK=https://github.com/${{ github.repository }}/pull/${{ github.event.issue.number }}" >> $GITHUB_ENV
          echo "OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }}" >> $GITHUB_ENV
          echo "GITHUB_TOKEN=${{ github.token }}" >> $GITHUB_ENV
          echo "GITHUB_ACTOR=${{ github.actor }}" >> $GITHUB_ENV
          python review.py
```

2. Add the review.py script to the root of your repository and make sure to populate the WHITELIST variable with a list of usernames you want to be able to call the bot
```python
import os
import requests
import json

import openai


WHITELIST = [] # move this to github actions (probably some 'uses' I don't know about


def get_review():
  github_env = os.getenv("GITHUB_ENV")
  with open(github_env, "r") as f:
    variables = dict([line.split("=") for line in f.read().splitlines()])

  if variables["GITHUB_ACTOR"] not in WHITELIST: # only run review for whitelisted users
      return

  pr_link = variables["LINK"]
  openai.api_key = variables["OPENAI_API_KEY"]

  request_link = "https://patch-diff.githubusercontent.com/raw/" + pr_link[len("https://github.com/"):] + ".patch"
  patch = requests.get(request_link).text

  question = "\n Can you summarize this GitHub Pull Request for me?"
  prompt = patch[:4096 - len(question)] + question

  # model = "text-ada-001"
  model = "text-davinci-003"
  response = openai.Completion.create(
    engine=model,
    prompt=prompt,
    temperature=0.5,
    max_tokens=256,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
  )
  review = response['choices'][0]['text']

  ACCESS_TOKEN = variables["GITHUB_TOKEN"]
  headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/x-www-form-urlencoded',
  }

  data = {"body": review}
  data = json.dumps(data)


  OWNER = pr_link.split("/")[-4]
  REPO = pr_link.split("/")[-3]
  PR_NUMBER = pr_link.split("/")[-1]

  response = requests.post(f'https://api.github.com/repos/{OWNER}/{REPO}/issues/{PR_NUMBER}/comments', headers=headers, data=data)
  print(response.json())


if __name__ == "__main__":
  get_review()
```

3. Create a secret called OPENAI_API_KEY for your OpenAI API Key
