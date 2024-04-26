import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

# Load the dataset
data = pd.read_csv("Test4_data.csv")

# Data preprocessing
# Drop rows with missing values
data.dropna(inplace=True)
data.drop_duplicates(inplace=True)

# Round the 'EDA' and 'TEMP' columns to the desired number of decimal places
data['EDA'] = data['EDA'].round(7)
data['TEMP'] = data['TEMP'].round(2)

# Find the minimum number of rows among the labels
min_rows = data['Label'].value_counts().min()

# Sample the same number of rows from each label
data = data.groupby('Label').apply(lambda x: x.sample(min_rows)).reset_index(drop=True)

# Save the preprocessed data to a new CSV file
data.to_csv("preprocessed_data2.csv", index=False)

# Shuffle the dataset
data_shuffled = data.sample(frac=1, random_state=42)  # Shuffle with a fixed random state for reproducibility

# Separate features (X) and target variable (label)
X = data_shuffled[['EDA', 'HR', 'TEMP']]
y = data_shuffled['Label']

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
optimizer = Adam(learning_rate=0.001)
model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Early stopping
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Train the model
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.1, callbacks=[early_stopping], verbose=1)

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy}")

# Save the trained model
model.save("Try_Me_Del_Me.h5")
# THe ONE

import matplotlib.pyplot as plt

# Plot training & validation accuracy values
plt.figure(figsize=(12, 6))
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()