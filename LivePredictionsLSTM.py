import argparse
import numpy as np
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import tensorflow as tf
import socketio

# Load the trained model
model = tf.keras.models.load_model('stressLSTM.h5')

# Initialize variables to store received data
eda_data = None
hr_data = None
temp_data = None


sio = socketio.Server()
app = socketio.WSGIApp(sio)

labels = ['medium', 'low', 'high']

def preprocess_data(eda, hr, temp):
    eda_scaled = eda / 200.0
    hr_scaled = hr / 200.0
    temp_scaled = temp / 200.0
    return [eda_scaled, hr_scaled, temp_scaled]

def predict_stress_level(data):
    # Convert the list to numpy array and add a time step dimension
    data_array = np.array([data]).reshape((1, 1, len(data)))
    prediction = model.predict(data_array)
    max_index = prediction[0].argmax()
    max_label = labels[max_index]
    max_probability = prediction[0][max_index]
    return max_label, max_probability * 100  # return label and probability in percentage

def osc_handler(address, *args):
    global eda_data, hr_data, temp_data

    # print(f"Received data from {address}: {args}")
    
    # Check the address and update corresponding data
    if address == "/EmotiBit/0/EDA":
        eda_data = args[0] if len(args) > 0 else None
    elif address == "/EmotiBit/0/TEMP":
        temp_data = args[0] if len(args) > 0 else None
    elif address == "/EmotiBit/0/HR":
        hr_data = args[0] if len(args) > 0 else None

        # If all data is available, preprocess and predict
        if eda_data is not None and temp_data is not None:
                preprocessed_data = preprocess_data(eda_data, hr_data, temp_data)
                label, probability = predict_stress_level(preprocessed_data)
                sio.emit('stress_level', label)
                print(f"Predicted stress level: {label} with probability: {probability:.2f}%")

if __name__ == "__main__":
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