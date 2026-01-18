import sys
from PyQt5.QtWidgets import QApplication
from quiz_app import QuizApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizApp()
    window.show()
    sys.exit(app.exec_())