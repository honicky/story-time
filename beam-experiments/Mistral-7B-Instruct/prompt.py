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

url = "https://apps.beam.cloud/4n33n"


def create_prompt():
    words_to_include = vocab.three_random_words()
    return f"""
    Write a children's story using only vocabulary and concepts that a 3-year old would understand.
    The main characters are Talia and her golden retriever dog Noa.
    Use the words {words_to_include[0]},  {words_to_include[1]} and {words_to_include[2]} in the story.
    Each sentence should start with the words "Talia the brown haired little girl in the blue shirt and her golden retriever dog Noa".
    Each paragraph should be one sentence long. Make sure that each sentence really begins with "Talia the brown haired little girl in the blue shirt and her golden retriever dog Noa"
    """

payload = {
    "prompt": create_prompt(),
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
