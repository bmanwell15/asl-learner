import cv2
import mediapipe as mp
import numpy as np
import pickle

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Labels for ASL gestures
labels = ["A", "B", "C", "-"]
data = {label: [] for label in labels}

cap = cv2.VideoCapture(0)

current_label = 0
print("Press space to switch to the next label. Press [q] to quit.")

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

            # Convert landmarks to a NumPy array
            landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])  # No flatten()

            # Normalize: Translate so wrist (index 0) is at (0,0,0)
            landmarks -= landmarks[0]

            # Compute max distance from wrist (fixing the previous error)
            max_dist = np.max(np.linalg.norm(landmarks, axis=1))  # axis=1 now works

            if max_dist > 0:  # Avoid division by zero
                landmarks /= max_dist  # Scale the landmarks

                
            landmarks = landmarks.flatten()
            if len(landmarks) == 63:
                data[labels[current_label]].append(landmarks)

    cv2.putText(frame, f"Label: {labels[current_label]}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Data Collection", frame)

    key = cv2.waitKey(1)
    if key == ord(' '):
        current_label = (current_label + 1) % len(labels)
        print(f"Switched to {labels[current_label]}")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Save collected data
with open("./App/AI Model/asl_data.pkl", "wb") as f:
    pickle.dump(data, f)
