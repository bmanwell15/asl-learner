from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPixmap
import os
import Constants

class WordSpellingPage(QWidget):
    def __init__(self, recognizer, on_back, on_complete):
        super().__init__()
        self.recognizer = recognizer
        self.on_back = on_back
        self.on_complete = on_complete

        self.words = ["CLIP", "BARK", "SHOE", "FEED", "DESK", "CHOIR"]
        self.current_word_index = 0
        self.current_letter_index = 0
        self.correct_detected = False
        self.is_active = True  # Used to prevent QTimer from acting on deleted widgets

        self.init_ui()
        self.update_display()

        self.timer = QTimer()
        self.timer.timeout.connect(self.detect)
        self.timer.start(500)

    def init_ui(self):
        self.setStyleSheet("""
            QLabel { color: white; background-color: transparent; }
            QPushButton { background-color: transparent; color: white; border: none; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 40, 20, 20)
        layout.setSpacing(25)
        layout.setAlignment(Qt.AlignTop)

        # Top bar
        top_bar = QHBoxLayout()
        self.back_btn = QPushButton("←")
        self.back_btn.setFont(QFont("Arial", 20))
        self.back_btn.setFixedSize(40, 40)
        self.back_btn.clicked.connect(self.go_back)

        self.streak_label = QLabel("5 🔥")
        self.streak_label.setFont(QFont("Arial", 16))
        self.streak_label.setStyleSheet("color: #a139e8;")

        top_bar.addWidget(self.back_btn)
        top_bar.addStretch()
        top_bar.addWidget(self.streak_label)
        layout.addLayout(top_bar)

        self.word_label = QLabel()
        self.word_label.setFont(QFont("Arial", 36, QFont.Bold))
        self.word_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.word_label)

        self.sign_image = QLabel()
        self.sign_image.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.sign_image)

        self.feedback_label = QLabel("Sign the first letter")
        self.feedback_label.setFont(QFont("Arial", 18))
        self.feedback_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.feedback_label)

    def update_display(self):
        word = self.words[self.current_word_index]
        highlighted = ""
        for i, letter in enumerate(word):
            if i < self.current_letter_index:
                highlighted += f"<span style='color: lightgreen;'>{letter}</span>"
            elif i == self.current_letter_index:
                highlighted += f"<u>{letter}</u>"
            else:
                highlighted += letter
        self.word_label.setText(highlighted)

        self.current_letter = word[self.current_letter_index]
        self.img_path = os.path.normpath(os.path.join(Constants.BASE_DIRECTORY, "..", "Assets", f"{self.current_letter.upper()}.png"))
        #green_img_path = self.img_path.replace(".png", "_green.png")

        if os.path.exists(self.img_path):
            self.sign_image.setPixmap(QPixmap(self.img_path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.sign_image.setText("Image not found")

    def detect(self):
        if not self.is_active or self.correct_detected:
            return

        symbol = self.recognizer.getCurrentHandSymbol()
        word = self.words[self.current_word_index]
        target_letter = word[self.current_letter_index]

        if symbol == target_letter:
            self.correct_detected = True
            self.feedback_label.setText(f"✅ {symbol} is correct!")
            green_img_path = self.img_path.replace(".png", "_green.png")
            if os.path.exists(green_img_path):
                self.sign_image.setPixmap(QPixmap(green_img_path).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            self.current_letter_index += 1

            if self.current_letter_index >= len(word):
                self.current_word_index += 1
                self.current_letter_index = 0

                if self.current_word_index >= len(self.words):
                    self.timer.stop()
                    self.feedback_label.setText("🎉 All words completed!")
                    QTimer.singleShot(2000, self.on_complete)
                    return
                else:
                    QTimer.singleShot(1000, lambda: self.is_active and self.feedback_label.setText("Next word. Get ready!"))
                    QTimer.singleShot(1500, lambda: self.is_active and (self.update_display(), self.reset_flag()))
            else:
                QTimer.singleShot(1000, lambda: self.is_active and self.feedback_label.setText("Sign the next letter"))
                QTimer.singleShot(1200, self.reset_flag)
            self.update_display()
        elif symbol:
            self.feedback_label.setText(f"❌ Detected: {symbol}, expected: {target_letter}")
        else:
            self.feedback_label.setText("❓ No hand detected")

    def reset_flag(self):
        self.correct_detected = False

    def go_back(self):
        self.is_active = False
        self.timer.stop()
        self.on_back()

    def reset_lesson(self):
        self.is_active = True
        self.current_word_index = 0
        self.current_letter_index = 0
        self.correct_detected = False
        self.update_display()
        self.feedback_label.setText("🎉 Welcome to Lesson 2!")
        QTimer.singleShot(2000, lambda: self.is_active and self.feedback_label.setText("Sign the first letter"))
        self.timer.start(1000)
