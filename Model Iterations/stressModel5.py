import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

# Load the dataset
df = pd.read_csv('Test4_data.csv')  # Replace 'your_dataset.csv' with the path to your dataset

# Data preprocessing
# Handling missing values (if any)
# For simplicity, let's assume there are no missing values in this example

# Handling outliers (if any)
# For simplicity, let's skip outlier detection and treatment in this example

# Normalization
scaler = StandardScaler()
df[['HR', 'EDA', 'TEMP']] = scaler.fit_transform(df[['HR', 'EDA', 'TEMP']])

# Splitting the dataset into features and target variable
X = df[['HR', 'EDA', 'TEMP']]
y = df['Label']

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Reshape the data to add a time step dimension
X_train = np.reshape(X_train.values, (X_train.shape[0], 1, X_train.shape[1]))
X_test = np.reshape(X_test.values, (X_test.shape[0], 1, X_test.shape[1]))

# Define the neural network model
model = keras.Sequential([
    layers.LSTM(64, return_sequences=True, input_shape=(None, 3)),  # 3 input features
    layers.LSTM(64),
    layers.Dense(3, activation='softmax')  # 3 output classes
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Evaluate the model on the test set
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f'Test accuracy: {test_accuracy}')

# Save the trained model
model.save('stressLSTM.h5')  # Save the model to a file named 'stressLSTM.h5'