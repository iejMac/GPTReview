import os
import json

import openai


def get_review():
  github_env = os.getenv("GITHUB_ENV")
  with open(github_env, "r") as f:
    variables = dict([line.split("=") for line in f.readlines()])

  pr_link = variables["LINK"]
  review = f"Horrible code, please stop, {pr_link}"
  return review

if __name__ == "__main__":
  print(get_review())
