from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class HomePage(QWidget):
    def __init__(self, switch_to_lesson):
        super().__init__() #used to call the constructor of the QMainWindow class - the parent class
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("ASL Learner")
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        btn = QPushButton("Start Lesson 1")
        btn.setFont(QFont("Arial", 18))
        btn.setFixedSize(250, 60)
        btn.clicked.connect(switch_to_lesson)

        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(btn)
        self.setLayout(layout)
