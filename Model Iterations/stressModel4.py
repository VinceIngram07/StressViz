import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from tensorflow import keras
from tensorflow.keras import layers

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

# Define the neural network model
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=[3]),  # 3 input features
    layers.Dense(64, activation='relu'),
    layers.Dense(3, activation='softmax')  # 3 output classes (0 - relaxed, 1 - moderate stress, 2 - high stress)
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Evaluate the model on the test set
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f'Test accuracy: {test_accuracy}')

# Save the trained model
model.save('stress.h5')  # Save the model to a file named 'stress_prediction_model.h5'
