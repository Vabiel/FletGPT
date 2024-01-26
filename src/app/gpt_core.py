import g4f


class GptCore:
    def __init__(self):
        pass

    @staticmethod
    def ask_question(context: list):

        return g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=context,
            stream=True,
        )

