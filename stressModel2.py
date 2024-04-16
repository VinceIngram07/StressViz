import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

# Load the dataset
data = pd.read_csv("merged_data.csv")

# Data preprocessing
# Drop rows with missing values
data.dropna(inplace=True)

# Convert mixed type column to numeric
data['id'] = pd.to_numeric(data['id'], errors='coerce')
data.dropna(inplace=True)

# Shuffle the dataset
data_shuffled = data.sample(frac=1, random_state=42)  # Shuffle with a fixed random state for reproducibility

# Separate features (X) and target variable (label)
X = data_shuffled[['EDA', 'HR', 'TEMP']]
y = data_shuffled['label']

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Define the neural network model
model = Sequential([
    Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.5),
    Dense(16, activation='relu'),
    Dropout(0.5),
    Dense(3, activation='softmax')  # 3 neurons for 3 classes, softmax activation for multi-class classification
])

# Compile the model
optimizer = Adam(learning_rate=0.001)  # Adjust learning rate if needed
model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Early stopping
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Train the model
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.1, callbacks=[early_stopping], verbose=1)

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy}")

# Save the trained model
model.save("stress_prediction_model_multiclass.h5")
# THe ONE