from PySide6.QtWidgets import QMainWindow, QStackedWidget
from components.LetterPage import LetterPage
from HandRecognizer import HandRecognizer
import string

class ASLLearner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASL Learner")
        self.setMinimumSize(800, 800)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.recognizer = HandRecognizer()

        self.letters = list(string.ascii_uppercase)
        self.current_index = 0

        self.lesson_pages = []
        for letter in self.letters:
            page = LetterPage(letter, self.recognizer, self.next_letter)
            self.stack.addWidget(page)
            self.lesson_pages.append(page)

        self.stack.setCurrentWidget(self.lesson_pages[0])

    def return_home(self):
        self.close()

    def next_letter(self):
        self.current_index += 1
        if self.current_index < len(self.lesson_pages):
            self.stack.setCurrentWidget(self.lesson_pages[self.current_index])
        else:
            self.close()
