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


import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

name = "microsoft/phi-1_5"

app = App(
    name="phi-1_5",
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

    torch.set_default_device('cuda')
    model = AutoModelForCausalLM.from_pretrained(name, trust_remote_code=True, torch_dtype="auto")
    tokenizer = AutoTokenizer.from_pretrained(name, trust_remote_code=True, torch_dtype="auto")
    inputs = tokenizer(prompt, return_tensors="pt", return_attention_mask=False)
    outputs = model.generate(**inputs, max_length=400)
    output_text = tokenizer.batch_decode(outputs)[0]

    print(output_text)
    
    # Write text output to a text file, which we'll retrieve when the async task completes
    output_path = "output.txt"
    with open(output_path, "w") as f:
        f.write(output_text)
