from dotenv import load_dotenv

load_dotenv()

import base64
import os
import uuid

from openai import OpenAI

from . import object_store_client

BUCKET_NAME = "botos-generated-images"


class OpenAIImageClient:
    def __init__(self, openai_api_key, image_count=4):
        self.client = OpenAI(api_key=openai_api_key)
        self.image_count = image_count

    def generate_image(self, prompt):
        """Generate images using GPT-5.2 with the image_generation tool via the Responses API."""
        images_b64 = []
        for _ in range(self.image_count):
            response = self.client.responses.create(
                model="gpt-5.2",
                input=prompt,
                tools=[{"type": "image_generation"}],
            )
            for output in response.output:
                if output.type == "image_generation_call":
                    images_b64.append(output.result)
                    break
        return upload_images_to_s3(images_b64)


def upload_images_to_s3(images_b64):
    client = object_store_client.Boto3Client()
    generation_id = uuid.uuid4()
    urls = []
    for idx, b64_data in enumerate(images_b64):
        image_bytes = base64.b64decode(b64_data)
        key = f"generated-images/{generation_id}/{idx}.png"
        client.upload_object(image_bytes, BUCKET_NAME, key, content_type="image/png")
        urls.append(construct_image_url(key))
    return urls


def construct_image_url(object_key):
    return f"https://www.storytime.glass/{object_key}"


def generate_image_with_client(prompt, image_count=4):
    openai_api_token = os.environ.get("OPENAI_API_TOKEN")
    client = OpenAIImageClient(openai_api_token, image_count=image_count)
    return client.generate_image(prompt)
