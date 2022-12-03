import os
import json

import openai


def get_review():
  pr_link = None
  review = f"Horrible code, please stop, {pr_link}"
  return review

if __name__ == "__main__":
  print(get_review())
