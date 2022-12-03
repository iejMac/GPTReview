import os
import requests

import openai


def get_review():
  github_env = os.getenv("GITHUB_ENV")
  with open(github_env, "r") as f:
    variables = dict([line.split("=") for line in f.readlines()])
  pr_link = variables["LINK"]
  openai.api_key = variables["OPENAI_API_KEY"]

  request_link = "https://patch-diff.githubusercontent.com/raw/" + pr_link[len("https://github.com/"):] + ".patch"
  patch = requests.get(request_link).text

  question = "\n Can you summarize this GitHub Pull Request for me?"
  prompt = patch[:2048 - len(question)] + question

  review = variables["OPENAI_API_KEY"]

  '''
  prompt = "test"

  response = openai.Completion.create(
    engine="text-ada-001",
    prompt=prompt,
    temperature=0.5,
    max_tokens=256,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
  )
  review = response['choices'][0]['text']
  '''
  return review

if __name__ == "__main__":
  print(get_review())
