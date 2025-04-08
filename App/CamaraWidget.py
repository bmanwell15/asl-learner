from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, QTimer
import Constants

class CameraWidget(QWidget):
    def __init__(self, parent: QWidget, handRecognizer):
        super().__init__(parent)

        # Assign the passed handRecognizer object to an instance variable
        self.handRecognizer = handRecognizer

        # Initialize the layout and QLabel for displaying the camera feed
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: black;")  # optional fallback

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        # Timer to update frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(int(1000 / Constants.CAMERA_FPS))  # Convert FPS to milliseconds

    def updateFrame(self):
        rgbFrame = self.handRecognizer.getFrame()
        height, width, channel = rgbFrame.shape
        bytesPerLine = channel * width
        qImg = QImage(rgbFrame.data, width, height, bytesPerLine, QImage.Format_RGB888)

        # Resize image to match widget size
        scaled = QPixmap.fromImage(qImg).scaled(
            self.image_label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )

        self.image_label.setPixmap(scaled)