import g4f


class GptCore:
    def __init__(self):
        self.messages = []

    def add_message(self, content: str, is_assistant: bool) -> None:
        self.messages.append(
            {"role": "assistant" if is_assistant else "user", "content": content}
        )

    def ask_question(self, question: str) -> str:
        self.add_message(content=question, is_assistant=False)
        print(f"question: {question}")
        # print(f"history:\n{self.messages}")
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4_turbo,
            messages=self.messages,
        )
        print(f"answer: {response}")
        answer = "\n".join(response) if isinstance(response, tuple) else response

        self.add_message(content=answer, is_assistant=True)

        return answer

    def clear_messages(self) -> None:
        self.messages.clear()
