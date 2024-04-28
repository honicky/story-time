from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI
import replicate
from .util import current_time_ms
from wandb.sdk.data_types.trace_tree import Trace


class GTP4LLM:
    def __init__(self, api_token) -> None:
        self.reset_history()
        self.api_token = api_token
        self.client = OpenAI(api_key=self.api_token)

    def reset_history(self) -> None:
        self.chat_history = [
            {
                "role": "system",
                "content": "You are a children's book author helping me write a children's book for my friend's children",
            }
        ]

    def generate_text(self, prompt, wandb_parent_span, model_name="gpt-4-1106-preview"):
        # Append the user's prompt to the chat history
        self.chat_history.append({"role": "user", "content": prompt})

        # Call the GPT-4 model
        # model_name = "gpt-4"
        # model_name = "gpt-4-1106-preview"
        start_time = current_time_ms()

        try:
            response = self.client.chat.completions.create(model=model_name, messages=self.chat_history)

            end_time = current_time_ms()
            status = "success"
            status_message = "Success"
            response_text = response.choices[0].message.content
            token_usage = response.usage

        except Exception as e:
            end_time = current_time_ms()
            status = "error"
            status_message = str(e)
            response_text = ""
            token_usage = {}

        llm_prompt_span = Trace(
            name="LLMPrompt",
            kind="llm",
            status_code=status,
            status_message=status_message,
            metadata={
                "token_usage": token_usage,
                "model_name": model_name,
            },
            start_time_ms=start_time,
            end_time_ms=end_time,
            inputs={"prompt": prompt, "chat_history": self.chat_history[:-1]},
            outputs={"response": response_text},
        )
        wandb_parent_span.add_child(llm_prompt_span)
        wandb_parent_span.add_inputs_and_outputs(inputs={"prompt": prompt}, outputs={"response": response_text})
        wandb_parent_span._span.end_time_ms = end_time

        if status == "success":
            # Extract and append the model's reply to the chat history
            self.chat_history.append({"role": "assistant", "content": response_text})

        return response_text.strip()

class OpenAILLM:
    def __init__(self, api_token) -> None:
        self.api_token = api_token
        self.client = OpenAI(api_key=self.api_token)

    def generate_text(self, prompt, model_name="gpt-3.5-turbo-0125", **non_default_params):
        # Append the user's prompt to the chat history
        messages = [
            {
                "role": "system",
                "content": "You are a children's book author helping me write a children's book for my friend's children",
            },
            {
                "role": "user", "content": prompt
            }
        ]

        response = self.client.chat.completions.create(model=model_name, messages=messages, **non_default_params)
        response_text = response.choices[0].message.content

        return response_text.strip()

class ReplicateLLM:

    models = {
        "mixtral": {
            "id": "mistralai/mixtral-8x7b-instruct-v0.1",
            "parameters": {
            "top_k": 50,
            "top_p": 0.9,
            "prompt": None,
            "temperature": 0,
            "max_new_tokens": 1024,
            "prompt_template": "<s>[INST] {prompt} [/INST] ",
            "presence_penalty": 0,
            "frequency_penalty": 0
            },
        },
        "llama-2-70b": {
            "id": "meta/llama-2-70b-chat",    
            "parameters": {
            "debug": False,
            "top_k": 50,
            "top_p": 1,
            "prompt": None,
            "temperature": 0.5,
            "system_prompt": "You are a helpful, respectful and honest assistant.",
            "max_new_tokens": 500,
            "min_new_tokens": -1
            },
        },
        "codellama-7b-instruct": {
            "id": "meta/codellama-7b-instruct:aac3ab196f8a75729aab9368cd45ea6ad3fc793b6cda93b1ded17299df369332",
            "parameters": {
            "top_k": 250,
            "top_p": 0.95,
            "prompt": None,
            "max_tokens": 500,
            "temperature": 0.95,
            "system_prompt": "",
            "repeat_penalty": 1.1,
            "presence_penalty": 0,
            "frequency_penalty": 0
            }
        },
        "codellama-13b-instruct": {
            "id": "meta/codellama-13b-instruct:a5e2d67630195a09b96932f5fa541fe64069c97d40cd0b69cdd91919987d0e7f",
            "parameters": {
            "top_k": 250,
            "top_p": 0.95,
            "prompt": None,
            "max_tokens": 500,
            "temperature": 0.95,
            "system_prompt": "",
            "repeat_penalty": 1.1,
            "presence_penalty": 0,
            "frequency_penalty": 0
            }
        },
        "codellama-34b-instruct": {
            "id": "meta/codellama-34b-instruct:eeb928567781f4e90d2aba57a51baef235de53f907c214a4ab42adabf5bb9736",
            "parameters": {
            "top_k": 50,
            "top_p": 0.9,
            "prompt": None,
            "max_tokens": 500,
            "temperature": 0.75,
            "system_prompt": "Responses should be written in Python.",
            "repeat_penalty": 1.1,
            "presence_penalty": 0,
            "frequency_penalty": 0
            }
        },
        "codellama-70b-instruct": {
            "id": "meta/codellama-70b-instruct:a279116fe47a0f65701a8817188601e2fe8f4b9e04a518789655ea7b995851bf",
            "parameters": {
            "top_k": 10,
            "top_p": 0.95,
            "prompt": None,
            "max_tokens": 500,
            "temperature": 0.8,
            "system_prompt": "",
            "repeat_penalty": 1.1,
            "presence_penalty": 0,
            "frequency_penalty": 0
            }
        },
    }

    def __init__(self, model_name):
        self.model_name = model_name

    def generate_text(self, prompt, **non_default_params):

        parameters = ReplicateLLM.models[self.model_name]["parameters"].copy()
        parameters.update(non_default_params)
        parameters["prompt"] = prompt

        for event in replicate.run(
            ReplicateLLM.models[self.model_name]["id"],
            parameters
        ):
            yield str(event)

