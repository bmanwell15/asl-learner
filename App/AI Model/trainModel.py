print("Importing libraries...")
from pickle import load as pickleLoad, dump as pickleDump
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.losses import CategoricalCrossentropy
from sklearn.utils.class_weight import compute_class_weight
from numpy import array, unique, argmax
from os.path import exists

print("Preparing data...")
# Load data
with open("./App/AI Model/asl_data.pkl", "rb") as f:
    data = pickleLoad(f)

# Prepare dataset
x = []
y = []
labels = list(data.keys())

for label, samples in data.items():
    x.extend(samples)
    y.extend([labels.index(label)] * len(samples))

x = array(x)
y = array(y)

# One-hot encode labels
y = to_categorical(y, num_classes=len(labels))

class_weights = compute_class_weight(
    class_weight='balanced',
    classes=unique(argmax(y, axis=1)),
    y=argmax(y, axis=1)
)
class_weight_dict = dict(enumerate(class_weights))

# Define the model
if exists("./App/AI Model/asl_model.h5"):
    model = load_model('./App/AI Model/asl_model.h5')
    print("MODEL LOADED...")
else:
    model = Sequential([
        Dense(128, activation='tanh', input_shape=(63,)),  # 63 input features (flattened landmarks)
        BatchNormalization(),
        Dropout(0.4),
        Dense(64, activation='tanh'),
        BatchNormalization(),
        Dropout(0.3),
        Dense(32, activation='tanh'),
        BatchNormalization(),
        Dense(len(labels), activation='softmax')
    ])

model.compile(optimizer="adam", loss=CategoricalCrossentropy(label_smoothing=0.1), metrics=["accuracy"])

# Train the model
model.fit(x, y, epochs=80, batch_size=16, validation_split=0.3, class_weight=class_weight_dict)

# Save the model and labels
model.save("./App/AI Model/asl_model.h5")
with open("./App/AI Model/labels.pkl", "wb") as f:
    pickleDump(labels, f)

print("\n\n\n\n")
model.summary()