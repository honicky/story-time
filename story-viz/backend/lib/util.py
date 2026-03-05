from io import BytesIO
from PIL import Image
import requests
import time


def current_time_ms():
    return time.time() * 1000


def url_to_pil_image(url):
    """Takes a URL and returns a PIL image."""
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))
