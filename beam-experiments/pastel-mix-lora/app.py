from beam import App, Runtime, Image, Output, Volume

import os
import requests
import torch
from diffusers import StableDiffusionPipeline

cache_path = "./models"
app_name = "pastel-mix-lora"
# The environment your code will run on
app = App(
    name=app_name,
    runtime=Runtime(
        cpu=4,
        memory="32Gi",
        gpu="A10G",
        image=Image(
            python_version="python3.10",
            python_packages=[
                "diffusers[torch]>=0.21",
                "transformers",
                "torch",
                "pillow",
                "accelerate",
                "safetensors",
                "xformers",
                "omegaconf"
            ],
        ),
    ),
    volumes=[Volume(name="models", path="./models")],
)


@app.task_queue(
    # File to store image outputs
    outputs=[Output(path="output.png")]
)
def generate_image(**inputs):
    prompt = f'{inputs["prompt"]}, <lora:Child illustrationa_20230804152414:0.83>'

    torch.backends.cuda.matmul.allow_tf32 = True

    pastel_model_name = "pastel_mix_checkpoint.pt"
    pastel_model_uri = "https://civitai.com/api/download/models/26321"
    pastel_model_dir_path = os.path.join(cache_path, app_name)
    pastel_model_path = os.path.join(pastel_model_dir_path, pastel_model_name)

    download_file(pastel_model_uri, pastel_model_path)

    pipe = StableDiffusionPipeline.from_single_file(
        pastel_model_path,
        revision="fp16",
        torch_dtype=torch.float16,
        local_files_only=True,
        use_safetensors=True,
    ).to("cuda")

    lora_uri = "https://civitai.com/api/download/models/139639"
    lora_name = "child-illustrationa-127614"
    tensor_name = f"{lora_name}.safetensors"
    lora_path = os.path.join(cache_path, tensor_name)
    download_file(lora_uri, lora_path)
    pipe.load_lora_weights(lora_path, weight_name=tensor_name)

    with torch.inference_mode():
        with torch.autocast("cuda"):
            image = pipe(prompt, num_inference_steps=30, guidance_scale=7).images[0]

    print(f"Saved Image: {image}")
    image.save("output.png")

def download_file(url, local_path):
  """Downloads a file from the specified URL to the provided local path,
  but only if the file does not already exist.

  Args:
    url: The URL of the file to download.
    local_path: The local path to save the downloaded file to.
  """
  # Create the directory for the file if it doesn't already exist.
  os.makedirs(os.path.dirname(local_path), exist_ok=True)

  print(f"Downloading {url} to {local_path}...")
  # Check if the file already exists.
  
  if os.path.exists(local_path):
    print(f'File {local_path} already exists.')
    return

  # Download the file.
  response = requests.get(url)

  # Save the file to the local path.
  with open(local_path, 'wb') as f:
    f.write(response.content)

  print("done")

if __name__ == "__main__":
    prompt = "a renaissance style photo of elon musk"
    generate_image(prompt=prompt)
