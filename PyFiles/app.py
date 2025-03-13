import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import pickle

# Load trained model
MODEL_PATH = "./AI Model/asl_model.h5"
LABELS_PATH = "./AI Model/labels.pkl"
model = tf.keras.models.load_model(MODEL_PATH)
with open(LABELS_PATH, "rb") as f:
    labels = pickle.load(f)


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]).flatten()
            
            if len(landmarks) == 63:
                landmarks = np.expand_dims(landmarks, axis=0)
                prediction = model.predict(landmarks)
                predicted_label = labels[np.argmax(prediction)]

                prediction = model.predict(landmarks)
                print("Prediction Probabilities:", prediction)  # Debugging output
                # predicted_label = labels[np.argmax(prediction)]
                # print("Detected Sign:", predicted_label)
                
                cv2.putText(frame, predicted_label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                            1, (0, 255, 0), 2, cv2.LINE_AA)
    
    cv2.imshow("ASL Recognition", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
