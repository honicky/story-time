from beam import App, Runtime, Image, Output, Volume, VolumeType

import json
import os
import requests
import time
import uuid

import llama_2_runpod_story_generation as story_gen
import object_store_client

# The environment your code will run on
app = App(
    name="image-story-generator",
    runtime=Runtime(
        cpu=1,
        memory="4Gi",
        image=Image(
            python_version="python3.10",
            python_packages=[
                "boto3",
            ],
        ),
    ),
    # volumes=[Volume(name="models", path="./models")],
)

def create_sdxl_payload(prompt, bucket_id, object_key):
    """
    Create a payload with the "prompt" key.

    Args:
        prompt (str): The initial part of the prompt.
        bucket_id (str): The ID of the bucket to store the output image.
        object_key (str): The path to the image object

    Returns:
        dict: The constructed payload.
    """
    
    return {
        "prompt": prompt,
        "bucket_name": bucket_id,
        "object_key": object_key,
    }

def query_sdxl_endpoint(token, payload):
    """
    Query the sdxl endpoint with the provided token and prompt.

    Args:
        token (str): The authorization token.
        prompt (str): The initial part of the prompt.

    Returns:
        Response: The response from the server.
    """
    
    # url = "https://apps.beam.cloud/f8oqb"
    # url = "https://apps.beam.cloud/5eyxd"
    url = "https://apps.beam.cloud/z9j1i"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Authorization": f"Basic {token}",
        "Connection": "keep-alive",
        "Content-Type": "application/json"
    }

    # Construct payload using the provided prompt
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=600)
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
            timeout=10
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

def create_story_descriptor(sentences, image_paths):
    return json.dumps({
        "sentences": sentences,
        "image_paths": image_paths,
    }).encode('utf-8')

def write_story_descriptor(story_descriptor, bucket_id, user_id):
    client = object_store_client.Boto3Client()
    story_descriptor_key = f"{user_id}/story_descriptor.json"
    client.upload_object(story_descriptor, bucket_id, story_descriptor_key)

@app.schedule(when="20 17 * * *")
def generate_image_story():

    sentences = story_gen.generate_story()

    token = os.environ["BEAM_SECRET_KEY_UUENCODED"]
    user_id = "rj-test-user"
    bucket_id = "botos-generated-images"
    image_paths = [f"{user_id}/{uuid.uuid4()}.png" for i in range(len(sentences))]
    payloads = [
        create_sdxl_payload(sentence, bucket_id, image_path)
        for sentence, image_path in zip(sentences, image_paths)
    ]

    responses = [
        query_sdxl_endpoint(token, payload)
        for payload in payloads
    ]

    # for now, we just rely on exceptions to handle errors and diagnostic output
    story_descriptor = create_story_descriptor(sentences, image_paths)
    write_story_descriptor(story_descriptor, bucket_id, user_id)
    
