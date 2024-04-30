import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.regularizers import l2

# Step 1: Data Collection
data = pd.read_csv("TheOne_data.csv")

# Step 2: Data Preprocessing
data.dropna(inplace=True)
data.drop_duplicates(inplace=True)

scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

X = data_scaled[:, :-1]  # Features (EDA, Temperature, HR)
y = data_scaled[:, -1]   # Target (stress levels)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Model Architecture
model = Sequential()
model.add(LSTM(units=30, input_shape=(X_train.shape[1], 1), kernel_regularizer=l2(0.01), recurrent_regularizer=l2(0.01), bias_regularizer=l2(0.01)))
model.add(Dropout(0.5))  # Increase dropout rate
model.add(Dense(1, kernel_regularizer=l2(0.01)))

# Step 4: Model Training
model.compile(optimizer='adam', loss='mean_squared_error')

early_stopping = EarlyStopping(monitor='val_loss', patience=20)  # Increase patience

model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2, callbacks=[early_stopping])

# Step 5: Model Evaluation
y_pred = model.predict(X_test)

mse = np.mean((y_pred - y_test)**2)
print("Mean Squared Error:", mse)

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

model.save("Model2.h5")