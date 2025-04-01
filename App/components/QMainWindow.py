from PySide6.QtWidgets import QMainWindow, QStackedWidget
from components.HomePage import HomePage
from components.LessonPage import LessonPage
from HandRecognizer import HandRecognizer
import string

class ASLLearner(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASL Learner")
        self.setMinimumSize(700,700)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.letters = list(string.ascii_uppercase)
        self.current_index = 0

        self.recognizer = HandRecognizer() #THIS NEED ADJUSTMENTS IN HandRecognizer.py TO WORK

        self.home_page = HomePage(self.start_lesson)
        self.stack.addWidget(self.home_page)

        #for each letter, create a new lesson page for it, adds the page to the stacked widget, and appends it to the list of lesson pages
        self.lesson_pages = list()
        for letter in self.letters:
            page = LessonPage(letter, self.recognizer, self.next_letter)
            self.stack.addWidget(page)
            self.lesson_pages.append(page)
        

    def start_lesson(self):
        #start lesson method - called when user clicks on start lesson
        self.current_index = 0
    
    def next_letter(self): 
        #next_letter method - called when the current letter is successfully completed (when user performs the correct sign)
        self.current_index += 1
        if self.current_index < len(self.lesson_pages):
            self.stack.setCurrentWidget(self.lesson_pages[self.current_index])
        else:
            self.stack.setCurrentWidget(self.home_page)

    def closeEvent(self, event):
        self.recognizer.release()
        super().closeEvent(event)