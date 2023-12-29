import argparse
import json
import os
import openai
import requests
import time
import uuid

import object_store_client
import replicate


class NextLegClient:
    def __init__(self, auth_token, base_url="https://api.thenextleg.io"):
        self.auth_token = auth_token
        self.base_url = base_url
        self.ppu_url = f"{base_url}/ppu"
        self.headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }
        self.max_retries = 100
        self.retry_delay = 5000  # Initial delay in milliseconds

    def _sleep(self, milliseconds):
        time.sleep(milliseconds / 1000)

    def _fetch_to_completion(self, message_id, ppu_id, retry_count=0):
        image_res = requests.get(
            f"{self.ppu_url}/message/{message_id}?ppuId={ppu_id}", headers=self.headers
        )
        image_response_data = image_res.json()

        if image_response_data.get("progress") == 100:
            return image_response_data
        
        if image_response_data.get("progress") == "incomplete":
            raise Exception("Image generation failed")

        if retry_count >= self.max_retries:
            raise Exception(f"Max retries exceeded: {image_response_data}")

        if image_response_data.get("progress") and image_response_data.get(
            "progressImageUrl"
        ):
            print("---------------------")
            print(f'Progress: {image_response_data["progress"]}%')
            print(f'Progress Image Url: {image_response_data["progressImageUrl"]}')
            print("---------------------")

        self._sleep(self.retry_delay)
        return self._fetch_to_completion(message_id, ppu_id, retry_count + 1)

    def _check_for_errors(self, response_data):
        text = response_data.get("text", "")
        for error_code in NextLegException.error_descriptions:
            if error_code in text:
                raise NextLegException(error_code)

    def generate_image(self, prompt):
        image_res = requests.post(
            f"{self.ppu_url}/imagine",
            headers=self.headers,
            json={
                "msg": f"{prompt} --relax --v 6"
            },
            timeout=120,
        )
        image_response_data = image_res.json()

        self._check_for_errors(
            image_response_data
        )  # Check for error codes using the custom exception

        print("\n=====================")
        print("IMAGE GENERATION MESSAGE DATA")
        print(image_response_data)
        print("=====================")

        completed_image_data = self._fetch_to_completion(
            image_response_data["messageId"], image_response_data["ppuId"]
        )

        print("\n=====================")
        print("COMPLETED IMAGE DATA")
        print(completed_image_data)
        print("=====================")

        # Extract and return the array of image URLs
        image_urls = completed_image_data.get("response", {}).get("imageUrls", [])
        if image_urls and isinstance(image_urls, list):
            return copy_images_to_s3(image_urls)
        else:
            raise Exception("No image URLs found in the response")

    def get_image(self, image_url):
        payload = {"imgUrl": image_url}
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/arraybuffer",
            "Authorization": f"Bearer {self.auth_token}",
        }

        response = requests.post(
            f"{self.base_url}/getImage",
            headers=headers,
            json=payload,
            timeout=120,
        )
        import pdb; pdb.set_trace()
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Failed to get image. Status code: {response.status_code}")


# Define a custom exception for handling specific error codes and their descriptions
class NextLegException(Exception):
    error_descriptions = {
        "ALREADY_REQUESTED_UPSCALE": "You've already requested an upscale for this image",
        "BOT_TOOK_TOO_LONG_TO_PROCESS_YOUR_COMMAND": "Midjourney Bot took too long to process your command",
        "APPEAL_ACCEPTED": "Your appeal has been accepted",
        "APPEAL_REJECTED": "Your appeal has been rejected",
        "BANNED_PROMPT": "You can't use this prompt",
        "BLOCKED": "This message has been blocked",
        "BUTTON_NOT_FOUND": "Button not found",
        "FAILED_TO_PROCESS_YOUR_COMMAND": "Midjourney failed to process your command",
        "FAILED_TO_REQUEST": "Failed to request",
        "IMAGE_BLOCKED": "This image has been blocked",
        "INTERNAL_ERROR": "Midjourney had an internal error",
        "INVALID_LINK": "Invalid link",
        "INVALID_PARAMETER": "Invalid parameter",
        "JOB_ACTION_RESTRICTED": "Job action restricted",
        "JOB_QUEUED": "Job queued",
        "MODERATION_OUTAGE": "There is a content moderator outage",
        "NO_FAST_HOURS": "You've ran out of fast hours",
        "PLEASE_SUBSCRIBE_TO_MJ_IN_YOUR_DASHBOARD": "You're not subscribed to Midjourney",
        "QUEUE_FULL": "Queue full",
    }

    def __init__(self, error_code):
        self.error_code = error_code
        self.error_description = self.error_descriptions.get(
            error_code, "Unknown error code"
        )
        super().__init__(f"{self.error_code}: {self.error_description}")

class DalleClient:
    def __init__(self, openai_api_key):
        openai.api_key = openai_api_key

    def generate_image(self, prompt):
        return openai.Image.create(prompt=prompt, n=1, size="1024x1024")["data"][0][
            "url"
        ]

class StableDiffusionClient:
    def __init__(self, beam_api_key, bucket_id, user_id, beam_api_id="a066e92232b30d96e03f924643e6df42"):
        self.api_key = beam_api_key
        self.api_id = beam_api_id
        self.bucket_id = bucket_id
        self.user_id = user_id

    def _create_sdxl_payload(self, prompt):
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
            "bucket_name": self.bucket_id,
            "object_key": f"{self.user_id}/{uuid.uuid4()}.png",
        }

    def _query_sdxl_endpoint(self, payload):
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

        headers = self._construct_headers()

        # Construct payload using the provided prompt
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=600)
        return response

    def _construct_headers(self):
        return {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Authorization": f"Basic {self.api_key}",
            "Connection": "keep-alive",
            "Content-Type": "application/json"
        }

    def wait_for_complete(self, task_id, interval=10, max_retries=45):
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
        headers = self._construct_headers()
        while retries < max_retries:
            resp = requests.get(
                url=f"https://api.beam.cloud/v1/task/{task_id}/status/",
                headers=headers,
            )

            resp_data = resp.json()
            status = resp_data.get('status')

            if status == "COMPLETE":
                return
            
            elif status == "ERROR":
                raise Exception("Error occurred while processing the task.")
            
            # If status is neither "COMPLETE" nor "ERROR", sleep for the given interval before retrying
            time.sleep(interval)
            retries += 1

    def generate_image(self, prompt):
        payload = self._create_sdxl_payload(prompt)
        response = self._query_sdxl_endpoint(payload)
        if response.status_code == 200:
            task_id = response.json().get('task_id')
            self.wait_for_complete(task_id)
            return [ construct_image_url(payload['object_key']) ]

        else:
            return [ {
                "error": f"Failed to generate image. Status code: {response.status_code} Response: {response.text}",
            } ]

class ReplicateClient:
    def __init__(self, model_name, image_count=4):
        self.models = {
            "sdxl": {
                "id": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                "parameters": {
                    "width": 1024,
                    "height": 1024,
                    "refine": "expert_ensemble_refiner",
                    "scheduler": "K_EULER",
                    "lora_scale": 0.6,
                    "num_outputs": image_count,
                    "guidance_scale": 7.5,
                    "apply_watermark": False,
                    "high_noise_frac": 0.8,
                    "prompt_strength": 0.8,
                    "num_inference_steps": 25
                
                },
                "supports_multiple": True,
            },
            "playground-v2": {
                "id": "lucataco/playground-v2:6c309de0b6ef3a66502204ff2ffab0c0a9757b30498ef99b9886b79b0046f3ca",
                "parameters": {
                    "width": 1024,
                    "height": 1024,
                    "scheduler": "K_EULER_ANCESTRAL",
                    "guidance_scale": 3,
                    "playground_model": "playground-v2-1024px-aesthetic",
                    "num_inference_steps": 50,
                    "num_outputs": 4,
                },
                "supports_multiple": False,
            }
        }
        self.model_name = model_name
        self.image_count = image_count

    def generate_image(self, prompt, negative_prompt=""):

        model = self.models[self.model_name].copy()
        model["parameters"]["prompt"] = prompt
        model["parameters"]["negative_prompt"] = negative_prompt

        if self.models[self.model_name]["supports_multiple"]:
            image_urls = replicate.run(
                model["id"],
                input=model["parameters"]
            )
        else:
            image_urls = [
                replicate.run(
                    model["id"],
                    input=model["parameters"]
                )[0]
                for _ in range(self.image_count)
            ]

        return copy_images_to_s3(image_urls)

def copy_images_to_s3(image_urls):
    client = object_store_client.Boto3Client()
    generation_id = uuid.uuid4()
    return [
        construct_image_url(
            client.upload_from_url(
                image_url, "botos-generated-images", f"generated-images/{generation_id}", id
            )
        )
        for id, image_url in enumerate(image_urls)
    ]

def construct_image_url(object_key):
    return f"https://www.storytime.glass/{object_key}"


def generate_image_with_client(client_type, prompt):
    if client_type == 'nextleg':
        auth_token = os.environ.get("THE_NEXT_LEG_API_TOKEN")
        client = NextLegClient(auth_token)
    elif client_type == 'dalle':
        openai_api_token = os.environ.get("OPENAI_API_TOKEN")
        client = DalleClient(openai_api_token)
    elif client_type == 'watercolor_lora':
        beam_api_token = os.environ.get("BEAM_SECRET_KEY_UUENCODED")
        client = StableDiffusionClient(beam_api_token, "botos-generated-images", "dev-test-user")
    elif client_type == 'sdxl':
        client = ReplicateClient("sdxl")
    elif client_type == 'playground':
        client = ReplicateClient("playground-v2")
    else:
        raise ValueError("Invalid client type specified. Choose 'nextleg' or 'dalle'.")
    
    image_url = client.generate_image(prompt)
    return image_url

def main():
    parser = argparse.ArgumentParser(description='Generate images using Dalle or NextLeg clients.')
    parser.add_argument('prompt', type=str, help='The prompt to generate an image for.')
    parser.add_argument(
        '--client',
        type=str,
        choices=['nextleg', 'dalle', 'watercolor_lora', "sdxl", "playground"],
        required=True,
        help='The image generation client to use.'
    )
    
    args = parser.parse_args()
    
    image_data = generate_image_with_client(args.client, args.prompt)
    print(image_data)

if __name__ == "__main__":
    main()