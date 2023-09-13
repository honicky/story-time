from beam import App, Runtime, Image, Output, Volume

import os
import torch
import concurrent.futures

from diffusers import DiffusionPipeline

# from diffusers import StableDiffusionXLPipeline, StableDiffusionXLImg2ImgPipeline
# from diffusers import (
#     PNDMScheduler,
#     LMSDiscreteScheduler,
#     DDIMScheduler,
#     EulerDiscreteScheduler,
#     EulerAncestralDiscreteScheduler,
#     DPMSolverMultistepScheduler,
# )

cache_path = "./models"

# The environment your code will run on
app = App(
    name="sdxl-app",
    runtime=Runtime(
        cpu=4,
        memory="32Gi",
        gpu="A10G",
        image=Image(
            python_version="python3.8",
            python_packages=[
                "diffusers[torch]>=0.10",
                "transformers",
                "torch",
                "pillow",
                "accelerate",
                "safetensors",
                "xformers",
                "scipy",
            ],
        ),
    ),
    volumes=[Volume(name="models", path="./models")],
)

# copied from https://github.com/runpod-workers/worker-sdxl/blob/main/src/rp_handler.py (MIT license)




    # def load_base():
    #     print('asdf')
    #     base_pipe = StableDiffusionXLPipeline.from_pretrained(
    #         "stabilityai/stable-diffusion-xl-base-1.0",
    #         # revision="fp16",
    #         cache_dir=cache_path,
    #         # Add your own auth token from Huggingface
    #         use_auth_token=os.environ["HUGGINGFACE_API_KEY"],

    #         torch_dtype=torch.float16, variant="fp16", use_safetensors=True, add_watermarker=False
    #     ).to("cuda")
    #     print('asdf2')
    #     base_pipe.enable_xformers_memory_efficient_attention()
    #     print('asdf3')
    #     return base_pipe


    # def load_refiner():
    #     print("qwer")
    #     refiner_pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
    #         "stabilityai/stable-diffusion-xl-refiner-1.0",
    #         cache_dir=cache_path,
    #         # Add your own auth token from Huggingface
    #         use_auth_token=os.environ["HUGGINGFACE_API_KEY"],

    #         torch_dtype=torch.float16, variant="fp16", use_safetensors=True, add_watermarker=False
    #     ).to("cuda")
    #     print("qwer2")
    #     refiner_pipe.enable_xformers_memory_efficient_attention()
    #     print("qwer2")
    #     return refiner_pipe

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     future_base = executor.submit(load_base)
    #     future_refiner = executor.submit(load_refiner)

    #     base = future_base.result()
    #     refiner = future_refiner.result()

    # return base, refiner

# def make_scheduler(name, config):
#     return {
#         "PNDM": PNDMScheduler.from_config(config),
#         "KLMS": LMSDiscreteScheduler.from_config(config),
#         "DDIM": DDIMScheduler.from_config(config),
#         "K_EULER": EulerDiscreteScheduler.from_config(config),
#         # "K_EULER_ANCESTRAL": EulerAncestralDiscreteScheduler.from_config(config),
#         "DPMSolverMultistep": DPMSolverMultistepScheduler.from_config(config),
#     }[name]

@app.task_queue(
    # File to store image outputs
    outputs=[
        Output(path="latent.png"),
        Output(path="output.png"),
    ]
)
def generate_image(**inputs):
    prompt = inputs["prompt"]

    # torch.backends.cuda.matmul.allow_tf32 = True

    # pipe = StableDiffusionPipeline.from_pretrained(
    #     model_id,
    #     revision="fp16",
    #     torch_dtype=torch.float16,
    #     cache_dir=cache_path,
    #     # Add your own auth token from Huggingface
    #     use_auth_token=os.environ["HUGGINGFACE_API_KEY"],
    # ).to("cuda")

    n_steps = 40
    high_noise_frac = 0.8
    
    base = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
    )
    base.to("cuda")

    refiner = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-refiner-1.0",
        text_encoder_2=base.text_encoder_2,
        vae=base.vae,
        torch_dtype=torch.float16,
        use_safetensors=True,
        variant="fp16",
    )
    refiner.to("cuda")

    # base, refiner = load_models()
    # base.scheduler = make_scheduler("DPMSolverMultistep", base.scheduler.config)
    # generator = torch.Generator("cuda").manual_seed(42)

    print("here1")
    with torch.inference_mode():
        print("here2")

        image = base(
            prompt=prompt,
            num_inference_steps=n_steps,
            denoising_end=high_noise_frac,
            output_type="latent",
        ).images
        image = refiner(
            prompt=prompt,
            num_inference_steps=n_steps,
            denoising_start=high_noise_frac,
            image=image,
        ).images[0]


    print(f"Saved Image: {image}")
    image.save("output.png")


if __name__ == "__main__":
    prompt = "a renaissance style photo of elon musk"
    generate_image(prompt=prompt)

