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
            return {
                "attempted": 0,
                "correct": 0,
                "accuracy": 0
            }

        accuracy = (self.correct_answers / self.total_questions) * 100

        return {
            "attempted": self.total_questions,
            "correct": self.correct_answers,
            "accuracy": round(accuracy, 2)
        }