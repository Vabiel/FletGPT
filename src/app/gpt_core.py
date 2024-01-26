import g4f


class GptCore:
    def __init__(self):
        pass

    def ask_question(self, context: list):

        return g4f.ChatCompletion.create(    
            model=g4f.models.gpt_4,
            messages=context,
            stream=True,
        )

    def clear_messages(self) -> None:
        self.messages.clear()
