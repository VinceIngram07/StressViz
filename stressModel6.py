import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Step 1: Data Collection
# Assuming you have collected your data and stored it in a CSV file
# You need to replace "physiological_data.csv" with your actual data file
data = pd.read_csv("Test4_data.csv")

# Step 2: Data Preprocessing
# Drop any unnecessary columns
# data.drop(columns=["unnecessary_column"], inplace=True)

# Handle missing values
data.dropna(inplace=True)
data.drop_duplicates(inplace=True)

# Normalize/Standardize features
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Split the dataset into features (X) and target (y)
X = data_scaled[:, :-1]  # Features (EDA, Temperature, HR)
y = data_scaled[:, -1]   # Target (stress levels)

# Find the minimum number of rows among the labels
min_rows = data['Label'].value_counts().min()

# Sample the same number of rows from each label
data = data.groupby('Label').apply(lambda x: x.sample(min_rows)).reset_index(drop=True)

# Save the preprocessed data to a new CSV file
data.to_csv("preprocessed_data6.csv", index=False)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Model Architecture
model = Sequential()
model.add(LSTM(units=50, input_shape=(X_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(Dense(1))

# Step 4: Model Training
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, epochs=100, batch_size=32)

# Step 5: Model Evaluation
y_pred = model.predict(X_test)

# Evaluate the model using appropriate metrics
# For simplicity, let's assume we're using mean squared error
mse = np.mean((y_pred - y_test)**2)
print("Mean Squared Error:", mse)

# Other metrics
y_pred_binary = np.where(y_pred > 0.5, 1, 0)  # Convert to binary predictions
y_test_binary = np.where(y_test > 0.5, 1, 0)
accuracy = accuracy_score(y_test_binary, y_pred_binary)
precision = precision_score(y_test_binary, y_pred_binary)
recall = recall_score(y_test_binary, y_pred_binary)
f1 = f1_score(y_test_binary, y_pred_binary)
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

model.save("CheggModel.h5")
# Step 6: Real-Time Prediction Script
# Implement the script to capture live physiological data streams, preprocess the data,
# and feed it into the trained LSTM model for prediction. This would involve setting up
# data acquisition hardware and real-time data processing capabilities.