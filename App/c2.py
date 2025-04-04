import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtMultimedia import QCamera, QMediaCaptureSession, QMediaDevices, QImageCapture
from PySide6.QtMultimediaWidgets import QVideoWidget

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()

        self.camera = None
        self.capture_session = QMediaCaptureSession()
        self.image_capture = QImageCapture()

        available_cameras = QMediaDevices().videoInputs()
        if not available_cameras:
            print("No camera found")
            sys.exit()

        self.camera = QCamera(available_cameras[0])
        self.capture_session.setCamera(self.camera)
        self.capture_session.setImageCapture(self.image_capture)

        self.video_widget = QVideoWidget()
        self.capture_session.setVideoOutput(self.video_widget)

        self.capture_button = QPushButton("Capture Image")
        self.capture_button.clicked.connect(self.capture_image)

        hbox = QHBoxLayout()
        hbox.addWidget(self.capture_button)

        vbox = QVBoxLayout()
        vbox.addWidget(self.video_widget)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.camera.start()

    def capture_image(self):
        self.image_capture.captureToFile()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec())