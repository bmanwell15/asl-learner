"""
    This page holds all constants throughout the entire project. This is good organizational solution.
"""
import os

WINDOW_WIDTH: int = 360
WINDOW_HEIGHT: int = 640

AI_MODEL_LETTERS: str = "ABCDEFGHIKLMNOPQRS"
AI_MODEL_NUMBER_OF_LANDMARKS: int = 63

SYMBOL_DETECTION_INTERVAL_MS: int = 500
CAMERA_FPS = 30

BASE_DIRECTORY: str = os.path.dirname(os.path.abspath(__file__))
AI_MODEL_PATH: str = os.path.join(BASE_DIRECTORY, "AI Model", "asl_model.h5")
AI_MODEL_LABELS_PATH: str = os.path.join(BASE_DIRECTORY, "AI Model", "labels.pkl")
NAUTILUS_LOGO_PATH: str = os.path.join(os.path.dirname(__file__), "Assets", "nautilus_logo.png")