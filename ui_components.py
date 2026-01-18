import os
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont


class StarLabel(QLabel):
    def __init__(self, index, parent=None):
        super().__init__(parent)
        self.index = index

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent().edit_manager.select_star(self.index)
            event.accept()


class Bubble(QWidget):
    def __init__(self, text, image_path, bubble_type="question", align_right=False):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.container = QWidget()
        c_layout = QVBoxLayout(self.container)
        c_layout.setSpacing(0)

        if bubble_type == "question":
            c_layout.setContentsMargins(60, 40, 60, 40)
        elif bubble_type == "answer":
            c_layout.setContentsMargins(30, 17, 40, 17)
        else:
            c_layout.setContentsMargins(44, 25, 30, 30)

        self.bg = QLabel(self.container)
        self.bg.setPixmap(QPixmap(image_path))
        self.bg.setScaledContents(True)
        self.bg.lower()

        self.text_label = QLabel(text, self.container)
        self.text_label.setWordWrap(True)
        self.text_label.setFont(QFont("Alice", 12))
        self.text_label.setStyleSheet("color: black; background: transparent;")
        c_layout.addWidget(self.text_label)

        layout.addWidget(self.container)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def resizeEvent(self, event):
        self.bg.resize(self.container.size())
        super().resizeEvent(event)


class StarEditBubble(QWidget):
    def __init__(self, index, x, y, w, h, assets_path):
        super().__init__()
        self.setGeometry(x, y, w, h)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.bg = QLabel(self)
        star_path = os.path.join(assets_path, f"{index}star.png")
        if os.path.exists(star_path):
            self.bg.setPixmap(QPixmap(star_path))
        self.bg.setScaledContents(True)
        self.bg.setGeometry(0, 0, w, h)


class EditBubble(QWidget):
    def __init__(self, question="", answer="", is_add_new=False):
        super().__init__()
        self.is_add_new = is_add_new
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.container = QWidget()
        c_layout = QVBoxLayout(self.container)
        c_layout.setContentsMargins(10, 20, 10, 20)
        c_layout.setSpacing(5)
        self.setFixedWidth(313)

        self.bg = QLabel(self.container)
        edit_bubble_path = os.path.join("assets", "editbubble.png")
        if os.path.exists(edit_bubble_path) and not is_add_new:
            self.bg.setPixmap(QPixmap(edit_bubble_path))
        self.bg.setScaledContents(True)
        self.bg.lower()

        if is_add_new:
            self.add_button = QPushButton("+")
            self.add_button.setFont(QFont("Arial", 20, QFont.Bold))
            self.add_button.setStyleSheet("""
                QPushButton {
                    color: white;
                    background: black;
                    border: none;
                    border-radius: 20px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background: #333;
                }
            """)
            self.add_button.setFixedSize(40, 40)
            c_layout.addWidget(self.add_button, alignment=Qt.AlignCenter)
        else:
            self.question_edit = QLineEdit(question)
            self.question_edit.setFont(QFont("Alice", 13))
            self.question_edit.setStyleSheet("color: black; background: transparent; border: none;")
            self.question_edit.setAlignment(Qt.AlignCenter)
            self.question_edit.setPlaceholderText("Question")

            self.answer_edit = QLineEdit(answer)
            self.answer_edit.setFont(QFont("Alice", 13))
            self.answer_edit.setStyleSheet("color: black; background: transparent; border: none;")
            self.answer_edit.setAlignment(Qt.AlignCenter)
            self.answer_edit.setPlaceholderText("Answer")

            self.remove_button = QPushButton("🗑️", self.container)
            self.remove_button.setFont(QFont("Arial", 14))
            self.remove_button.setStyleSheet("""
                QPushButton {
                    color: black;
                    background: rgba(255,255,255,0.8);
                    border: none;
                    border-radius: 10px;
                    padding: 2px;
                }
                QPushButton:hover {
                    background: rgba(255,255,255,1.0);
                }
            """)
            self.remove_button.setFixedSize(25, 25)
            self.remove_button.move(288, 5)  

            c_layout.addWidget(self.question_edit)
            c_layout.addWidget(self.answer_edit)

        layout.addWidget(self.container)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def resizeEvent(self, event):
        self.bg.resize(self.container.size())
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            main_window = self.window()
            if hasattr(main_window, 'edit_manager') and main_window.selected_star is not None:
                main_window.edit_manager.duplicate_star_on_bubble(self, event.pos())
                event.accept()
                return True
        super().mousePressEvent(event)