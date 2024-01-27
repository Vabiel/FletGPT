import g4f


class GptCore:
    def __init__(self):
        pass

    @staticmethod
    def ask_question(context: list, model: str):

        return g4f.ChatCompletion.create(
            model=model,
            messages=context,
            stream=True,
        )

