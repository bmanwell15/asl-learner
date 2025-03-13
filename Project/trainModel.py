#from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import pickle
import os

# Load data
with open("./Project/asl_data.pkl", "rb") as f:
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
if os.path.exists("./Project/asl_model.h5"):
    model = tf.keras.models.load_model('./Project/asl_model.h5')
    print("MODEL LOADED...")
else:
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(len(labels), activation='softmax')
    ])

# datagen = ImageDataGenerator(
#     rotation_range=20,  # Randomly rotate images
#     width_shift_range=0.2,  # Randomly shift images horizontally
#     height_shift_range=0.2,  # Randomly shift images vertically
#     shear_range=0.2,  # Apply random shear transformations
#     zoom_range=0.2,  # Randomly zoom in/out of images
#     horizontal_flip=True,  # Randomly flip images horizontally
#     fill_mode='nearest'  # Fill in missing pixels after transformations
# )

# datagen.fit()

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Train the model
model.fit(x, y, epochs=50, batch_size=16, validation_split=0.3)

# Save the model and labels
model.save("./Project/asl_model.h5")
with open("./Project/labels.pkl", "wb") as f:
    pickle.dump(labels, f)
