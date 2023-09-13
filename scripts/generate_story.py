import json
import re
import requests
import time
import vocab

url = f"https://api.runpod.ai/v2/llama2-13b-chat/run"

headers = {
  "Authorization": os.environ["RUNPOD_SECRET_KEY"],
  "Content-Type": "application/json"
}

words_to_include = vocab.three_random_words()

prompt = f"""
Write a children's story using only vocabulary and concepts that a 3-year old would understand.
The main characters are Talia and her golden retriever dog Noa.
Use the words {words_to_include[0]},  {words_to_include[1]} and {words_to_include[2]} in the story.
Each sentence should start with the words "Talia the brown haired little girl in the blue shirt and her golden retriever dog Noa".
Each paragraph should be one sentence long. Make sure that each sentence really begins with "Talia the brown haired little girl in the blue shirt and her golden retriever dog Noa"
"""

# prompt = f"""
# Write a two paragraph children's story using only vocabulary and concepts that a 3-year old would understand.
# The main characters are Talia and her golden retriever dog Noa.
# Use the words {words_to_include[0]},  {words_to_include[1]} and {words_to_include[2]} in the story.
# The characters should discover a problem in the first pargraph and resolve it in the second paragraph.
# They should change from one location to another.
# """

payload = {
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

def split_sentences(text):
    pattern = r'(?<=[.!?"])(?:\s|\n|$)'
    sentences = re.split(pattern, text)
    
    # Filter out any empty strings caused due to multiple spaces or newline characters
    return [s.strip() for s in sentences if s.strip()]


response = requests.post(url, headers=headers, json=payload)
response_json = response.json()
status_url = f"https://api.runpod.ai/v2/llama2-13b-chat/stream/{response_json['id']}"

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
    time.sleep(1)
    response_json = requests.get(status_url, headers=headers).json()

# story = """
# Okay, here is a two-paragraph children's story using only vocabulary and concepts that a 3-year old would understand, with the main characters Talia and her golden retriever dog Noa:

# Talia and Noa were playing in the forest when they saw a problem. The forest was too hot! The sun was shining bright and making everything feel yucky. They needed to find a way to cool down. So, they decided to go on an adventure to find a place that was cooler. They walked through the forest until they found a big, green meadow. In the meadow, they saw a cow eating grass. The cow told them that there was a special place where they could go to cool off. The cow led them to a big, white microwave. Inside the microwave, it was nice and cool! Talia and Noa were so happy to find a place to cool off. They played in the microwave for a while, and then they went back to the forest to continue their adventure.

# Talia and Noa had fun in the forest and the meadow, but they were happy to be back in their own home. They learned that sometimes you have to go on an adventure to find what you need, but you can always come back home to your favorite place. And they lived happily ever after!
# """

truncated_story = "\n".join([
  line
  for line in story.splitlines()[2:]
  if line.startswith("Talia")
])

print(f"truncated story: {truncated_story}")

# break_up_prompt = f"""
# [INST]
# Here is a children's story:

# {truncated_story}

# Change each sentence so is self contained, and it explicitly mentions "Talia and her golden retriever Noa"
# [/INST]

# """

# print(f"break_up_prompt: {break_up_prompt}")

# payload = {
#   "input": {
#     "prompt": break_up_prompt,
#     "system_prompt": "you are a children's book illustrator, breaking up the story into self contained pages",
#     "sampling_params": {
#       "max_tokens": 1000,
#       "n": 1,
#       "presence_penalty": 1.0,
#       "frequency_penalty": .5,
#       "temperature": 0.7,
#     }
#   }
# }

# # sentences = split_sentences(story)
# response = requests.post(url, headers=headers, json=payload)
# response_json = response.json()
# status_url = f"https://api.runpod.ai/v2/llama2-13b-chat/stream/{response_json['id']}"

# # import pdb; pdb.set_trace()
# #print_stream(response_json["stream"])

# story = ""
# while True:
#   if response_json["status"] not in ("IN_QUEUE", "IN_PROGRESS", "COMPLETED"):
#     print(response_json)

#   if "stream" in response_json:
#     stream_text = stream_to_text(response_json["stream"])
#     print(stream_text, end="")
#     story += stream_text

#   if response_json["status"] == "COMPLETED":
#     break
#   else:
#     time.sleep(1)
#     response_json = requests.get(status_url, headers=headers).json()

