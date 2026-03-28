class ProgressMemory:

    def __init__(self):
        self.total_questions = 0
        self.correct_answers = 0

    def update(self, correct):

        self.total_questions += 1

        if correct:
            self.correct_answers += 1

    def stats(self):

        if self.total_questions == 0:
            return "No questions answered yet."

        accuracy = (self.correct_answers / self.total_questions) * 100

        return f"""
Questions Attempted: {self.total_questions}
Correct Answers: {self.correct_answers}
Accuracy: {accuracy:.2f}%
"""
