from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import threading
import argparse
import csv
import os
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from flask_cors import CORS
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)
server = None
server_thread = None

hr = None
eda = None
temp = None
label = None
User = 'Test'

def write_to_csv(filename):
    global hr, eda, temp, label, User
    if User is not None:  # Only write to the file if User is not None
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            if os.stat(filename).st_size == 0:
                writer.writerow(['HR', 'EDA', 'TEMP', 'Label'])  # Include the label in the header
            writer.writerow([hr, eda, temp, label])  # Include the label in the data

def print_handler(address, *args):
    global hr, eda, temp, User
    print(f"Received data from {address}: {args}")
    if address == "/EmotiBit/0/HR":
        hr = args[0]
    elif address == "/EmotiBit/0/EDA":
        eda = args[0]
    elif address == "/EmotiBit/0/TEMP":
        temp = args[0]
    write_to_csv(f'{User}_data.csv')
    socketio.emit('data', {'hr': hr, 'eda': eda, 'temp': temp})

@app.route('/start', methods=['POST'])
def start():
    global server, server_thread, label, User
    User = request.json.get('username', 'User1')
    label = request.json.get('label', 0)  # Get the label from the request data
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="172.20.10.10", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = Dispatcher()
    dispatcher.map("/EmotiBit/0/HR", print_handler)
    dispatcher.map("/EmotiBit/0/EDA", print_handler)
    dispatcher.map("/EmotiBit/0/TEMP", print_handler)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    return 'Started'

@app.route('/stop', methods=['POST'])
def stop():
    global server, server_thread
    if server:
        server.shutdown()
        server_thread.join()
        server = server_thread = None

    return 'Stopped'
@app.route('/train', methods=['POST'])
def train():
    # global User
    # User = request.json.get('username', 'User1')  # Get the username from the request data

    # Load the dataset
    data = pd.read_csv(f"{User}_data.csv")

    # Data preprocessing
    # Drop rows with missing values
    data.dropna(inplace=True)
    data.drop_duplicates(inplace=True)

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
    model.save(f"stress_prediction_model_{User}.h5")

    return 'Model trained and saved'

if __name__ == "__main__":
    socketio.run(app, port=8080)