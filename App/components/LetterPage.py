from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont, QPixmap
import os
from CamaraWidget import CameraWidget

class LetterPage(QWidget):
    def __init__(self, letter, recognizer, on_back, on_success, initCamera):
        super().__init__()
        self.letter = letter
        self.recognizer = recognizer
        self.on_back = on_back
        self.on_success = on_success

        self.init_ui(initCamera)
        self.start_detection()

    def init_ui(self, initCamera=False):
        self.setStyleSheet("QLabel { background: transparent; }")

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Add camera widget as base layer
        if initCamera:
            self.camera_widget = CameraWidget(self, self.recognizer)
            self.camera_widget.setFixedSize(360, 640)  # fill area
            layout.addWidget(self.camera_widget)

        # Overlay container (floats on top)
        overlay = QWidget(self)
        overlay.setAttribute(Qt.WA_TransparentForMouseEvents)  # allow interactions to pass through
        overlay.setStyleSheet("background: transparent;")
        overlay.setGeometry(0, 0, 360, 640)  # same as window size

        overlay_layout = QVBoxLayout(overlay)
        overlay_layout.setContentsMargins(20, 20, 20, 20)
        overlay_layout.setSpacing(20)
        overlay_layout.setAlignment(Qt.AlignTop)

        # Top bar
        top_bar = QHBoxLayout()
        back_btn = QPushButton("←")
        back_btn.setFont(QFont("Arial", 20))
        back_btn.setFixedSize(40, 40)
        back_btn.setStyleSheet("background: transparent; border: none; color: white;")
        back_btn.clicked.connect(self.on_back)

        self.streak_label = QLabel("5 🔥")
        self.streak_label.setFont(QFont("Arial", 16))
        self.streak_label.setStyleSheet("color: #a139e8;")

        top_bar.addWidget(back_btn)
        top_bar.addStretch()
        top_bar.addWidget(self.streak_label)
        overlay_layout.addLayout(top_bar)

        # Big letter
        self.letter_label = QLabel(self.letter)
        self.letter_label.setFont(QFont("Arial", 72, QFont.Bold))
        self.letter_label.setAlignment(Qt.AlignCenter)
        self.letter_label.setStyleSheet("color: white;")
        overlay_layout.addWidget(self.letter_label)

        # Sign image
        self.sign_image = QLabel()
        self.sign_image.setAlignment(Qt.AlignCenter)
        img_path = os.path.join("assets", "images", f"{self.letter}.png")
        if os.path.exists(img_path):
            self.sign_image.setPixmap(QPixmap(img_path).scaled(150, 150, Qt.KeepAspectRatio))
        else:
            self.sign_image.setText("Image not found")
            self.sign_image.setStyleSheet("color: white;")
        overlay_layout.addWidget(self.sign_image)

        # Feedback text
        self.feedback = QLabel("Try to form the sign")
        self.feedback.setFont(QFont("Arial", 16))
        self.feedback.setAlignment(Qt.AlignCenter)
        self.feedback.setStyleSheet("color: white;")
        overlay_layout.addWidget(self.feedback)

    def start_detection(self):
        self.timer = QTimer()
        # self.timer.timeout.connect(self.check_symbol)
        # self.timer.start(500)

    def check_symbol(self):
        symbol = self.recognizer.getCurrentHandSymbol()
        if symbol == self.letter:
            self.feedback.setText("✅ Correct!")
            self.letter_label.setStyleSheet("color: lightgreen;")
            self.timer.stop()
            QTimer.singleShot(1500, self.on_success)
        elif symbol:
            self.feedback.setText(f"❌ Detected: {symbol}")
            self.letter_label.setStyleSheet("color: white;")
        else:
            self.feedback.setText("❓ No hand detected")
            self.letter_label.setStyleSheet("color: white;")