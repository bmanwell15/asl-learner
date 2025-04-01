#from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import pickle
import os

# Load data
with open("./App/AI Model/asl_data.pkl", "rb") as f:
    data = pickle.load(f)

# Prepare dataset
x = []
y = []
labels = list(data.keys())

for label, samples in data.items():
    x.extend(samples)
    y.extend([labels.index(label)] * len(samples))

x = np.array(x)
y = np.array(y)

# One-hot encode labels
y = tf.keras.utils.to_categorical(y, num_classes=len(labels))

# Define the model
if os.path.exists("./App/AI Model/asl_model.h5"):
    model = tf.keras.models.load_model('./App/AI Model/asl_model.h5')
    print("MODEL LOADED...")
else:
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(63,)),  # 63 input features (flattened landmarks)
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(len(labels), activation='softmax')
    ])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Train the model
model.fit(x, y, epochs=50, batch_size=16, validation_split=0.3)

# Save the model and labels
model.save("./App/AI Model/asl_model.h5")
with open("./App/AI Model/labels.pkl", "wb") as f:
    pickle.dump(labels, f)

model.summary()