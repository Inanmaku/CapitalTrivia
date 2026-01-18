import random
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

from ui_components import Bubble


class QuizLogic:
    def __init__(self, app):
        self.app = app

    def load_next_group(self):
        if self.app.group_index < len(self.app.groups):
            self.app.current_questions = [q for q in self.app.groups[self.app.group_index] if q in self.app.all_countries]
            self.app.group_index += 1
        else:
            self.app.current_questions = []

    def get_next_question(self):
        candidates = [q for q in self.app.current_questions if q[0] not in self.app.correct_set]
        if not candidates:
            if self.app.group_index < len(self.app.groups):
                self.load_next_group()
                return self.get_next_question()
            else:
                self.add_message("🎉 You’ve answered all capitals correctly!", "feedback")
                return None
        # Get available candidates (not deferred or deferred count <= 0)
        available = [q for q in candidates if q not in self.app.deferred or self.app.deferred[q] <= 0]
        if available:
            q = available[0]
        else:
            # All are deferred, pick the one with the lowest deferred count
            q = min(candidates, key=lambda x: self.app.deferred.get(x, 0))
        # Decrement deferred counts
        for key in list(self.app.deferred.keys()):
            if self.app.deferred[key] > 0:
                self.app.deferred[key] -= 1
            else:
                del self.app.deferred[key]
        self.app.last_question = q
        return q

    def load_question(self):
        q = self.get_next_question()
        if q is None:
            return
        country, capital = q
        self.app.q_index = self.app.countries.index(q)
        self.add_message(f"What is the capital of {country}?", "question")

    def get_capital(self, country):
        for c, cap in self.app.countries:
            if c == country:
                return cap
        return ""

    def check_answer(self):
        ans = self.app.answer_box.text().strip().lower()
        if not ans:
            return

        self.add_message(ans, "answer")
        country, correct_capital = self.app.countries[self.app.q_index]
        info = self.app.known_set[country]
        info["attempts"] += 1

        if ans == correct_capital.lower():
            self.add_message("Correct!✅", "feedback")

            if info["attempts"] >= 3:
                self.add_emote(self.app.emotes["proud"])

            info["correct"] = True
            self.app.correct_set.add(country)

            if not [q for q in self.app.current_questions if q[0] not in self.app.correct_set]:
                if self.app.group_index < len(self.app.groups) - 1:
                    self.add_message("You've completed this set!🎉 Moving to the next.", "feedback")
        else:
            if info["attempts"] == 3:
                self.add_emote(self.app.emotes["interesting"])
            elif info["attempts"] == 6:
                self.add_emote(self.app.emotes["awkward"])

            self.add_message(f"Wrong!❌ The answer is {correct_capital.title()}.", "feedback")
            self.app.deferred[self.app.countries[self.app.q_index]] = 6

        self.app.answer_box.clear()
        self.load_question()

    def add_message(self, text, bubble_type):
        img = {
            "question": self.app.question_bubble,
            "answer": self.app.answer_bubble,
            "feedback": self.app.feedback_bubble
        }.get(bubble_type, self.app.feedback_bubble)
        align_right = bubble_type == "answer"
        bubble = Bubble(text, img, bubble_type, align_right)
        wrapper = QWidget()
        wrapper.setAttribute(Qt.WA_TranslucentBackground)
        layout = QHBoxLayout(wrapper)
        layout.setContentsMargins(30, 5, 30, 5)
        if align_right:
            layout.addStretch()
            layout.addWidget(bubble)
        else:
            layout.addWidget(bubble)
            layout.addStretch()
        self.app.chat_layout.addWidget(wrapper)
        QTimer.singleShot(100, lambda: self.app.scroll_area.verticalScrollBar().setValue(self.app.scroll_area.verticalScrollBar().maximum()))

    def add_emote(self, emote_path):
        emote_label = QLabel()
        pix = QPixmap(emote_path)
        pix = pix.scaledToWidth(120, Qt.SmoothTransformation)
        emote_label.setPixmap(pix)
        emote_label.setStyleSheet("background: transparent;")

        wrapper = QWidget()
        layout = QHBoxLayout(wrapper)
        layout.setContentsMargins(60, 5, 30, 5)
        layout.addWidget(emote_label, alignment=Qt.AlignLeft)
        self.app.chat_layout.addWidget(wrapper)