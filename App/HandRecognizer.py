import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import pickle



class HandRecognizer:
    _MODEL_PATH = "./App/AI Model/asl_model.h5"
    _LABELS_PATH = "./App/AI Model/labels.pkl"

    def __init__(self):
        # Load trained model
        self.model = tf.keras.models.load_model(HandRecognizer._MODEL_PATH)
        with open(HandRecognizer._LABELS_PATH, "rb") as f:
            self.labels = pickle.load(f)

        self.mpHands = mp.solutions.hands
        self.mpDrawing = mp.solutions.drawing_utils
        self.hands = self.mpHands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

        self.isCamaraOpen = False # Set to false so that way openCamara() can set it to true
        self.openCamara()
    
    def openCamara(self) -> None:
        if not self.isCamaraOpen:
            self.camaraCapture = cv2.VideoCapture(0)
            self.isCamaraOpen = True
    
    def closeCamara(self) -> None:
        if self.isCamaraOpen:
            self.camaraCapture.release()
            self.isCamaraOpen = False
    
    def getCurrentHandSymbol(self) -> str:
        if not self.isCamaraOpen:
            self.openCamara()

        ret, frame = self.camaraCapture.read()
        if not ret:
            raise RuntimeError("ret not defined!")
    
        frame = cv2.flip(frame, 1) # Frame of the camara
        rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Frame in RGB color format
        results = self.hands.process(rgbFrame)
        
        if results.multi_hand_landmarks:
            for handLandmarks in results.multi_hand_landmarks:
                self.mpDrawing.draw_landmarks(frame, handLandmarks, self.mpHands.HAND_CONNECTIONS)
                landmarks = np.array([[lm.x, lm.y, lm.z] for lm in handLandmarks.landmark]).flatten()

                for i in range(len(landmarks)):
                    landmarks[i] -= landmarks[4] # landmarks[4] being the left most point in a right hand (tip of thumb)
                    landmarks[i] = abs(landmarks[i])
                
                if len(landmarks) == 63: # If full hand is in the video frame
                    landmarks = np.expand_dims(landmarks, axis=0)
                    prediction = self.model.predict(landmarks, verbose=0) # verbose=0 makes it not print a progress bar when predicting
                    predictedLabel = self.labels[np.argmax(prediction)]
            
                    # print("Detected Sign:", predictedLabel) # Debug
                    # cv2.putText(frame, predictedLabel, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA) # Print the label on the video image
                    return predictedLabel
        return None
    
    def waitUntilHandSymbol(self, symbol: str) -> str:
        lastHandSignal = self.getCurrentHandSymbol()
        while lastHandSignal != symbol:
            lastHandSignal = self.getCurrentHandSymbol()
        return lastHandSignal
