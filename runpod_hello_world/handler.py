import runpod
import torch

# import os
import json
# import time

# sleep_time = int(os.environ.get('SLEEP_TIME', 3))

# load lamma-2-70B-instruct from huggingface


def handler(event):
    #    print(event)
    # time_slept = 0
    # while time_slept < sleep_time:
    #     print("working, I promise")
    #     time_slept += 1
    #     time.sleep(1)
    # do the things
    return { 'cuda': torch.cuda.is_available() }


runpod.serverless.start({
    "handler": handler
})
