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
model = None

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

def preprocess_data(eda, hr, temp):
    if eda is None or hr is None or temp is None:
        raise ValueError('eda, hr, and temp must be a number, not None')
    
def osc_handler(address, *args):
    global eda_data, hr_data, temp_data

    print(f"Received data from {address}: {args}")
    
    # Check the address and update corresponding data
    if address == "/EmotiBit/0/EDA":
        eda_data = args[0] if len(args) > 0 else None
    elif address == "/EmotiBit/0/HR":
        hr_data = args[0] if len(args) > 0 else None
    elif address == "/EmotiBit/0/TEMP":
        temp_data = args[0] if len(args) > 0 else None

    # If all data is available, preprocess and predict
    if eda_data is not None and hr_data is not None and temp_data is not None:
        preprocessed_data = preprocess_data(eda_data, hr_data, temp_data)
        prediction = predict_stress_level(preprocessed_data)
        # Print the prediction in standard notation
        print("Predicted stress level:", prediction)

    eda_scaled = eda / 100.0  # Example scaling
    hr_scaled = hr / 100.0  # Example scaling
    temp_scaled = temp / 100.0  # Example scaling
    return [eda_scaled, hr_scaled, temp_scaled]

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

@app.route('/predict', methods=['POST'])
def predict():
    global hr, eda, temp, User, model

    # Check if all necessary data is available
    if hr is None or eda is None or temp is None:
        return jsonify({'error': 'Data not available'}), 400

    # Load the trained model if it's not already loaded
    if model is None:
        model = tf.keras.models.load_model(f'stress_prediction_model_multiclass.h5')

    # Preprocess the data
    preprocessed_data = preprocess_data(eda, hr, temp)

    # Predict the stress level
    prediction = model.predict(np.array([preprocessed_data]))
    # Return the prediction
    return jsonify({'prediction': prediction.tolist()})

if __name__ == "__main__":
    dispatcher = Dispatcher()
    dispatcher.map("/EmotiBit/0/HR", osc_handler)
    dispatcher.map("/EmotiBit/0/EDA", osc_handler)
    dispatcher.map("/EmotiBit/0/TEMP", osc_handler)

    server = osc_server.ThreadingOSCUDPServer(("localhost", 5005), dispatcher)
    print("Serving on {}".format(server.server_address))
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    socketio.run(app, port=8080)

# import argparse
# import csv
# import numpy as np
# from pythonosc.dispatcher import Dispatcher
# from pythonosc import osc_server
# import tensorflow as tf

# # Load the trained model
# model = tf.keras.models.load_model('stress_prediction_model_multiclass.h5')

# # Initialize variables to store received data
# eda_data = None
# hr_data = None
# temp_data = None

# def preprocess_data(eda, hr, temp):
#     # Preprocess the data if needed
#     # Here, we are just scaling the data
#     eda_scaled = eda / 100.0  # Example scaling
#     hr_scaled = hr / 100.0  # Example scaling
#     temp_scaled = temp / 100.0  # Example scaling
#     return [eda_scaled, hr_scaled, temp_scaled]

# def predict_stress_level(data):
#     # Convert the list to numpy array
#     data_array = np.array([data])
#     print ('Test')
#     print (data_array)
#     prediction = model.predict(data_array)
#     # Format the prediction as a string in standard notation
#     prediction_str = np.array2string(prediction, formatter={'float_kind': lambda x: "%.6f" % x})
#     return prediction_str

# def osc_handler(address, *args):
#     global eda_data, hr_data, temp_data

#     print(f"Received data from {address}: {args}")
    
#     # Check the address and update corresponding data
#     if address == "/EmotiBit/0/EDA":
#         eda_data = args[0] if len(args) > 0 else None
#     elif address == "/EmotiBit/0/HR":
#         hr_data = args[0] if len(args) > 0 else None
#     elif address == "/EmotiBit/0/TEMP":
#         temp_data = args[0] if len(args) > 0 else None

#     # If all data is available, preprocess and predict
#     if eda_data is not None and hr_data is not None and temp_data is not None:
#         preprocessed_data = preprocess_data(eda_data, hr_data, temp_data)
#         prediction = predict_stress_level(preprocessed_data)
#         # Print the prediction in standard notation
#         print("Predicted stress level:", prediction)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--ip", default="172.20.10.10", help="The ip to listen on")
#     parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
#     args = parser.parse_args()

#     dispatcher = Dispatcher()
#     dispatcher.map("/EmotiBit/0/HR", osc_handler)
#     dispatcher.map("/EmotiBit/0/EDA", osc_handler)
#     dispatcher.map("/EmotiBit/0/TEMP", osc_handler)

#     server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
#     print("Serving on {}".format(server.server_address))
#     server.serve_forever()
