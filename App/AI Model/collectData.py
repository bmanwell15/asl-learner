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
labels = list("ABCDEFGHIKLMNOPQRSTUVWXY-")
data = {label: [] for label in labels}
landmarks = None
currentLabel = 0
iteration = 0

camara = cv2.VideoCapture(0) # Start the camara
print("Press space to switch to the next label. Press [q] to quit.")

while camara.isOpened():
    iteration += 1
    print("Iteration", iteration)
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

            # Normalize landmarks (translate wrist to origin and scale)
            landmarks -= landmarks[0]
            maxDistance = np.max(np.linalg.norm(landmarks, axis=1))
            if maxDistance > 0:
                landmarks /= maxDistance

            if handedness.classification[0].label == "Left":
                landmarks[:, 0] *= -1  # Flip to normalize left/right hand

            # Flatten landmarks + add custom feature(s)
            landmarks = landmarks.flatten()

            # Optionally emphasize fingertips
            # important_indices = [4, 8, 12]
            # for idx in important_indices:
            #     landmarks[idx * 3 : idx * 3 + 3] *= 1.5
                
            landmarks = landmarks.flatten() # Convert into a 1-D array

    cv2.putText(frame, f"Training: {labels[currentLabel]}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) # Show the label as text
    cv2.imshow("Data Collection", frame) # Show the video feed

    key = cv2.waitKey(1) # Get a pressed key
    if key == ord(' '): # If space pressed, add the data
        if len(landmarks) == 63:
                data[labels[currentLabel]].append(landmarks)
        currentLabel = (currentLabel + 1) % len(labels)
    elif key == ord('q'): # Quit on q
        break

camara.release()
cv2.destroyAllWindows()

# Save collected data
with open("./App/AI Model/asl_data.pkl", "wb") as f: # Put all data collected into file
    pickleDump(data, f)

print("Completed!")