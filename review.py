import os
import requests
import json
from text_generation import Client


WHITELIST = ["younesbelkada", "lvwerra"] # move this to github actions (probably some 'uses' I don't know about
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/starchat-beta"
MAX_NUM_TOKENS = 8192
SYS_MESSAGE="Below is a conversation between a human user and a helpful AI coding assistant.\n\n"
QUESTION = "Can you summarize this GitHub Pull Request for me and suggest possible improvements?"

def get_review(hf_api_key=None):
  github_env = os.getenv("GITHUB_ENV")
  with open(github_env, "r") as f:
    variables = dict([line.split("=") for line in f.read().splitlines()])

  if variables["GITHUB_ACTOR"] not in WHITELIST: # only run review for whitelisted users
      return

  pr_link = variables["LINK"]
  if hf_api_key is None:
    hf_api_key = os.getenv("HF_HUB_KEY")

  request_link = "https://patch-diff.githubusercontent.com/raw/" + pr_link[len("https://github.com/"):] + ".patch"
  patch = requests.get(request_link).text

  truncated_patch = patch[:MAX_NUM_TOKENS - len(QUESTION.split(" "))] 
  prompt = SYS_MESSAGE + f"Human: \n```{truncated_patch}```\n{QUESTION}\n\nAssistant: "


  client = Client(
    API_URL,
    headers={"Authorization": f"Bearer {hf_api_key}"} if hf_api_key is not None else None,
  )

  # TODO: add generation kwargs
  response = client.generate(prompt)
  review = response.generated_text

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
