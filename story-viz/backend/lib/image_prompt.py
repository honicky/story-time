from dotenv import load_dotenv

load_dotenv()

import os
import uuid

from openai import OpenAI

from . import object_store_client


class DalleClient:
    def __init__(self, openai_api_key, image_count=4):
        self.client = OpenAI(api_key=openai_api_key)
        self.image_count = image_count

    def generate_image(self, prompt):
        """Generate images using DALL-E 3. Makes multiple API calls since DALL-E 3 only supports n=1."""
        image_urls = []
        for _ in range(self.image_count):
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024",
            )
            image_urls.append(response.data[0].url)
        return copy_images_to_s3(image_urls)


def copy_images_to_s3(image_urls):
    client = object_store_client.Boto3Client()
    generation_id = uuid.uuid4()
    return [
        construct_image_url(
            client.upload_from_url(image_url, "botos-generated-images", f"generated-images/{generation_id}", id)
        )
        for id, image_url in enumerate(image_urls)
    ]


def construct_image_url(object_key):
    return f"https://www.storytime.glass/{object_key}"


def generate_image_with_client(prompt, image_count=4):
    openai_api_token = os.environ.get("OPENAI_API_TOKEN")
    client = DalleClient(openai_api_token, image_count=image_count)
    return client.generate_image(prompt)
