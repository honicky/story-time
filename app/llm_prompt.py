


import openai


class GTP4LLM:
    def __init__(self, api_token) -> None:
        self.reset_history()
        self.api_token = api_token

    def reset_history(self) -> None:
        self.chat_history = [ 
            {"role": "system", "content": "You are a children's book author helping me write a children's book for my friend's children"}
        ]

    def generate_text(self, prompt):
        # Append the user's prompt to the chat history
        self.chat_history.append({"role": "user", "content": prompt})

        # Call the GPT-4 model
        openai.api_key = self.api_token
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=self.chat_history,
            # functions=functions,
        )

        # Extract and append the model's reply to the chat history
        assistant_reply = response['choices'][0]['message']['content']
        self.chat_history.append({"role": "assistant", "content": assistant_reply})

        return assistant_reply.strip()
