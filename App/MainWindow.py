from PySide6.QtWidgets import QMainWindow, QWidget, QStackedWidget
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QIcon
from LetterPage import LetterPage
from WordPage import WordSpellingPage
from CamaraWidget import CameraWidget
from HandRecognizer import HandRecognizer
import Constants

class ASLLearner(QMainWindow):
    def __init__(self, main_window = None, start_lesson=1):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("ASL Learner")
        self.setWindowIcon(QIcon(Constants.NAUTILUS_LOGO_PATH))
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

        self.letters = Constants.AI_MODEL_LETTERS
        self.current_index = 0
        self.lesson_pages = []

        # Symbol detection timer
        self.detection_timer = QTimer()
        self.detection_timer.timeout.connect(self.detect_and_update)
        self.detection_timer.start(Constants.SYMBOL_DETECTION_INTERVAL_MS)
        # Start from correct lesson
        if start_lesson == 1:
            for letter in self.letters: 
                page = LetterPage(letter, self.recognizer, self.go_back, self.next_letter)
                self.stack.addWidget(page)
                self.lesson_pages.append(page)
            self.stack.setCurrentWidget(self.lesson_pages[0])
        elif start_lesson == 2:
            self.word_lesson = WordSpellingPage(self.recognizer,self.go_back,self.return_home)
            self.stack.addWidget(self.word_lesson)
            # Slight delay before switching to allow UI & camera to initialize
            QTimer.singleShot(50, lambda: self.stack.setCurrentWidget(self.word_lesson))

            # Force immediate camera draw to prevent flash
            QTimer.singleShot(60, self.camera_widget.updateFrame)
            #self.stack.setCurrentWidget(self.word_lesson)
            self.word_lesson.reset_lesson()
    #Back button
    def go_back(self):
        self.close()
        if self.main_window:
            self.main_window.show()
        self.recognizer.closeCamara()
        self.detection_timer.stop()
    
    def detect_and_update(self):
        current_widget = self.stack.currentWidget()
        if current_widget in self.lesson_pages:
            symbol = self.recognizer.getCurrentHandSymbol()
            current_index = self.lesson_pages.index(current_widget)
            current_widget.update_feedback(symbol)
    
    def return_home(self):
        self.stop_camera()
        self.detection_timer.stop()
        if self.main_window:
            self.main_window.unlock_lesson_2()
            self.main_window.learner_window = None  # clear reference
            self.main_window.show()
        self.deleteLater()  # destroy this window

    def next_letter(self):
        self.current_index += 1
        if self.current_index < len(self.lesson_pages):
            self.stack.setCurrentWidget(self.lesson_pages[self.current_index])
        else:
            # End of Lesson 1 → unlock and return to main page
            self.recognizer.closeCamara()
            self.detection_timer.stop()

            msg = QMessageBox(self)
            msg.setWindowTitle("Lesson 1 Complete")
            msg.setText("🎉 Well done, you have unlocked Lesson 2!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.buttonClicked.connect(self.return_home)
            msg.exec()
    def stop_camera(self):
        if hasattr(self, "recognizer"):
            self.recognizer.closeCamara()
        if hasattr(self, "camera_widget"):
            self.camera_widget.hide()
