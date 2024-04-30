from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import threading
import argparse
import csv
import os
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
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

latest_hr = None
latest_eda = None
latest_temp = None

# Load the trained model
model = tf.keras.models.load_model('BestModel.h5')

hr = None
eda = None
temp = None
label = None
# thread = None
server = None
User = 'Test'

# Function to update latest values and write to CSV
def update_latest_values_print_handler(address, *args):
    global latest_hr, latest_eda, latest_temp
    if address == "/EmotiBit/0/HR":
        latest_hr = args[0]
    elif address == "/EmotiBit/0/EDA":
        latest_eda = args[0]
    elif address == "/EmotiBit/0/TEMP":
        latest_temp = args[0]

    # Write the latest data to CSV
    write_to_csv(f'{User}_data.csv')

    # Emit data to socketio
    socketio.emit('data', {'hr': latest_hr, 'eda': latest_eda, 'temp': latest_temp})

# Function to update values for predict function
def predict_print_handler(address, *args):
    global hr, eda, temp
    if address == "/EmotiBit/0/HR":
        hr = args[0]
    elif address == "/EmotiBit/0/EDA":
        eda = args[0]
    elif address == "/EmotiBit/0/TEMP":
        temp = args[0]

# Map print handlers to OSC addresses
dispatcher = Dispatcher()
dispatcher.map("/EmotiBit/0/HR", update_latest_values_print_handler)
dispatcher.map("/EmotiBit/0/EDA", update_latest_values_print_handler)
dispatcher.map("/EmotiBit/0/TEMP", update_latest_values_print_handler)
dispatcher.map("/EmotiBit/0/HR", predict_print_handler)
dispatcher.map("/EmotiBit/0/EDA", predict_print_handler)
dispatcher.map("/EmotiBit/0/TEMP", predict_print_handler)

# Start the OSC server
def start_osc_server():
    global server
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="172.20.10.10", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    server.serve_forever()

# Start the OSC server in a separate thread
thread = threading.Thread(target=start_osc_server)
thread.daemon = True
thread.start()

# Function to write data to CSV
def write_to_csv(filename):
    global hr, eda, temp, label, User
    if User is not None:
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            if os.stat(filename).st_size == 0:
                writer.writerow(['HR', 'EDA', 'TEMP', 'Label'])
            writer.writerow([hr, eda, temp, label])

@app.route('/start', methods=['POST'])
def start():
    global User, label, thread, server
    User = request.json.get('username', 'User1')
    label = request.json.get('label', 0)

    # If the server is not running, start it
    if server is None:
        thread = threading.Thread(target=start_osc_server)
        thread.daemon = True
        thread.start()

    return 'Started'

@app.route('/stop', methods=['POST'])
def stop():
    global server
    if server:
        server.shutdown()
        server = None
        return 'Data collection stopped'
    else:
        return 'No data collection is running'


@app.route('/predict', methods=['POST'])
def predict():
    global latest_hr, latest_eda, latest_temp
    if latest_hr is None or latest_eda is None or latest_temp is None:
        return jsonify({'error': 'No data available yet'})
    print(latest_hr, latest_eda, latest_temp)
    # Preprocess the latest data
    preprocessed_data = preprocess_data(latest_eda, latest_hr, latest_temp)
    # Predict the stress level
    stress_level = predict_stress_level(preprocessed_data)
    
    # Create response containing latest data and prediction
    prediction = {
        'hr': latest_hr,
        'eda': latest_eda,
        'temp': latest_temp,
        'stress_level': stress_level
    }
    return jsonify(prediction)

def preprocess_data(eda, hr, temp):
    # Preprocess the data if needed
    # Here, we are just scaling the data
    eda_scaled = eda / 100.0
    hr_scaled = hr / 100.0
    temp_scaled = temp / 100.0
    return [eda_scaled, hr_scaled, temp_scaled]

def predict_stress_level(data):
    # Convert the list to numpy array
    data_array = np.array([data])
    prediction = model.predict(data_array)
    stress_level = 'High' if prediction[0][0] > 0.5 else 'Low'
    return stress_level

if __name__ == "__main__":
    socketio.run(app, port=8080)
