from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPixmap
import os

class LetterPage(QWidget):
    def __init__(self, letter, recognizer, on_back, on_success):
        super().__init__()
        self.letter = letter
        self.recognizer = recognizer
        self.on_back = on_back
        self.on_success = on_success
        self.correct_detected = False

        self.init_ui()

    def init_ui(self):
        # Global style: transparent background and white text on top
        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
            QLabel {
                background-color: transparent;
                color: white;
            }
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 40, 20, 20) 
        layout.setSpacing(25)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        # Back button 
        top_bar = QHBoxLayout()
        back_btn = QPushButton("←")
        back_btn.setFont(QFont("Arial", 20))
        back_btn.setFixedSize(40, 40)
        back_btn.clicked.connect(self.go_back)
        
            
        self.streak_label = QLabel("5 🔥")
        self.streak_label.setFont(QFont("Arial", 16))
        self.streak_label.setStyleSheet("color: #a139e8;")  

        top_bar.addWidget(back_btn)
        top_bar.addStretch()
        top_bar.addWidget(self.streak_label)
        layout.addLayout(top_bar)

        self.letter_label = QLabel(self.letter)
        self.letter_label.setFont(QFont("Arial", 72, QFont.Bold))
        self.letter_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.letter_label)

        self.sign_image = QLabel()
        self.sign_image.setAlignment(Qt.AlignCenter)
        img_path = os.path.join("assets", f"{self.letter.upper()}.png")
        if os.path.exists(img_path):
            self.sign_image.setPixmap(QPixmap(img_path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.sign_image.setText("Image not found")
        layout.addWidget(self.sign_image)

        self.feedback = QLabel("Try to form the sign")
        self.feedback.setFont(QFont("Arial", 16))
        self.feedback.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.feedback)

    def update_feedback(self, symbol):
        if self.correct_detected:
            return

        if symbol == self.letter:
            self.feedback.setText("✅ Correct!")
            self.letter_label.setStyleSheet("color: lightgreen;")
            self.correct_detected = True
            QTimer.singleShot(1500, self.on_success)
        elif symbol:
            self.feedback.setText(f"❌ Detected: {symbol}")
            self.letter_label.setStyleSheet("color: white;")
        else:
            self.feedback.setText("❓ No hand detected")
            self.letter_label.setStyleSheet("color: white;")
            
    def go_back(self):
        self.on_back()