import sys
import cv2
from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QSizePolicy, QSpacerItem
)
class CameraFeed(QWidget):
    def __init__(self, parent=None):
        super(CameraFeed, self).__init__(parent)
        self.camera = cv2.VideoCapture(0)
        self.image_label = QLabel(self)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30) # 30 ms refresh rate

        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)
        self.setLayout(layout)

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(image)
            self.image_label.setPixmap(pixmap)
    
    def closeEvent(self, event):
        self.camera.release()
        cv2.destroyAllWindows()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CameraFeed()
    window.show()
    sys.exit(app.exec_())