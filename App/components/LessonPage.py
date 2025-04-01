from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap, QFont, QImage
import cv2

class LetterPage(QWidget):
    def __init__(self, letter, recognizer, go_to_next_letter):
        super().__init__()
        self.letter = letter
        self.recognizer = recognizer
        self.go_to_next_letter = go_to_next_letter