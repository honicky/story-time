from io import BytesIO
from PIL import Image
import requests
import time

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

# Example usage
# image = url_to_pil_image("https://example.com/image.jpg")
# image.show()
