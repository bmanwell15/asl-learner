from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont, QPixmap, QImage
import cv2
import os

class LetterPage(QWidget):
    def __init__(self, letter, recognizer, on_back, on_success):
        super().__init__()
        self.letter = letter
        self.recognizer = recognizer
        self.on_back = on_back
        self.on_success = on_success

        self.init_ui()
        self.start_camera()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        top_bar = QHBoxLayout()
        back_btn = QPushButton("←")
        back_btn.setFont(QFont("Arial", 18))
        back_btn.setFixedSize(40, 40)
        back_btn.setStyleSheet("background: transparent; border: none;")
        back_btn.clicked.connect(self.on_back)

        self.streak_label = QLabel("5 🔥")
        self.streak_label.setFont(QFont("Arial", 16))
        self.streak_label.setStyleSheet("color: #a139e8;")
        top_bar.addWidget(back_btn)
        top_bar.addStretch()
        top_bar.addWidget(self.streak_label)
        layout.addLayout(top_bar)

        self.prompt = QLabel(f"Sign: {self.letter}")
        self.prompt.setAlignment(Qt.AlignCenter)
        self.prompt.setFont(QFont("Arial", 26, QFont.Bold))
        layout.addWidget(self.prompt)

        self.sign_image = QLabel()
        self.sign_image.setAlignment(Qt.AlignCenter)
        img_path = os.path.join("assets", "images", f"{self.letter}.png")
        self.sign_image.setPixmap(QPixmap(img_path).scaled(200, 200, Qt.KeepAspectRatio))
        layout.addWidget(self.sign_image)

        self.video_feed = QLabel()
        self.video_feed.setFixedSize(300, 300)
        self.video_feed.setAlignment(Qt.AlignCenter)
        self.video_feed.setStyleSheet("border-radius: 20px; border: 2px solid #ccc;")
        layout.addWidget(self.video_feed)

        self.feedback = QLabel("Try to form the sign")
        self.feedback.setAlignment(Qt.AlignCenter)
        self.feedback.setFont(QFont("Arial", 16))
        layout.addWidget(self.feedback)
        self.setLayout(layout)

    def start_camera(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_view)
        self.timer.start(100)

    def update_view(self):
        frame, symbol = self.recognizer.get_frame_and_symbol()
        if frame is not None:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
            self.video_feed.setPixmap(QPixmap.fromImage(img))

        if symbol == self.letter:
            self.feedback.setText("✅ Correct!")
            self.timer.stop()
            QTimer.singleShot(1500, self.on_success)
        elif symbol:
            self.feedback.setText(f"❌ Detected: {symbol}")
        else:
            self.feedback.setText("❓ No hand detected")