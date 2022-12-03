import os
import json

import openai


def get_review():
  github_env = os.getenv("GITHUB_ENV")
  pr_link = github_env
  review = f"Horrible code, please stop, {pr_link}"
  return review

if __name__ == "__main__":
  print(get_review())
