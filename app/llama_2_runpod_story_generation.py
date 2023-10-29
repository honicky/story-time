
import json
import os
import re
import requests
import time
import vocab

RUNPOD_SECRET_KEY = os.environ["RUNPOD_SECRET_KEY"]
BASE_URL = "https://api.runpod.ai/v2/llama2-13b-chat"

headers = {
    "Authorization": RUNPOD_SECRET_KEY,
    "Content-Type": "application/json"
}

def create_llama_prompt():
    words_to_include = vocab.three_random_words()
    return f"""
    Write a children's story using only vocabulary and concepts that a 3-year old would understand.
    The main characters are Talia and her golden retriever dog Noa.
    Use the words {words_to_include[0]},  {words_to_include[1]} and {words_to_include[2]} in the story.
    Each sentence should start with the words "Talia the brown haired little girl in the blue shirt and her golden retriever dog Noa".
    Each paragraph should be one sentence long. Make sure that each sentence really begins with "Talia the brown haired little girl in the blue shirt and her golden retriever dog Noa"
    """

def create_llama_payload(prompt):
    return {
        "input": {
            "prompt": prompt,
            "system_prompt": "you are a children's book author, writing illustrated stories for 3 year olds",
            "sampling_params": {
                "max_tokens": 1000,
                "n": 1,
                "presence_penalty": 1.0,
                "frequency_penalty": 0,
                "temperature": 0.1,
            }
        }
    }

def stream_to_text(stream):
    return "".join([
        text
        for chunk in stream
        for text in chunk["output"]["text"]
    ])

def print_stream(stream):
    for chunk in stream:
        for text in chunk["output"]["text"]:
            print(text, end="")

def fetch_story_from_endpoint(payload):
    response = requests.post(f"{BASE_URL}/run", headers=headers, json=payload)
    response_json = response.json()
    status_url = f"{BASE_URL}/stream/{response_json['id']}"

    story = ""
    while True:
        if response_json["status"] not in ("IN_QUEUE", "IN_PROGRESS", "COMPLETED"):
            print(response_json)

        if "stream" in response_json:
            stream_text = stream_to_text(response_json["stream"])
            print(stream_text, end="")
            story += stream_text

        if response_json["status"] == "COMPLETED":
            break
        else:
            time.sleep(5)
            response_json = requests.get(status_url, headers=headers).json()

    return story

def split_sentences(text):
  return [
    line
    for line in text.splitlines()[2:]
    if line.startswith("Talia")
  ]


def generate_story():
    prompt = create_llama_prompt()
    payload = create_llama_payload(prompt)
    story = fetch_story_from_endpoint(payload)

    # split the story into sentences, you can do it here.
    return split_sentences(story)

if __name__ == "__main__":
    print(generate_story())
