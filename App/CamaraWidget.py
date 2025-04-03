from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, QTimer

class CameraWidget(QWidget):
    _FPS = 30
    def __init__(self, parent: QWidget, handRecognizer):
        super().__init__(parent)

        # Initialize the layout and QLabel for displaying the camera feed
        self.layout = QVBoxLayout()
        self.image_label = QLabel("Loading camera...")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)
        self.setLayout(self.layout)

        # Assign the passed handRecognizer object to an instance variable
        self.handRecognizer = handRecognizer

        # Timer to update frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(1000 / CameraWidget._FPS)  # Convert FPS to milliseconds

    def updateFrame(self):
        rgbFrame = self.handRecognizer.getFrame()  # Call getFrame method from the passed handRecognizer
        
        # Convert the frame to QImage
        height, width, channel = rgbFrame.shape
        bytesPerLine = channel * width
        qImg = QImage(rgbFrame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        
        # Display the frame in the QLabel
        self.image_label.setPixmap(QPixmap.fromImage(qImg))