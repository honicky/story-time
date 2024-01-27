import os
from openai import OpenAI

client = OpenAI(api_key=openai_api_key)

class DalleClient:
  def __init__(self, openai_api_key):

  def generate_image(self, prompt):
    return client.images.generate(
      prompt=prompt,
      n=1,
      size="1024x1024"
    )["data"][0]["url"]
