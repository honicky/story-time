from beam import App, Runtime, Image, Output, Volume

import io
import PIL
import torch

from diffusers import StableDiffusionXLPipeline

import object_store_client

cache_path = "./models"

# The environment your code will run on
app = App(
    name="sdxl-watercolor-lora-app",
    runtime=Runtime(
        cpu=4,
        memory="32Gi",
        gpu="A10G",
        image=Image(
            python_version="python3.8",
            python_packages=[
                "transformers",
                "safetensors",
                "accelerate",
                "boto3",
                # "diffusers[torch]==0.11.0",
                # "diffusers[torch]>=0.21",
                "torch==2.0.0",
                "diffusers[torch]",
                # "git+https://github.com/huggingface/diffusers.git",
            ],
        ),
    ),
    volumes=[Volume(name="models", path="./models")],
)

@app.task_queue(
    # File to store image outputs
    outputs=[
        Output(path="output.png"),
    ]
)
def generate_image(**inputs):
    prompt = inputs["prompt"]

    pipe = create_sdxl_lora_pipeline()

    image = generate_image_from_prompt(prompt, pipe)

    image_bytes = convert_image_to_bytes(image)
    bucket_name = inputs["bucket_name"]
    object_key = inputs["object_key"]
    
    upload_to_object_storage(image_bytes, bucket_name, object_key)

def generate_image_from_prompt(prompt: str, pipe):
    lora_scale= 0.9
    image = pipe(
        prompt,
        negative_prompt="ugly, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, ugly, blurry, bad anatomy, bad proportions, wrong proportions, extra limbs, cloned face, disfigured, out of frame, ugly, extra limbs, bad anatomy, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, mutated hands, fused fingers, too many fingers, long neck",
        num_inference_steps=30,
        guidance_scale=7.5,
        cross_attention_kwargs={"scale": lora_scale},
    ).images[0]
    
    return image

def create_sdxl_lora_pipeline():
    model_path = "stabilityai/stable-diffusion-xl-base-1.0"
    pipe = StableDiffusionXLPipeline.from_pretrained(model_path, torch_dtype=torch.float16)
    pipe.to("cuda")
    pipe.load_lora_weights("ostris/watercolor_style_lora_sdxl", weight_name="watercolor_v1_sdxl.safetensors")
    return pipe

def upload_to_object_storage(image: bytes, bucket_name: str, key: str) -> None:
    client = object_store_client.Boto3Client()
    print(f"writing image to {bucket_name}/{key}")
    client.upload_object(image, bucket_name, key)
    print(f"wrote image to {bucket_name}/{key}")


def convert_image_to_bytes(pil_image) -> bytes:
    image_bytes_io = io.BytesIO()
    pil_image.save(image_bytes_io, format="PNG")
    return image_bytes_io.getvalue()

