import os
import requests
import json

import openai


WHITELIST = ["iejMac"] # move this to github actions (probably some 'uses' I don't know about


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

  question = "\n Can you summarize this GitHub Pull Request for me and suggest possible improvements?"
  prompt = patch[:4096 - len(question.split(" "))] + question

  # model = "text-ada-001"
  model = "text-davinci-003"
  response = openai.Completion.create(
    engine=model,
    prompt=prompt,
    temperature=0.9,
    max_tokens=512, # TODO: need to find a dynamic way of setting this according to the prompt
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
