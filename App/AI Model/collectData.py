print("Importing Libraries...")
import cv2
import mediapipe as mp
import numpy as np
from pickle import dump as pickleDump
print("Initalizing Mediapipe...")

# Initialize MediaPipe
mediapipeHands = mp.solutions.hands
mediapipeDrawing = mp.solutions.drawing_utils
hands = mediapipeHands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Labels for ASL gestures
labels = list("ABCDEFGHIKLMNOPQRSTUVQXY")
data = {label: [] for label in labels}
landmarks = None
currentLabel = 0

camara = cv2.VideoCapture(0) # Start the camara
print("Press space to switch to the next label. Press [q] to quit.")

while camara.isOpened():
    ret, frame = camara.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgbFrame)

    if results.multi_hand_landmarks:
        for handLandmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            mediapipeDrawing.draw_landmarks(frame, handLandmarks, mediapipeHands.HAND_CONNECTIONS)

            # Convert landmarks to a NumPy array
            landmarks = np.array([[lm.x, lm.y, lm.z] for lm in handLandmarks.landmark])

            # Normalize: Translate so wrist (index 0) is at (0,0,0)
            landmarks -= landmarks[0]
            maxDistanceFromWrist = np.max(np.linalg.norm(landmarks, axis=1))  # Compute max distance from wrist (fixing the previous error)
            if maxDistanceFromWrist > 0:  # Avoid division by zero
                landmarks /= maxDistanceFromWrist  # Scale the landmarks
            
            if handedness.classification[0].label == "Left":
                landmarks[:, 0] *= -1  # Flip x-axis to make it represented as a right hand
                
            landmarks = landmarks.flatten() # Convert into a 1-D array
            important_indices = [4, 8, 12, 16, 20]  # Fingertip indices

            for idx in important_indices:
                landmarks[idx * 3 : idx * 3 + 3] *= 1.5  # Give 50% more weight to these coords

    cv2.putText(frame, f"Label: {labels[currentLabel]}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) # Show the label as text
    cv2.imshow("Data Collection", frame) # Show the video feed

    key = cv2.waitKey(1) # Get a pressed key
    if key == ord(' '): # If space pressed, add the data
        if len(landmarks) == 63:
                data[labels[currentLabel]].append(landmarks)
        currentLabel = (currentLabel + 1) % len(labels)
        print(f"Switched to {labels[currentLabel]}")
    elif key == ord('q'): # Quit on q
        break

camara.release()
cv2.destroyAllWindows()

# Save collected data
with open("./App/AI Model/asl_data.pkl", "wb") as f: # Put all data collected into file
    pickleDump(data, f)

print("Completed!")