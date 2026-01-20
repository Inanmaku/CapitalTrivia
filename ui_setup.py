import os
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QScrollArea, QPushButton, QFrame
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase

from ui_components import StarLabel, StarEditBubble


class UiSetup:
    def __init__(self, app):
        self.app = app
        self.setup_paths()
        self.setup_variables()
        self.init_ui()

    def setup_paths(self):
        self.app.assets_path = "assets"
        self.app.background = os.path.join(self.app.assets_path, "background.png")
        self.app.extra_background = os.path.join(self.app.assets_path, "extrabackground.png")
        self.app.menu_background = os.path.join(self.app.assets_path, "menu.png")
        self.app.frame = os.path.join(self.app.assets_path, "frame.png")
        self.app.question_bubble = os.path.join(self.app.assets_path, "question.png")
        self.app.answer_bubble = os.path.join(self.app.assets_path, "answer.png")
        self.app.feedback_bubble = os.path.join(self.app.assets_path, "correctorwrong.png")

    def setup_variables(self):
        self.app.star_positions = [
            (170, 125, 60, 60), (220, 125, 60, 60), (270, 125, 60, 60), (320, 125, 60, 60),
            (170, 175, 60, 60), (220, 175, 60, 60), (270, 175, 60, 60), (320, 178, 60, 60),
        ]
        self.app.menu_btn_size = (40, 40)
        self.app.menu_btn_pos = (430 - self.app.menu_btn_size[0] - 70, 55)
        self.app.back_btn_size = (250, 60)
        self.app.back_btn_pos = (130, 170)

    def init_ui(self):
        self.setup_backgrounds()
        self.setup_scroll_area()
        self.setup_input()
        self.setup_menu_elements()
        self.setup_edit_elements()
        self.setup_window_controls()
        self.setup_stars()
        self.setup_layering()

    def setup_backgrounds(self):
        self.app.bg_label = QLabel(self.app)
        if os.path.exists(self.app.background):
            self.app.bg_label.setPixmap(QPixmap(self.app.background))
        self.app.bg_label.setScaledContents(True)
        self.app.bg_label.setGeometry(0, 0, 430, 800)
        self.app.bg_label.lower()

        self.app.extra_bg_label = QLabel(self.app)
        if os.path.exists(self.app.extra_background):
            self.app.extra_bg_label.setPixmap(QPixmap(self.app.extra_background))
        self.app.extra_bg_label.setScaledContents(True)
        self.app.extra_bg_label.setGeometry(0, 0, 430, 800)
        self.app.extra_bg_label.raise_()

        self.app.frame_label = QLabel(self.app)
        if os.path.exists(self.app.frame):
            self.app.frame_label.setPixmap(QPixmap(self.app.frame))
        self.app.frame_label.setScaledContents(True)
        self.app.frame_label.setGeometry(0, 0, 430, 800)
        self.app.frame_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def setup_scroll_area(self):
        self.app.scroll_area = QScrollArea(self.app)
        self.app.scroll_area.setGeometry(20, 110, 390, 588)
        self.app.scroll_area.setStyleSheet(
            "QScrollArea { background: transparent; border: 0px; outline: none; } QScrollArea:focus { outline: none; } QWidget { background: transparent; } QScrollBar:vertical { width: 0px; background: transparent; }"
        )
        self.app.scroll_area.setFrameShape(QFrame.NoFrame)
        self.app.scroll_area.setWidgetResizable(True)
        self.app.scroll_area.setFocusPolicy(Qt.StrongFocus)
        self.app.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.app.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.app.chat_widget = QWidget()
        self.app.chat_widget.setAttribute(Qt.WA_TranslucentBackground)
        self.app.chat_layout = QVBoxLayout(self.app.chat_widget)
        self.app.chat_layout.setAlignment(Qt.AlignTop)
        self.app.chat_layout.setContentsMargins(10, 10, 10, 10)
        self.app.chat_layout.setSpacing(8)
        self.app.scroll_area.setWidget(self.app.chat_widget)
        self.app.scroll_area.viewport().setAttribute(Qt.WA_TransparentForMouseEvents, False)

    def setup_input(self):
        self.app.answer_box = QLineEdit(self.app)
        self.app.answer_box.setGeometry(72, 712, 280, 34)
        self.app.answer_box.setPlaceholderText("Type your answer...")
        self.app.answer_box.setStyleSheet("border: none; background: transparent; font-size: 12px; color: black;")
        self.app.answer_box.returnPressed.connect(self.app.quiz_logic.check_answer)

        self.app.send_button = QPushButton("", self.app)
        self.app.send_button.setGeometry(330, 712, 30, 30)
        self.app.send_button.setStyleSheet("background: transparent; border: none;")
        self.app.send_button.clicked.connect(self.app.quiz_logic.check_answer)

    def setup_menu_elements(self):
        self.app.menu_label = QLabel(self.app)
        if os.path.exists(self.app.menu_background):
            self.app.menu_label.setPixmap(QPixmap(self.app.menu_background))
        self.app.menu_label.setScaledContents(True)
        self.app.menu_label.setGeometry(0, 0, 430, 800)
        self.app.menu_label.hide()

        self.app.menu_button = QPushButton("", self.app)
        self.app.menu_button.setGeometry(*self.app.menu_btn_pos, *self.app.menu_btn_size)
        self.app.menu_button.setStyleSheet("background: transparent; border: none;")
        self.app.menu_button.clicked.connect(self.app.show_menu)
        self.app.menu_button.setToolTip("Open menu")

        self.app.back_button = QPushButton("", self.app)
        self.app.back_button.setGeometry(*self.app.back_btn_pos, *self.app.back_btn_size)
        self.app.back_button.setStyleSheet("background: transparent; border: none;")
        self.app.back_button.clicked.connect(self.app.hide_menu)
        self.app.back_button.hide()
        self.app.back_button.setToolTip("Back")

        self.app.edit_menu_button = QPushButton("", self.app)
        self.app.edit_menu_button.setGeometry(65, 182, 42, 42)
        self.app.edit_menu_button.setStyleSheet("background: transparent; border: none;")
        self.app.edit_menu_button.clicked.connect(self.app.edit_manager.show_edit_page)
        self.app.edit_menu_button.hide()

    def setup_edit_elements(self):
        self.app.edit_label = QLabel(self.app)
        edit_path = os.path.join(self.app.assets_path, "editpage.png")
        if os.path.exists(edit_path):
            self.app.edit_label.setPixmap(QPixmap(edit_path))
        self.app.edit_label.setScaledContents(True)
        self.app.edit_label.setGeometry(0, 0, 430, 800)
        self.app.edit_label.hide()

        self.app.edit_bar_label = QLabel(self.app)
        edit_bar_path = os.path.join(self.app.assets_path, "editbar.png")
        if os.path.exists(edit_bar_path):
            self.app.edit_bar_label.setPixmap(QPixmap(edit_bar_path))
        self.app.edit_bar_label.setScaledContents(True)
        self.app.edit_bar_label.setGeometry(0, 0, 430, 800)
        self.app.edit_bar_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.app.edit_bar_label.hide()

        self.app.edit_scroll = QScrollArea(self.app)
        self.app.edit_scroll.setGeometry(48, 113, 350, 680)
        self.app.edit_scroll.setStyleSheet("background: transparent; border: 0px; outline: none; QScrollArea:focus { outline: none; } QScrollBar:vertical { width: 0px; background: transparent; }")
        self.app.edit_scroll.setFrameShape(QFrame.NoFrame)
        self.app.edit_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.app.edit_scroll.setWidgetResizable(True)
        self.app.edit_scroll.hide()

        self.app.edit_widget = QWidget()
        self.app.edit_widget.setAttribute(Qt.WA_TranslucentBackground)
        self.app.edit_layout = QVBoxLayout(self.app.edit_widget)
        self.app.edit_layout.setContentsMargins(10, 10, 10, 10)
        self.app.edit_layout.setSpacing(8)
        self.app.edit_scroll.setWidget(self.app.edit_widget)
        self.app.edit_scroll.viewport().setAttribute(Qt.WA_TranslucentBackground)

        self.app.edit_back_button = QPushButton("", self.app)
        self.app.edit_back_button.setGeometry(320, 60, 40, 30)
        self.app.edit_back_button.setStyleSheet("background: transparent; border: none;")
        self.app.edit_back_button.clicked.connect(self.app.edit_manager.save_edit_changes)
        self.app.edit_back_button.hide()

        self.app.edit_toggle_remove_button = QPushButton("", self.app)
        self.app.edit_toggle_remove_button.setGeometry(65, 140, 40, 30)
        self.app.edit_toggle_remove_button.setStyleSheet("background: transparent; border: none; color: transparent; font-size: 12px; opacity: 0;")
        self.app.edit_toggle_remove_button.clicked.connect(self.app.edit_manager.toggle_remove_buttons)
        self.app.edit_toggle_remove_button.hide()
        self.app.edit_toggle_remove_button.setToolTip("Toggle remove buttons")

        self.app.restart_button = QPushButton("", self.app)
        self.app.restart_button.setGeometry(65, 180, 40, 30)
        self.app.restart_button.setStyleSheet("background: transparent; border: none; color: transparent; font-size: 12px; opacity: 0;")
        self.app.restart_button.clicked.connect(self.app.edit_manager.restart_questions)
        self.app.restart_button.hide()
        self.app.restart_button.setToolTip("Restart to original questions")

        self.app.edit_toggle_bar_button = QPushButton(" ", self.app)
        self.app.edit_toggle_bar_button.setGeometry(72, 53, 30, 30)
        self.app.edit_toggle_bar_button.setStyleSheet("background: transparent; border: none;")
        self.app.edit_toggle_bar_button.clicked.connect(self.app.edit_manager.toggle_edit_bar)
        self.app.edit_toggle_bar_button.hide()
        self.app.edit_toggle_bar_button.setToolTip("Toggle edit bar")

    def setup_window_controls(self):
        self.app.clock_label = QLabel(self.app)
        self.app.clock_label.setGeometry(73, 20, 100, 30)
        self.app.clock_label.setStyleSheet("color: black; background: transparent;")
        self.app.clock_label.setFont(QFont("Arial", 7, QFont.Bold))
        self.app.clock_timer = QTimer(self.app)
        self.app.clock_timer.timeout.connect(lambda: self.app.clock_label.setText(QTime.currentTime().toString("hh:mm")))
        self.app.clock_timer.start(1000)

        self.app.close_button = QPushButton("✕", self.app)
        self.app.close_button.setGeometry(390, 15, 25, 25)
        self.app.close_button.setStyleSheet("""
            QPushButton {
                color: transparent;
                background: transparent;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                color: red;
            }
        """)
        self.app.close_button.clicked.connect(self.app.confirm_close)
        self.app.close_button.setToolTip("Close")

        self.app.minimize_button = QPushButton("–", self.app)
        self.app.minimize_button.setGeometry(360, 15, 25, 25)
        self.app.minimize_button.setStyleSheet("""
            QPushButton {
                color: transparent;
                background: transparent;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                color: red;
            }
        """)
        self.app.minimize_button.clicked.connect(self.app.showMinimized)
        self.app.minimize_button.setToolTip("Minimize")

    def setup_stars(self):
        self.app.star_labels = []
        self.app.star_edit_bubbles = []
        for i, (x, y, w, h) in enumerate(self.app.star_positions, 1):
            star_bubble = StarEditBubble(i, x, y, w, h, self.app.assets_path)
            star_bubble.setParent(self.app)
            star_bubble.hide()
            self.app.star_edit_bubbles.append(star_bubble)
        self.app.star_display_labels = []
        for i, (x, y, w, h) in enumerate(self.app.star_positions, 1):
            star_label = StarLabel(i, self.app)
            star_path = os.path.join(self.app.assets_path, f"{i}star.png")
            if os.path.exists(star_path):
                star_label.setPixmap(QPixmap(star_path))
            star_label.setScaledContents(True)
            star_label.setGeometry(x, y, w, h)
            star_label.hide()
            star_label.setAttribute(Qt.WA_TransparentForMouseEvents, False)
            self.app.star_display_labels.append(star_label)

    def setup_layering(self):
        self.app.bg_label.lower()
        self.app.extra_bg_label.raise_()
        self.app.scroll_area.raise_()
        self.app.menu_label.raise_()
        self.app.edit_label.raise_()
        self.app.edit_bar_label.raise_()
        self.app.edit_scroll.raise_()
        self.app.frame_label.raise_()
        self.app.answer_box.raise_()
        self.app.send_button.raise_()
        self.app.clock_label.raise_()
        self.app.menu_button.raise_()
        self.app.back_button.raise_()
        self.app.close_button.raise_()
        self.app.minimize_button.raise_()

        self.app.menu_label.installEventFilter(self.app)
        self.app.frame_label.installEventFilter(self.app)
        self.app.edit_label.installEventFilter(self.app)