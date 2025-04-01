from PySide6.QtWidgets import QApplication
import sys 
from components.QMainWindow import ASLLearner

def main(): 
    app = QApplication(sys.argv)
    window = ASLLearner()
    window.show()
    sys.exit(app.exec())