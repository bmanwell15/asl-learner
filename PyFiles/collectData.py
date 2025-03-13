import cv2
import mediapipe as mp
import numpy as np
import pickle

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Labels for ASL gestures
labels = ["A", "B", "C", "D", "E", "-"]
data = {label: [] for label in labels}

cap = cv2.VideoCapture(0)

current_label = 0
print("Press [n] to switch to the next label. Press [q] to quit.")

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
                data[labels[current_label]].append(landmarks)

    cv2.putText(frame, f"Label: {labels[current_label]}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Data Collection", frame)

    key = cv2.waitKey(1)
    if key == ord('n'):
        current_label = (current_label + 1) % len(labels)
        print(f"Switched to {labels[current_label]}")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Save collected data
with open("./AI Model/asl_data.pkl", "wb") as f:
    pickle.dump(data, f)
