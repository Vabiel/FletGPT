class Message():
    def __init__(self, text: str, is_gpt_answer: bool):
        self.text = text
        self.is_gpt_answer = is_gpt_answer