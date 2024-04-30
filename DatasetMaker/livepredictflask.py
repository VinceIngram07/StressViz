from flask import Flask, request, jsonify
from flask_cors import CORS
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import argparse
import numpy as np
import tensorflow as tf
import socketio

app = Flask(__name__)
CORS(app)

# Load the trained model
model = tf.keras.models.load_model('CheggModel.h5')

# Initialize variables to store received data
eda_data = None
hr_data = None
temp_data = None

sio = socketio.Server()
# Function to preprocess data
def preprocess_data(eda, hr, temp):
    eda_scaled = eda / 100.0
    hr_scaled = hr / 100.0
    temp_scaled = temp / 100.0
    return [eda_scaled, hr_scaled, temp_scaled]

# Function to predict stress level
def predict_stress_level(data):
    data_array = np.array([data]).reshape((1, len(data), 1))
    prediction = model.predict(data_array)
    stress_level = 'high' if prediction[0][0] > 0.5 else 'low'
    return stress_level, prediction[0][0] * 100

# OSC handler function
def osc_handler(address, *args):
    global eda_data, hr_data, temp_data

    if address == "/EmotiBit/0/EDA":
        eda_data = args[0] if len(args) > 0 else None
    elif address == "/EmotiBit/0/TEMP":
        temp_data = args[0] if len(args) > 0 else None
    elif address == "/EmotiBit/0/HR":
        hr_data = args[0] if len(args) > 0 else None

        if eda_data is not None and temp_data is not None:
            preprocessed_data = preprocess_data(eda_data, hr_data, temp_data)
            label, probability = predict_stress_level(preprocessed_data)
            sio.emit('stress_level', label)
            print(f"Predicted stress level: {label} with probability: {probability:.2f}%")

# OPTIONS request handler for /start endpoint
@app.route('/start', methods=['OPTIONS'])
def options():
    response = jsonify({'message': 'CORS headers set'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response

# POST request handler for /start endpoint
@app.route('/start', methods=['POST'])
def start_server():
    global server
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="172.20.10.10", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = Dispatcher()
    dispatcher.map("/EmotiBit/0/HR", osc_handler)
    dispatcher.map("/EmotiBit/0/EDA", osc_handler)
    dispatcher.map("/EmotiBit/0/TEMP", osc_handler)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

    return 'OSC server started'

if __name__ == "__main__":
    app.run(port=8080)
