import g4f


class GptCore:
    def __init__(self):
        self.messages = []

    def add_message(self, content: str, is_assistant: bool) -> None:
        self.messages.append(
            {"role": "assistant" if is_assistant else "user", "content": content}
        )

    def ask_question(self, question: str):
        self.add_message(content=question, is_assistant=False)

        return g4f.ChatCompletion.create(    
            model=g4f.models.gpt_4,
            messages=self.messages,
            stream=True,
        )

    def clear_messages(self) -> None:
        self.messages.clear()
