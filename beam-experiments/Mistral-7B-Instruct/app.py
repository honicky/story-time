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

name = 'mistralai/Mistral-7B-Instruct-v0.1'


app = App(
    name="Mistral-7B-Instruct",
    runtime=Runtime(
        cpu=4,
        memory="32Gi",
        gpu="A10G",
        image=Image(
            python_packages=[
                "accelerate",
                "bitsandbytes",
                "scipy",
                "protobuf",
                "git+https://github.com/huggingface/transformers",
                "torch",
                "sentencepiece",
                "einops",
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

    print("here")
    device = "cuda" # the device to load the model onto

    model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")

    print("loaded")

    # this chat template is an easy way to make sure that the prompt is formatted correctly for the mode
    # even though we are not actually chatting
    messages = [
        {"role": "user", "content": prompt},
    ]

    encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")

    print(encodeds)

    model_inputs = encodeds.to(device)
    model.to(device)

    generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)
    decoded = tokenizer.batch_decode(generated_ids)
    print(decoded[0])

    # Write text output to a text file, which we'll retrieve when the async task completes
    output_path = "output.txt"
    with open(output_path, "w") as f:
        f.write(decoded[0])
