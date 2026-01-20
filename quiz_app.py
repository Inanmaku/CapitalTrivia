import sys
import os
import pickle
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFontDatabase

from data import COUNTRIES, ASSETS_PATH, EMOTES
from ui_setup import UiSetup
from quiz_logic import QuizLogic
from edit_manager import EditManager
from progress_manager import ProgressManager


class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capital Trivia")
        self.resize(430, 850)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.drag_position = None

        font_path = os.path.join("assets", "Alice-Regular.ttf")
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)

        self.emotes = EMOTES

        self.all_countries = [country for group in COUNTRIES for country in group]
        try:
            with open('countries.pkl', 'rb') as f:
                self.all_countries = pickle.load(f)
        except FileNotFoundError:
            pass
        self.countries = self.all_countries[:]
        self.groups = [[c for c in group if c in self.all_countries] for group in COUNTRIES]
        self.known_set = {c: {"correct": False, "attempts": 0} for c, _ in self.countries}
        self.q_index = None
        self.previous_question = None
        self.groups = COUNTRIES[:]
        self.group_index = 0
        self.current_questions = []
        self.correct_set = set()
        self.attempts = {}
        self.last_question = None
        self.current_country = None
        self.deferred = {}
        self.menu_open = False
        self.edit_bar_active = False

        self.selected_star = None
        self.duplicated_stars = []

        self.quiz_logic = QuizLogic(self)
        self.edit_manager = EditManager(self)
        self.progress_manager = ProgressManager(self)
        self.ui_setup = UiSetup(self)

        self.progress_manager.load_progress()
        if self.q_index is None:
            self.quiz_logic.load_next_group()
            self.quiz_logic.load_question()





    def confirm_close(self):
        if self.edit_label.isVisible():
            self.edit_manager.save_edit_changes()
        msg = QMessageBox(self)
        msg.setWindowTitle('Save Progress')
        msg.setText('Do you want to save your progress before closing?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        msg.setStyleSheet("QMessageBox { background-color: #E6E6FA; font-size: 10px; }")
        msg.setMinimumSize(300, 120)
        cancel_button = msg.button(QMessageBox.Cancel)
        if cancel_button:
            cancel_button.hide()
        reply = msg.exec_()
        if reply == QMessageBox.Yes:
            self.progress_manager.save_progress()
            self.close()
        elif reply == QMessageBox.No:
            try:
                os.remove('progress.pkl')
                os.remove('countries.pkl')
            except FileNotFoundError:
                pass
            self.close()

    def show_menu(self):
        self.menu_label.show()
        self.menu_label.raise_()
        self.frame_label.raise_()

        self.scroll_area.hide()
        self.answer_box.hide()
        self.send_button.hide()
        self.menu_button.hide()

        self.back_button.show()
        self.back_button.raise_()
        self.edit_menu_button.show()
        self.edit_menu_button.raise_()

        self.clock_label.raise_()
        self.close_button.raise_()
        self.minimize_button.raise_()

    def hide_menu(self):
        self.menu_label.hide()
        self.scroll_area.show()
        self.scroll_area.raise_()
        self.answer_box.show()
        self.send_button.show()
        self.back_button.hide()
        self.menu_button.show()
        self.menu_button.raise_()
        self.edit_menu_button.hide()
        self.frame_label.raise_()
        self.close_button.raise_()
        self.clock_label.raise_()

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.Show, QEvent.Paint):
            self.close_button.raise_()
            self.minimize_button.raise_()
            self.answer_box.raise_()
            self.send_button.raise_()

        return super().eventFilter(obj, event)



    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.edit_bar_active:
                return  
            self.drag_position = e.globalPos() - self.frameGeometry().topLeft()
            e.accept()

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton and self.drag_position is not None:
            self.move(e.globalPos() - self.drag_position)
            e.accept()




