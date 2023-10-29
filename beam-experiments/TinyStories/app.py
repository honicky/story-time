"""
### Llama 2 ###

** Pre-requisites **

1. Request access to the model on [Huggingface](https://huggingface.co/meta-llama/Llama-2-7b-hf)
2. Add your Huggingface API token to the Beam Secrets Manager, as `HUGGINGFACE_API_KEY`

** Run inference **

```sh
beam run app.py:generate -d '{"prompt": "Summarize rail travel in the United States"}'
```

** Deploy API **

```sh
beam deploy app.py:generate
```
"""
from beam import App, Runtime, Image, Output, Volume, VolumeType

from transformers import AutoModelForCausalLM, AutoTokenizer #, GenerationConfig

name = 'roneneldan/TinyStories-33M'


app = App(
    name="TinyStories-33M",
    runtime=Runtime(
        cpu=4,
        memory="16Gi",
        gpu="T4",
        image=Image(
            python_packages=[
                "accelerate",
                "bitsandbytes",
                "scipy",
                "protobuf",
                "accelerate",
                "transformers",
                "torch",
                "sentencepiece",
                "einops",
                # "triton-pre-mlir@git+https://github.com/vchiley/triton.git@triton_pre_mlir#subdirectory=python",
            ],
        ),
    ),
    volumes=[
        Volume(
            name="model_weights",
            path="./model_weights",
            volume_type=VolumeType.Persistent,
        )
    ],
)


@app.task_queue(outputs=[Output(path="output.txt")])
def generate(**inputs):
    prompt = inputs["prompt"]

    model = AutoModelForCausalLM.from_pretrained('roneneldan/TinyStories-33M')

    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-125M")

    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    output = model.generate(input_ids, max_length = 1000, num_beams=1)

    output_text = tokenizer.decode(output[0], skip_special_tokens=True)

    print(output_text)

    # Write text output to a text file, which we'll retrieve when the async task completes
    output_path = "output.txt"
    with open(output_path, "w") as f:
        f.write(output_text)
