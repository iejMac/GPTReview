import os
import json

import openai


def get_review():
  # Get the path to the GITHUB_EVENT_PATH environment variable
  event_path = os.environ["GITHUB_EVENT_PATH"]

  # Load the event data from the GITHUB_EVENT_PATH file
  with open(event_path, "r") as f:
      event_data = json.load(f)

  # Access the html_url property of the pull_request object to get the link to the PR
  pr_link = event_data["pull_request"]["html_url"]


  review = f"Horrible code, please stop, {pr_link}"
  return review

if __name__ == "__main__":
  print(get_review())
