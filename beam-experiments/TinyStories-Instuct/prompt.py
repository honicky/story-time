#!/usr/bin/env python3

import json
import random
import requests
import vocab

words = ", ".join(vocab.three_random_words())

possible_features = [
    "Dialogue",
    "Conflict",
    "Foreshadowing",
    "MoralValue",
]

size = random.randint(1,2)
features = ", ".join(random.sample(possible_features, size))

url = "https://apps.beam.cloud/mu2c2"
payload = {
    "prompt": f"""
Words: {words}
Features: {features}
Story:
"""
}

print (payload)


headers = {
  "Accept": "*/*",
  "Accept-Encoding": "gzip, deflate",
  "Authorization": "Basic YTA2NmU5MjIzMmIzMGQ5NmUwM2Y5MjQ2NDNlNmRmNDI6ODc4YWVlNmQ1MDVkMTYxNDlkZTZiNjJhMTY2ZDFmZGY=",
  "Connection": "keep-alive",
  "Content-Type": "application/json"
}

response = requests.request("POST", url, 
  headers=headers,
  data=json.dumps(payload)
)
