import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

from data import COUNTRIES
from ui_components import EditBubble


class EditManager:
    def __init__(self, app):
        self.app = app

    def show_edit_page(self):
        self.app.menu_label.hide()
        self.app.edit_menu_button.hide()
        self.app.back_button.hide()

        self.app.extra_bg_label.lower()

        self.app.edit_label.show()
        self.app.edit_label.raise_()
        self.app.edit_scroll.show()
        self.app.edit_scroll.raise_()
        self.app.edit_back_button.show()
        self.app.edit_back_button.raise_()
        self.app.edit_toggle_bar_button.show()
        self.app.edit_toggle_bar_button.raise_()
        self.app.restart_button.show()
        self.app.restart_button.raise_()

        self.load_edit_page()

        self.app.close_button.raise_()
        self.app.minimize_button.raise_()
        self.app.clock_label.raise_()
        self.app.edit_toggle_remove_button.raise_()
        self.app.edit_toggle_bar_button.raise_()
        self.app.restart_button.raise_()
        self.app.edit_back_button.raise_()
        self.app.frame_label.raise_()

    def hide_edit_page(self):
        self.app.edit_label.hide()
        self.app.edit_scroll.hide()
        self.app.edit_back_button.hide()
        self.app.edit_toggle_remove_button.hide()
        self.app.edit_toggle_bar_button.hide()
        self.app.restart_button.hide()
        self.app.edit_bar_label.hide()
        for star_label in self.app.star_display_labels:
            star_label.hide()

        self.app.extra_bg_label.raise_()

        self.app.menu_label.show()
        self.app.back_button.show()
        self.app.edit_menu_button.show()
        self.app.menu_label.raise_()
        self.app.back_button.raise_()
        self.app.edit_menu_button.raise_()
        self.app.clock_label.raise_()
        self.app.close_button.raise_()
        self.app.minimize_button.raise_()
        self.app.frame_label.raise_()

        self.app.selected_star = None

    def load_edit_page(self):
        for i in reversed(range(self.app.edit_layout.count())):
            widget = self.app.edit_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.app.edit_bubbles = []
        for country, capital in self.app.all_countries:
            bubble = EditBubble(country, capital)
            bubble.remove_button.clicked.connect(lambda _, b=bubble: self.remove_bubble(b))
            bubble.remove_button.hide()
            self.app.edit_layout.addWidget(bubble)
            self.app.edit_bubbles.append(bubble)

        self.app.add_bubble = EditBubble(is_add_new=True)
        self.app.add_bubble.add_button.clicked.connect(self.add_new_entry)
        self.app.edit_layout.addWidget(self.app.add_bubble)

        spacer = QWidget()
        spacer.setFixedHeight(100)
        self.app.edit_layout.addWidget(spacer)

        for bubble in self.app.edit_bubbles + [self.app.add_bubble]:
            bubble.installEventFilter(self.app)

    def remove_bubble(self, bubble):
        if bubble in self.app.edit_bubbles:
            self.app.edit_bubbles.remove(bubble)
            bubble.setParent(None)
            self.app.edit_layout.removeWidget(bubble)

    def add_new_entry(self):
        new_bubble = EditBubble()
        new_bubble.remove_button.clicked.connect(lambda _, b=new_bubble: self.remove_bubble(b))
        new_bubble.remove_button.hide()
        self.app.edit_layout.insertWidget(len(self.app.edit_bubbles), new_bubble)
        self.app.edit_bubbles.append(new_bubble)
        QTimer.singleShot(100, lambda: self.app.edit_scroll.ensureWidgetVisible(new_bubble))

    def toggle_remove_buttons(self):
        for bubble in self.app.edit_bubbles:
            if bubble.remove_button.isVisible():
                bubble.remove_button.hide()
            else:
                bubble.remove_button.show()

    def toggle_edit_bar(self):
        if self.app.edit_bar_label.isVisible():
            self.app.edit_bar_label.hide()
            for star_label in self.app.star_display_labels:
                star_label.hide()
            self.app.edit_toggle_remove_button.hide()
            for bubble in self.app.edit_bubbles:
                bubble.question_edit.setEnabled(True)
                bubble.answer_edit.setEnabled(True)
        else:
            self.app.edit_bar_label.show()
            self.app.edit_bar_label.raise_()
            for star_label in self.app.star_display_labels:
                star_label.show()
                star_label.raise_()
            self.app.edit_toggle_remove_button.show()
            self.app.edit_toggle_remove_button.raise_()
            self.app.edit_toggle_bar_button.raise_()
            self.app.restart_button.raise_()
            self.app.edit_back_button.raise_()
            self.app.clock_label.raise_()
            self.app.close_button.raise_()
            self.app.minimize_button.raise_()
            self.app.frame_label.raise_()

            for star in self.app.duplicated_stars:
                star.raise_()

            self.app.selected_star = None
            self.reset_star_sizes()

            for bubble in self.app.edit_bubbles:
                bubble.question_edit.setEnabled(False)
                bubble.answer_edit.setEnabled(False)

    def save_edit_changes(self):
        new_countries = []
        for bubble in self.app.edit_bubbles:
            question = bubble.question_edit.text().strip()
            answer = bubble.answer_edit.text().strip()
            if question or answer:
                if not question:
                    question = "Question"
                if not answer:
                    answer = "Answer"
                new_countries.append((question, answer))

        if not new_countries:
            return

        self.app.all_countries = new_countries
        self.app.countries = self.app.all_countries[:]

        self.app.groups = []
        for group in COUNTRIES:
            filtered = [c for c in group if c in new_countries]
            if filtered:
                self.app.groups.append(filtered)
        remaining = [c for c in new_countries if not any(c in g for g in self.app.groups)]
        for i in range(0, len(remaining), 20):
            self.app.groups.append(remaining[i:i+20])

        with open('countries.pkl', 'wb') as f:
            import pickle
            pickle.dump(new_countries, f)

        new_known_set = {}
        for country, capital in new_countries:
            if country in self.app.known_set:
                new_known_set[country] = self.app.known_set[country]
            else:
                new_known_set[country] = {"correct": False, "attempts": 0}
        self.app.known_set = new_known_set

        self.app.correct_set = {c for c, info in self.app.known_set.items() if info["correct"]}

        self.app.q_index = None
        self.app.previous_question = None
        self.app.group_index = 0
        self.app.current_questions = []
        self.app.attempts = {}
        self.app.last_question = None
        self.app.current_country = None
        self.app.deferred = {}

        # Clear the chat to prevent duplicate messages
        for i in reversed(range(self.app.chat_layout.count())):
            widget = self.app.chat_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.hide_edit_page()
        self.app.quiz_logic.load_question()

    def restart_questions(self):
        self.app.all_countries = [country for group in COUNTRIES for country in group]
        self.app.countries = self.app.all_countries[:]
        self.app.groups = COUNTRIES[:]

        try:
            os.remove('countries.pkl')
        except FileNotFoundError:
            pass

        self.app.known_set = {c: {"correct": False, "attempts": 0} for c, _ in self.app.countries}

        self.app.q_index = None
        self.app.previous_question = None
        self.app.group_index = 0
        self.app.current_questions = []
        self.app.correct_set = set()
        self.app.attempts = {}
        self.app.last_question = None
        self.app.current_country = None
        self.app.deferred = {}

        self.load_edit_page()

    def select_star(self, index):
        if self.app.selected_star is not None:
            self.reset_star_sizes()

        self.app.selected_star = index
        star_label = self.app.star_display_labels[index - 1]
        star_label.setGeometry(star_label.x() - 10, star_label.y() - 10, 80, 80)
        star_label.raise_()

    def reset_star_sizes(self):
        for i, star_label in enumerate(self.app.star_display_labels):
            x, y, w, h = self.app.star_positions[i]
            star_label.setGeometry(x, y, w, h)

    def duplicate_star_on_bubble(self, bubble, click_pos):
        star_label = QLabel(self.app.edit_scroll.widget())
        star_path = os.path.join(self.app.assets_path, f"{self.app.selected_star}star.png")
        if os.path.exists(star_path):
            star_label.setPixmap(QPixmap(star_path))
        star_label.setScaledContents(True)
        star_label.setFixedSize(40, 40)

        bubble_pos = bubble.mapTo(self.app.edit_scroll.widget(), click_pos)
        star_label.move(bubble_pos.x() - 20, bubble_pos.y() - 20)
        star_label.show()
        star_label.raise_()

        star_label.setAttribute(Qt.WA_TransparentForMouseEvents, False)

        def prevent_drag(event):
            if event.button() == Qt.LeftButton:
                event.accept()
        star_label.mousePressEvent = prevent_drag

        star_label.position = (bubble_pos.x() - 20, bubble_pos.y() - 20)
        star_label.star_index = self.app.selected_star

        self.app.duplicated_stars.append(star_label)