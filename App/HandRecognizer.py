from tensorflow.keras.models import load_model
from pickle import load as pickleLoad
import cv2
import mediapipe as mp
import numpy as np
import os
import Constants


class HandRecognizer:
    VERSION = "1.1.0" # Use this to keep track of the AI model version throughout different branches

    def __init__(self):
        self._LABELS_PATH = os.path.join(Constants.BASE_DIRECTORY, "AI Model", "labels.pkl")
        # Load trained model
        self.model = load_model(Constants.AI_MODEL_PATH, compile=False)
        with open(Constants.AI_MODEL_LABELS_PATH, "rb") as f:
            self.labels = pickleLoad(f)

        # Initilaze Mediapipe hand tracking
        self.mpHands = mp.solutions.hands
        self.mpDrawing = mp.solutions.drawing_utils
        self.hands = self.mpHands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

        self.isCamaraOpen = False # Set to false that way openCamara() can set it to true
        self.openCamara()
    
    def openCamara(self) -> None:
        """ Opens the camara for the AI Model to view. """
        if not self.isCamaraOpen:
            self.camaraCapture = cv2.VideoCapture(0)
            self.camaraCapture.set(cv2.CAP_PROP_FRAME_WIDTH, Constants.WINDOW_WIDTH)
            self.camaraCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, Constants.WINDOW_HEIGHT)
            self.isCamaraOpen = True
    
    def closeCamara(self) -> None:
        """ Closes the camara for the AI Model to view. """
        if self.isCamaraOpen:
            self.camaraCapture.release()
            self.isCamaraOpen = False
    
    def getFrame(self):
        """Returns the frame of the camara in RGB format"""
        if not self.isCamaraOpen:
            return None  # Gracefully skip if camera isn't ready

        ret, frame = self.camaraCapture.read()
        if not ret or frame is None:
            return None

        frame = cv2.flip(frame, 1)
        rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return rgbFrame
    
    def getCurrentHandSymbol(self) -> str:
        """ Returns a string containing the label for the hand symbol that is currently being displayed. If no hand is found on screen `None` is returned. """
        if not self.isCamaraOpen:
            self.openCamara()

        rgbFrame = self.getFrame()
        results = self.hands.process(rgbFrame)
        
        if results.multi_hand_landmarks:
            for handLandmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                #self.mpDrawing.draw_landmarks(frame, handLandmarks, self.mpHands.HAND_CONNECTIONS)
                landmarks = np.array([[lm.x, lm.y, lm.z] for lm in handLandmarks.landmark])

                # Normalize landmarks (translate wrist to origin and scale)
                landmarks -= landmarks[0]
                maxDistance = np.max(np.linalg.norm(landmarks, axis=1))
                if maxDistance > 0:
                    landmarks /= maxDistance

                if handedness.classification[0].label == "Left":
                    landmarks[:, 0] *= -1  # Flip to normalize left/right hand

                # Flatten landmarks + add custom feature(s)
                landmarks = landmarks.flatten()

                if len(landmarks) == 63: # If full hand is in the video frame
                    landmarks = np.expand_dims(landmarks, axis=0)
                    prediction = self.model.predict(landmarks, verbose=0) # verbose=0 makes it not print a progress bar when predicting
                    predictedLabel = self.labels[np.argmax(prediction)]
            
                    # print("Detected Sign:", predictedLabel) # Debug
                    # cv2.putText(frame, predictedLabel, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA) # Print the label on the video image
                    return predictedLabel
        return None
    
    def waitUntilHandSymbol(self, symbol: str) -> str:
        """ Blocks the script until the specified symbol is found. WARNING: As of now, there is not a timeout, so be very careful with the symbol that is imputted. If the symbol doesn't exist in the model, the script is blocked forever. """
        lastHandSignal = self.getCurrentHandSymbol()
        while lastHandSignal != symbol:
            lastHandSignal = self.getCurrentHandSymbol()
        return lastHandSignal
