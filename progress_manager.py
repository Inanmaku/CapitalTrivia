import pickle
import os


class ProgressManager:
    def __init__(self, app):
        self.app = app

    def load_progress(self):
        try:
            with open('progress.pkl', 'rb') as f:
                data = pickle.load(f)
                self.app.known_set = data.get('known_set', self.app.known_set)
                self.app.group_index = data.get('group_index', 0)
                self.app.current_questions = data.get('current_questions', [])
                self.app.correct_set = data.get('correct_set', set())
                self.app.attempts = data.get('attempts', {})
                self.app.last_question = data.get('last_question')
                self.app.current_country = data.get('current_country')
                self.app.q_index = data.get('q_index')
                self.app.previous_question = data.get('previous_question')
                self.app.deferred = data.get('deferred', {})
                if self.app.q_index is not None:
                    country, _ = self.app.countries[self.app.q_index]
                    self.app.quiz_logic.add_message(f"What is the capital of {country}?", "question")
        except FileNotFoundError:
            pass

    def save_progress(self):
        data = {
            'known_set': self.app.known_set,
            'group_index': self.app.group_index,
            'current_questions': self.app.current_questions,
            'correct_set': self.app.correct_set,
            'attempts': self.app.attempts,
            'last_question': self.app.last_question,
            'current_country': self.app.current_country,
            'q_index': self.app.q_index,
            'previous_question': self.app.previous_question,
            'deferred': self.app.deferred
        }
        with open('progress.pkl', 'wb') as f:
            pickle.dump(data, f)