import sys
import os
import random
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QSizePolicy, QSpacerItem
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
from lesson_page import LessonPage

class NautilusUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nautilus")
        self.setFixedSize(360, 640)
        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 #d3ecf6, stop:1 #a8d8f8
                );
                font-family: Arial;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Top bar
        top_layout = QHBoxLayout()
        profile_pic = QLabel()
        profile_pic.setFixedSize(40, 40)
        profile_pic.setStyleSheet("background-color: #ccc; border-radius: 20px;")

        name = QLabel("profile_name")
        name.setFont(QFont("Arial", 12))
        name.setStyleSheet("background: transparent;")
        

        flame = QLabel("5 🔥")
        flame.setStyleSheet("color: #a139e8;")
        flame.setFont(QFont("Arial", 12))
        flame.setStyleSheet("background: transparent;")

        top_layout.addWidget(profile_pic)
        top_layout.addWidget(name)
        top_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        top_layout.addWidget(flame)

        layout.addLayout(top_layout)

        # Logo image
        logo = QLabel()
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("background: transparent;")

        logo_path = os.path.join(os.path.dirname(__file__), "nautilus_logo.png")
        pixmap = QPixmap(logo_path)
        if pixmap.isNull():
            logo.setText("🌀")
            logo.setFont(QFont("Arial", 64))
        else:
            logo.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        layout.addWidget(logo)

        # Title
        title = QLabel("nautilus")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 26))
        title.setStyleSheet("""
            QLabel {
                background: transparent;
                color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6157f6, stop:1 #a139e8
                );
            }
        """)
        layout.addWidget(title)

        
        # Lesson buttons
        lesson1_layout, lesson1_btn = self.make_lesson_button("lesson 1", enabled=True)
        layout.addLayout(lesson1_layout)

        if lesson1_btn:
            lesson1_btn.clicked.connect(self.open_lesson1)  #  Link to the lesson window

        for i in range(2, 6):
            locked_layout, _ = self.make_lesson_button(f"lesson {i}", enabled=False)
            layout.addLayout(locked_layout)
    def make_lesson_button(self, label, enabled=False):
        btn_layout = QHBoxLayout()
        btn = QPushButton(f"  🔒  {label}")
        btn.setFixedHeight(50)
        btn.setFont(QFont("Arial", 14))
        btn.setCursor(Qt.PointingHandCursor)

        if enabled:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2d36f4;
                    color: white;
                    border-radius: 25px;
                    text-align: left;
                    padding-left: 20px;
                }
            """)
        else:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #b0bcc1;
                    color: #333;
                    border-radius: 25px;
                    text-align: left;
                    padding-left: 20px;
                }
            """)
            btn.setEnabled(False)

        btn_layout.addWidget(btn)
        return btn_layout, btn
    def open_lesson1(self):
        letters = ["A", "B", "C"]
        #letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        #random.shuffle(letters)
        self.lesson_window = LessonPage(lesson_letters=letters, index=0, parent=self)
        self.lesson_window.show()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NautilusUI()
    window.show()
    sys.exit(app.exec())

