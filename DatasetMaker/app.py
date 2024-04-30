from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import threading
import argparse
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import numpy as np
import tensorflow as tf

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

latest_hr = None
latest_eda = None
latest_temp = None

# Load the trained model
model = tf.keras.models.load_model('Stress.h5')

# Function to continuously update the latest HR, EDA, and TEMP values
def update_latest_values():
    global latest_hr, latest_eda, latest_temp
    def print_handler(address, *args):
        global latest_hr, latest_eda, latest_temp
        if address == "/EmotiBit/0/HR":
            latest_hr = args[0]
        elif address == "/EmotiBit/0/EDA":
            latest_eda = args[0]
        elif address == "/EmotiBit/0/TEMP":
            latest_temp = args[0]

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="172.20.10.10", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = Dispatcher()
    dispatcher.map("/EmotiBit/0/HR", print_handler)
    dispatcher.map("/EmotiBit/0/EDA", print_handler)
    dispatcher.map("/EmotiBit/0/TEMP", print_handler)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    server.serve_forever()

# Start the thread to continuously update the latest values
thread = threading.Thread(target=update_latest_values)
thread.daemon = True
thread.start()

# Function to preprocess data
def preprocess_data(eda, hr, temp):
    # Preprocess the data if needed
    # Here, we are just scaling the data
    eda_scaled = eda / 100.0  # Example scaling
    hr_scaled = hr / 100.0  # Example scaling
    temp_scaled = temp / 100.0  # Example scaling
    return [eda_scaled, hr_scaled, temp_scaled]

# Function to predict stress level
def predict_stress_level(data):
    # Convert the list to numpy array
    data_array = np.array([data])
    prediction = model.predict(data_array)
    # Get the predicted stress level from the prediction array
    stress_level = 'High' if prediction[0][0] > 0.5 else 'Low'
    return stress_level


@app.route('/predict', methods=['POST'])
def predict():
    global latest_hr, latest_eda, latest_temp
    if latest_hr is None or latest_eda is None or latest_temp is None:
        return jsonify({'error': 'No data available yet'})

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

if __name__ == "__main__":
    socketio.run(app, port=8080)
