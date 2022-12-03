import os
import requests

import openai


def get_review():
  github_env = os.getenv("GITHUB_ENV")
  with open(github_env, "r") as f:
    variables = dict([line.split("=") for line in f.readlines()])

  pr_link = variables["LINK"]

  cookies = {
      '_octo': 'GH1.1.65460497.1638757762',
      'logged_in': 'no',
      'preferred_color_mode': 'dark',
      'tz': 'America%2FLos_Angeles',
      '_gh_sess': 'Im4XfXn8RWAB63Kd9RpM7%2F0zu1ArvGPsFi%2BHPBgTXFxOFKpx0sqjM7kUwIxDpKsV%2Fm136GT7ahy%2BY1EmZz%2FAduDQYT4VZOuksT8xNW7RYdAhv3kk%2BNl2Jwypksn6OytVLep5gIak7KwJ4noyGYyNMlcCNqQSA6mvr7BiUF2QgiO5R5vlWJxjuBgJRVXpRQdsjhWR8M1G8VdBe7nObuL2WOaoq9ve1gkUa7K8OE1aKA3EFnyonZmKVnagyfnRLWyiAZZkHmO%2FIBayaXIk0NT4Fw%3D%3D--HUNOxGtaOI40XnQH--CuNOeDvsNO1btPhdR115vQ%3D%3D',
  }

  headers = {
      'authority': 'github.com',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'accept-language': 'en-US,en;q=0.9',
      # 'cookie': '_octo=GH1.1.65460497.1638757762; logged_in=no; preferred_color_mode=dark; tz=America%2FLos_Angeles; _gh_sess=Im4XfXn8RWAB63Kd9RpM7%2F0zu1ArvGPsFi%2BHPBgTXFxOFKpx0sqjM7kUwIxDpKsV%2Fm136GT7ahy%2BY1EmZz%2FAduDQYT4VZOuksT8xNW7RYdAhv3kk%2BNl2Jwypksn6OytVLep5gIak7KwJ4noyGYyNMlcCNqQSA6mvr7BiUF2QgiO5R5vlWJxjuBgJRVXpRQdsjhWR8M1G8VdBe7nObuL2WOaoq9ve1gkUa7K8OE1aKA3EFnyonZmKVnagyfnRLWyiAZZkHmO%2FIBayaXIk0NT4Fw%3D%3D--HUNOxGtaOI40XnQH--CuNOeDvsNO1btPhdR115vQ%3D%3D',
      'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"macOS"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'none',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
  }

  patch = requests.get(pr_link + ".patch", cookies=cookies, headers=headers).text
  # review = f"Horrible code, please stop {pr_link} {patch}"
  review = patch
  return review

if __name__ == "__main__":
  print(get_review())
