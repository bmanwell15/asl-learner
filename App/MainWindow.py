from PySide6.QtWidgets import QMainWindow, QWidget, QStackedLayout, QStackedWidget
from PySide6.QtCore import QTimer
from LetterPage import LetterPage
from CamaraWidget import CameraWidget
from HandRecognizer import HandRecognizer
import Constants

class ASLLearner(QMainWindow):
    def __init__(self, main_window = None):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("ASL Learner")
        self.setFixedSize(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT)
        
        # Central container (manual widget layering)
        self.container = QWidget(self)
        self.setCentralWidget(self.container)
        self.container.setFixedSize(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT)

        # Camera widget (background)
        self.recognizer = HandRecognizer()
        self.camera_widget = CameraWidget(self.container, self.recognizer)
        self.camera_widget.setGeometry(0, 0, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT)
        self.camera_widget.lower()  # keep behind

        # Letter pages (overlay)
        self.stack = QStackedWidget(self.container)
        self.stack.setGeometry(0, 0, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT)
        self.stack.raise_()  # force top visibility

        self.letters = list(Constants.AI_MODEL_LETTERS)
        self.current_index = 0
        self.lesson_pages = []
        
        for letter in self.letters: 
            page = LetterPage(letter, self.recognizer, self.go_back, self.next_letter)
            self.stack.addWidget(page)
            self.lesson_pages.append(page)

        self.stack.setCurrentWidget(self.lesson_pages[0])

        # Symbol detection timer
        self.detection_timer = QTimer()
        self.detection_timer.timeout.connect(self.detect_and_update)
        self.detection_timer.start(Constants.SYMBOL_DETECTION_INTERVAL_MS)
    #Back button
    def go_back(self):
        self.close()
        if self.main_window:
            self.main_window.show()
        self.recognizer.closeCamara()
        self.detection_timer.stop()
    def detect_and_update(self):
        symbol = self.recognizer.getCurrentHandSymbol()
        current_page = self.lesson_pages[self.current_index]
        current_page.update_feedback(symbol)

    def return_home(self):
        self.close()

    def next_letter(self):
        self.current_index += 1
        print("Switched to:", self.letters[self.current_index] if self.current_index < len(self.lesson_pages) else "END")
        if self.current_index < len(self.lesson_pages):
            self.stack.setCurrentWidget(self.lesson_pages[self.current_index])
        else:
            self.close()