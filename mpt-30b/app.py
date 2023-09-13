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

import json
import torch
import transformers
from transformers import ( AutoTokenizer, pipeline )

name = 'mosaicml/mpt-7b-instruct'


app = App(
    name="mpt-7b-instruct",
    runtime=Runtime(
        cpu=8,
        memory="32Gi",
        gpu="A10G",
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

    config = transformers.AutoConfig.from_pretrained(name, trust_remote_code=True)
    # config.attn_config['attn_impl'] = 'torch'  # change this to use triton-based FlashAttention
    # config.attn_config['attn_impl'] = 'triton'  # change this to use triton-based FlashAttention
    # config.init_device = 'meta' # For fast initialization directly on GPU!
    config.init_device = 'cuda:0' # For fast initialization directly on GPU!
    # config.max_seq_len = 16384 # (input + output) tokens can now be up to 16384


    model = transformers.AutoModelForCausalLM.from_pretrained(
        name,
        config=config,
        torch_dtype=torch.bfloat16, # Load model weights in bfloat16
        trust_remote_code=True,
        # load_in_8bit=True
    )

    tokenizer = AutoTokenizer.from_pretrained('mosaicml/mpt-30b')

    # pipe = pipeline('text-generation', model=model, tokenizer=tokenizer, device='cuda:0')
    pipe = pipeline('text-generation', model=model, tokenizer=tokenizer)
    with torch.autocast('cuda', dtype=torch.bfloat16):
        decoded_output = pipe(prompt,
            max_new_tokens=250,
            do_sample=True,
            use_cache=True
        )

    print(decoded_output)

    generated_text = decoded_output[0]['generated_text']

    # Write text output to a text file, which we'll retrieve when the async task completes
    output_path = "output.txt"
    with open(output_path, "w") as f:
        f.write(generated_text)

