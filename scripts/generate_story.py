# import json
# import os
# import re
# import requests
# import time
# import vocab

# url = f"https://api.runpod.ai/v2/llama2-13b-chat/run"

# headers = {
#   "Authorization": os.environ["RUNPOD_SECRET_KEY"],
#   "Content-Type": "application/json"
# }

# words_to_include = vocab.three_random_words()

# prompt = f"""
# Write a children's story using only vocabulary and concepts that a 3-year old would understand.
# The main characters are Talia and her golden retriever dog Noa.
# Use the words {words_to_include[0]},  {words_to_include[1]} and {words_to_include[2]} in the story.
# Each sentence should start with the words "Talia the brown haired little girl in the blue shirt and her golden retriever dog Noa".
# Each paragraph should be one sentence long. Make sure that each sentence really begins with "Talia the brown haired little girl in the blue shirt and her golden retriever dog Noa"
# """

# # prompt = f"""
# # Write a two paragraph children's story using only vocabulary and concepts that a 3-year old would understand.
# # The main characters are Talia and her golden retriever dog Noa.
# # Use the words {words_to_include[0]},  {words_to_include[1]} and {words_to_include[2]} in the story.
# # The characters should discover a problem in the first pargraph and resolve it in the second paragraph.
# # They should change from one location to another.
# # """

# payload = {
#   "input": {
#     "prompt": prompt,
#     "system_prompt": "you are a children's book author, writing illustrated stories for 3 year olds",
#     "sampling_params": {
#       "max_tokens": 1000,
#       "n": 1,
#       "presence_penalty": 1.0,
#       "frequency_penalty": 0,
#       "temperature": 0.1,
#     }
#   }
# }

# def stream_to_text(stream):
#   return "".join([
#     text
#     for chunk in stream
#     for text in chunk["output"]["text"]
#   ])

# def print_stream(stream):
#     for chunk in stream:
#         for text in chunk["output"]["text"]:
#             print(text, end="")

# def split_sentences(text):
#     pattern = r'(?<=[.!?"])(?:\s|\n|$)'
#     sentences = re.split(pattern, text)
    
#     # Filter out any empty strings caused due to multiple spaces or newline characters
#     return [s.strip() for s in sentences if s.strip()]


# response = requests.post(url, headers=headers, json=payload)
# response_json = response.json()
# status_url = f"https://api.runpod.ai/v2/llama2-13b-chat/stream/{response_json['id']}"

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

# # story = """
# # Okay, here is a two-paragraph children's story using only vocabulary and concepts that a 3-year old would understand, with the main characters Talia and her golden retriever dog Noa:

# # Talia and Noa were playing in the forest when they saw a problem. The forest was too hot! The sun was shining bright and making everything feel yucky. They needed to find a way to cool down. So, they decided to go on an adventure to find a place that was cooler. They walked through the forest until they found a big, green meadow. In the meadow, they saw a cow eating grass. The cow told them that there was a special place where they could go to cool off. The cow led them to a big, white microwave. Inside the microwave, it was nice and cool! Talia and Noa were so happy to find a place to cool off. They played in the microwave for a while, and then they went back to the forest to continue their adventure.

# # Talia and Noa had fun in the forest and the meadow, but they were happy to be back in their own home. They learned that sometimes you have to go on an adventure to find what you need, but you can always come back home to your favorite place. And they lived happily ever after!
# # """

# truncated_story = "\n".join([
#   line
#   for line in story.splitlines()[2:]
#   if line.startswith("Talia")
# ])

# print(f"truncated story: {truncated_story}")

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
            time.sleep(1)
            response_json = requests.get(status_url, headers=headers).json()

    return story

def split_sentences(text):
  return [
    line
    for line in text.splitlines()[2:]
    if line.startswith("Talia")
  ]


def create_sdxl_payload(prompt):
    """
    Create a payload with the "prompt" key.

    Args:
        prompt (str): The initial part of the prompt.

    Returns:
        dict: The constructed payload.
    """
    
    return {
        # "prompt": f"{prompt} watercolor, children's book illustration"
        "prompt": prompt,
    }

def query_sdxl_endpoint(token, prompt):
    """
    Query the sdxl endpoint with the provided token and prompt.

    Args:
        token (str): The authorization token.
        prompt (str): The initial part of the prompt.

    Returns:
        Response: The response from the server.
    """
    
    # url = "https://apps.beam.cloud/f8oqb"
    # url = "https://apps.beam.cloud/z9j1i"
    url = "https://apps.beam.cloud/5eyxd"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Authorization": f"Basic {token}",
        "Connection": "keep-alive",
        "Content-Type": "application/json"
    }

    # Construct payload using the provided prompt
    payload = create_sdxl_payload(prompt)

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    return response

def fetch_output_urls(task_id, client_id, client_secret, interval=10, max_retries=45):
    """
    Continuously fetch the status of a task from the Beam API. If status is COMPLETE,
    it fetches and returns the output URLs. If status is ERROR, it raises an exception.
    Otherwise, it continues checking.

    Args:
        task_id (str): The ID of the task.
        client_id (str): The client ID for authentication.
        client_secret (str): The client secret for authentication.
        interval (int): Time interval (in seconds) between status checks. Default is 10 seconds.
        max_retries (int): Maximum number of times to retry checking status.

    Returns:
        list: A list of output URLs.
    """

    retries = 0
    while retries < max_retries:
        resp = requests.get(
            url=f"https://api.beam.cloud/v1/task/{task_id}/status/",
            auth=(client_id, client_secret),
        )

        resp_data = resp.json()
        status = resp_data.get('status')

        if status == "COMPLETE":
            outputs = resp_data.get('outputs', {})
            output_urls = [output_data['url'] for output_name, output_data in outputs.items() if 'url' in output_data]
            return output_urls
        
        elif status == "ERROR":
            raise Exception("Error occurred while processing the task.")
        
        # If status is neither "COMPLETE" nor "ERROR", sleep for the given interval before retrying
        time.sleep(interval)
        retries += 1

    raise Exception("Max retries reached without a complete or error status.")

def main():
    prompt = create_llama_prompt()
    payload = create_llama_payload(prompt)
    story = fetch_story_from_endpoint(payload)

    # split the story into sentences, you can do it here.
    sentences = split_sentences(story)

    token = os.environ["RUNPOD_SECRET_KEY_UUENCODED"]
    responses = [
        query_sdxl_endpoint(token, sentence)
        for sentence in sentences
    ]

    for response in responses:
        print(response.json())


if __name__ == "__main__":
    main()



