import os
import requests

import openai


def get_review():
  github_env = os.getenv("GITHUB_ENV")
  with open(github_env, "r") as f:
    variables = dict([line.split("=") for line in f.read().splitlines()])
  pr_link = variables["LINK"]
  openai.api_key = variables["OPENAI_API_KEY"]

  request_link = "https://patch-diff.githubusercontent.com/raw/" + pr_link[len("https://github.com/"):] + ".patch"
  patch = requests.get(request_link).text

  question = "\n Can you summarize this GitHub Pull Request for me?"
  prompt = patch[:4096 - len(question)] + question

  response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    temperature=0.5,
    max_tokens=256,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
  )
  review = response['choices'][0]['text']
  print(review)

  review = "".join(review.split()) # This way has issues with whitespace in comment body

  ACCESS_TOKEN = variables["GITHUB_TOKEN"]
  headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/x-www-form-urlencoded',
  }

  data = '{"body":"' + review + '"}'
  OWNER = pr_link.split("/")[-4]
  REPO = pr_link.split("/")[-3]
  PR_NUMBER = pr_link.split("/")[-1]

  response = requests.post(f'https://api.github.com/repos/{OWNER}/{REPO}/issues/{PR_NUMBER}/comments', headers=headers, data=data)

  print(response.json())


if __name__ == "__main__":
  get_review()
