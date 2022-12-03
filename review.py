import os
import requests

import openai


def get_review():
  github_env = os.getenv("GITHUB_ENV")
  with open(github_env, "r") as f:
    variables = dict([line.split("=") for line in f.readlines()])

  pr_link = variables["LINK"]

  request_link = "https://patch-diff.githubusercontent.com/raw/" + pr_link[len("https://github.com/"):] + ".patch"

  patch = requests.get(request_link).text
  # review = f"Horrible code, please stop {pr_link} {patch}"
  review = patch
  return review

if __name__ == "__main__":
  print(get_review())
