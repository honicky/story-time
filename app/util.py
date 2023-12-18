from io import BytesIO
from PIL import Image
import requests
import time

# from transformers import CLIPProcessor

def current_time_ms():
    return time.time() * 1000


def url_to_pil_image(url):
  """
  Takes a URL and returns a PIL image.

  :param url: URL of the image to be fetched
  :return: PIL Image object
  """
  response = requests.get(url)
  response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

  return Image.open(BytesIO(response.content))

# def count_clip_tokens(text, model_name="openai/clip-vit-base-patch16"):
#     # Load the CLIP tokenizer
#     processor = CLIPProcessor.from_pretrained(model_name)

#     # Tokenize the text
#     tokens = processor(text, return_tensors="pt").input_ids

#     # Count the number of tokens
#     num_tokens = tokens.size(1)
    
#     return num_tokens