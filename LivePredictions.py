import argparse
import csv
import numpy as np
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import tensorflow as tf

# Load the trained model
model = tf.keras.models.load_model('Stress.h5')

# Initialize variables to store received data
eda_data = None
hr_data = None
temp_data = None

def preprocess_data(eda, hr, temp):
    # Preprocess the data if needed
    # Here, we are just scaling the data
    eda_scaled = eda / 100.0  # Example scaling
    hr_scaled = hr / 100.0  # Example scaling
    temp_scaled = temp / 100.0  # Example scaling
    return [eda_scaled, hr_scaled, temp_scaled]

def predict_stress_level(data):
    # Convert the list to numpy array
    data_array = np.array([data])
    print ('Test')
    print (data_array)
    prediction = model.predict(data_array)
    # Format the prediction as a string in standard notation
    prediction_str = np.array2string(prediction, formatter={'float_kind': lambda x: "%.6f" % x})
    return prediction_str

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
