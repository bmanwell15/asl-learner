import sys
import os
import cv2
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QImage, QPixmap, QFont
from PySide6.QtCore import Qt, QTimer

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from HandRecognizer import HandRecognizer


class LessonPage(QWidget):
    def __init__(self, lesson_letters=None, index=0, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Lesson 1")
        self.setFixedSize(360, 640)
        self.handRecognizer = HandRecognizer()
        self.lesson_letters = lesson_letters or ["A", "B", "C"]
        #self.lesson_letters = lesson_letters or list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.index = index
        self.target_symbol = self.lesson_letters[self.index]
        self.awaiting_reset = False  # Flag to block repeated correct triggers

        self.init_ui()
        self.start_camera()

    def init_ui(self):
        self.setStyleSheet("background: transparent;")

        # Camera display as background
        self.camera_label = QLabel(self)
        self.camera_label.setGeometry(0, 0, 360, 640)
        self.camera_label.setStyleSheet("background-color: transparent;")
        self.camera_label.setScaledContents(True)

        # Back button
        self.back_btn = QPushButton("←", self)
        self.back_btn.setGeometry(10, 10, 30, 30)
        self.back_btn.setStyleSheet("font-size: 20px; background: transparent; border: none;")
        self.back_btn.clicked.connect(self.go_back)
        # Steak point
        self.streak_label = QLabel("5 🔥", self)
        self.streak_label.setGeometry(310, 10, 40, 30)
        self.streak_label.setStyleSheet("background: transparent; color: #a139e8; font-size: 14px; border: none;")
        # Letter display 
        self.letter_label = QLabel("-", self)
        self.letter_label.setGeometry(160, 60, 40, 40)
        self.letter_label.setStyleSheet("background: transparent;")
        self.letter_label.setFont(QFont("Arial", 60))
        self.letter_label.setAlignment(Qt.AlignCenter)
        #Letter by Upload Image
        #self.sign_img = QLabel(self)
        #self.sign_img.setGeometry(80, 130, 200, 200)
        #sign_img_path = f"LBlack_{self.target_symbol}.png"
        #if os.path.exists(sign_img_path):
           # self.sign_img.setPixmap(QPixmap(sign_img_path).scaled(200, 200, Qt.KeepAspectRatio))
        #else:
           # self.sign_img.setText(self.target_symbol)
           # self.sign_img.setAlignment(Qt.AlignCenter)
           # self.sign_img.setStyleSheet("background: transparent; border: none;")
           
# Make the camera fit the UI screen (LOW KEY LAGGY maybe because of conflict with HandRecognizer.py)
    def start_camera(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        if not self.handRecognizer.isCamaraOpen:
            return

        ret, frame = self.handRecognizer.camaraCapture.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qt_img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_img).scaled(
            self.camera_label.width(),
            self.camera_label.height(),
            Qt.KeepAspectRatio,  # preserve aspect ratio
            Qt.SmoothTransformation  # optional: better quality scaling
        )
        self.camera_label.setPixmap(pixmap)
        
        symbol = self.handRecognizer.getCurrentHandSymbol()

        # Always display the target letter
        self.letter_label.setText(self.target_symbol)

        if symbol == self.target_symbol:
            # Correct
            self.letter_label.setStyleSheet("color: green; background: transparent;")
            #self.sign_img.setStyleSheet("border: none; background: transparent;")
            
        
        else:
            # Incorrect or nothing detected
            self.letter_label.setStyleSheet("color: black; background: transparent;")
            # self.sign_img.setStyleSheet("border: none; background: transparent;")
   
   
    def closeEvent(self, event):
        self.handRecognizer.closeCamara()
        self.timer.stop()
        event.accept()

    def go_back(self):
        self.close()
        if self.parent():
            self.parent().show()
