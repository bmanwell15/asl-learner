import sys
import os
from datetime import datetime, timedelta
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QSizePolicy, QSpacerItem
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
import Constants

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
        

        flame = QLabel(str(NautilusUI.getStreak()) + " 🔥")
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

        pixmap = QPixmap(Constants.NAUTILUS_LOGO_PATH)
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

        self.lessonButtons = []

        self.lessonButtons.append(self.make_lesson_button("lesson 1", lesson_id=1, enabled=True))
        self.lessonButtons.append(self.make_lesson_button("lesson 2", lesson_id=2, enabled=False))

        for i in range(3, 6):
            self.lessonButtons.append(self.make_lesson_button(f"lesson {i}", lesson_id=i, enabled=False))
        
        for button in self.lessonButtons:
            layout.addWidget(button.itemAt(0).widget())

    def make_lesson_button(self, label, lesson_id, enabled=False):
        btn_layout = QHBoxLayout()
        btn = QPushButton(f"  🔒  {label}" if not enabled else label)
        btn.setFixedHeight(50)
        btn.setFont(QFont("Arial", 14))
        btn.setCursor(Qt.PointingHandCursor)

        if lesson_id == 1:
            btn.clicked.connect(lambda: self.launch_lesson(1))
        elif lesson_id == 2:
            self.lesson2_button = btn 
            btn.clicked.connect(lambda: self.launch_lesson(2))

        btn.setEnabled(enabled)

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

        btn_layout.addWidget(btn)
        return btn_layout

   
    
    def launch_lesson(self, lesson_id=1):
        self.lessonButtons[lesson_id - 1].setEnabled(False)
        self.updateButton(lesson_id, "loading lesson...")
        from MainWindow import ASLLearner
        self.updateButton(lesson_id, "loading lesson.....")
        if hasattr(self, 'learner_window') and self.learner_window:
            self.learner_window.deleteLater()
        self.updateButton(lesson_id, "loading lesson......")
        self.learner_window = ASLLearner(main_window=self, start_lesson=lesson_id)
        self.updateButton(lesson_id, "loading lesson.......")
        self.hide()
        self.learner_window.show()
        self.lessonButtons[lesson_id - 1].setEnabled(True)
        self.updateButton(lesson_id, f"lesson {lesson_id}")


    def unlock_lesson_2(self):
        self.lesson2_button.setEnabled(True)
        self.lesson2_button.setText("lesson 2")
        self.lesson2_button.clicked.connect(lambda: self.launch_lesson(2))
        self.lesson2_button.setStyleSheet("""
            QPushButton {
            background-color: #2d36f4;
            color: white;
            border-radius: 25px;
            text-align: left;
            padding-left: 20px;
            }
        """)
    

    def updateButton(self, lesson_id, text): # Updates the button
        self.lessonButtons[lesson_id - 1].itemAt(0).widget().setText(text)
        QApplication.processEvents() # Update the GUI
    
    def getStreak():
        today = datetime.today().date()
        if os.path.exists(Constants.SAVE_FILE_PATH):
            with open(Constants.SAVE_FILE_PATH, "r") as saveFile:
                saveData = saveFile.readlines()
            for line in saveData:
                lineValue = line[line.find("=") + 1:] # Each line in file is formatted as key=value
                if line.startswith("lastSeen"):
                    lastSeen = datetime.strptime(lineValue, "%Y-%m-%d\n").date()
                elif line.startswith("currentStreak"):
                    currentStreak = int(lineValue)
        
            dayDifference = (today - lastSeen).days
            if dayDifference == 1:
                currentStreak += 1
            elif dayDifference != 0: # Account for loggin on multiple times in a day
                currentStreak = 1 # Equals 1 if counting today, 0 otherwise
        else: 
            currentStreak = 1
            
        with open(Constants.SAVE_FILE_PATH, "w") as saveFile:
            saveFile.write("lastSeen=" + today.strftime("%Y-%m-%d") + "\n")
            saveFile.write(f"currentStreak={currentStreak}\n")
        
        return currentStreak



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NautilusUI()
    window.show()
    sys.exit(app.exec())
