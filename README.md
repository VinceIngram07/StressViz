# StressViz
![StressViz Image](https://github.com/VinceIngram07/StressViz/blob/main/Videos/StressViz.png)

## Abstract

"StressViz is a comprehensive system designed to detect and visualize stress levels in real-time using Emotibit EDA data and neural networks. The system leverages physiological measurements and neural network techniques to provide insightful feedback through an easy-to-use application. The goal of StressViz is to promote effective stress management and enhance overall well-being. The application is built with a React frontend and a Flask backend, and it integrates with the EmotiBit device for real-time data collection. This project, developed as a senior project at Morgan State University, aims to contribute to the field of mental health by providing a tool that helps individuals understand and manage their stress levels more effectively."


## About This Project

This project was developed as a senior project for Morgan State University. It represents the culmination of years of study and was designed to provide real-world experience in developing and managing a full-stack application. The goal of the project was to create a system that could help people understand and manage their stress levels more effectively, contributing to overall well-being and mental health.

## Credits

StressViz was developed as a senior project at Morgan State University by the following team members:

Vincent Ingram,
Emmanuel Olaleye,
Marcus Cusaac,
Savannah Sales,
Tyrese Knight,


## Table of Contents

- [Abstract](#abstract)
- [About This Project](#about-this-project)
- [Credits](#credits)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Neural Network Model](#neural-network-model)
  - [Model Architecture](#model-architecture)
  - [Model Training](#model-training)
  - [Model Evaluation](#model-evaluation)
- [License](#license)
- [Why Use Our Product](#why-use-our-product)
- [Demonstration Videos](#demonstration-videos)
- [References](#references)

## Installation

This project requires several Python libraries, including Flask, Flask-CORS, Flask-SocketIO, argparse, csv, os, python-osc, numpy, pandas, TensorFlow, scikit-learn, and more. Here's how to install these dependencies:

1. **Python**: Download from the [official website](https://www.python.org/downloads/). Verify the installation by running `python --version` in your terminal.
2. **Python Libraries**: Install the necessary libraries using pip:
    - Flask: `pip install flask`
    - Flask-CORS: `pip install flask-cors`
    - Flask-SocketIO: `pip install flask-socketio`
    - argparse: This is part of the Python standard library and does not need to be installed separately.
    - csv: This is part of the Python standard library and does not need to be installed separately.
    - os: This is part of the Python standard library and does not need to be installed separately.
    - python-osc: `pip install python-osc`
    - numpy: `pip install numpy`
    - pandas: `pip install pandas`
    - TensorFlow: `pip install tensorflow`
    - scikit-learn: `pip install scikit-learn`
    - threading: This is part of the Python standard library and does not need to be installed separately.

You might need to use `python3` and `pip3` instead of `python` and `pip`, depending on your system configuration.

3. **React**: First, install Node.js and npm from the [official website](https://nodejs.org/en/download/). Verify the installation by running `node --version` and `npm --version` in your terminal. Then, create a new React application by running `npx create-react-app my-app` in your terminal.

## Setup

1. **EmotiBit Setup**: Follow the [EmotiBit Documentation](https://github.com/EmotiBit/EmotiBit_Docs) to set up your EmotiBit device. When setup use the Emotibit Oscilloscope application to send the Emotibit data Via OSC.
![Oscilloscope Image](https://github.com/VinceIngram07/StressViz/blob/main/Videos/osc.png)

2. **File Replacement**: After setting up your EmotiBit, navigate to the `EmotiBit Oscilloscope` data directory, typically located at `C:\Program Files\EmotiBit\EmotiBit Oscilloscope\data`. Replace the existing files in this directory with the files from the `emotibit` directory in this repository. You can find the `emotibit` directory [here](https://github.com/VinceIngram07/StressViz/tree/main/Emotibit).

## Usage

This application consists of a frontend developed with React and a backend developed with Flask. Here's how to run the application:

1. **Frontend**: Navigate to the frontend directory and start the React application:
    ```bash
    cd frontend/stressviz
    npm start
    ```
    This will start the React application, which by default runs on `http://localhost:3000`.

2. **Backend**: In a new terminal window, navigate to the `dataset maker` directory and start the Flask application:
    ```bash
    cd Backend
    python app.py
    ```
    This will start the Flask application, which by default runs on `http://localhost:5000`.

Once both applications are running, you can use the application by opening a web browser and navigating to `http://localhost:3000`.

The application allows users to monitor their stress levels in real time. Users can perform various tasks and see how these tasks affect their stress levels, helping them understand and manage their stress more effectively.

Now on `http://localhost:3000` there will be 5 tabs on the top the 2 main features are:

1. **Build/ Train**: In this window, you can create your dataset! We recommend starting with putting a different label with a different video that you can open and expand on the left to get your stress levels to different states. You can also set a username to set your dataset and model names to different people.
![Image](https://github.com/VinceIngram07/StressViz/blob/main/Videos/image.png)

3. **Prediction**: In this window, you can see the model predicting in real time! During this process, the Videos on the left are still available if you want to test if your model worked by putting you in the same stress state.
![Screenshot Image](https://github.com/VinceIngram07/StressViz/blob/main/Videos/Screenshot%202024-04-30%20230536.png)

## Project Structure

1. Backend: This is where all the Flask and server endpoints are dealt with and where the magic happens. There are many servers but the app.py is the most sophisticated.

2. Frontend: Using react we display the data being sent from the backend.

3. Model Iterations: Different versions of the models we used for testing and figuring out the best way to predict stress.

4. Videos: Content for the Readme file.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please make sure to update tests as appropriate.

# Neural Network Model

The neural network model used in this project is implemented using the Keras API with TensorFlow as the backend. The model is a type of Recurrent Neural Network (RNN) called Long Short-Term Memory (LSTM), which is particularly good at processing sequential data, making it a great choice for our time-series physiological data.

## Model Architecture

The model consists of an LSTM layer followed by a Dropout layer and a Dense layer:

- The LSTM layer has 50 units. LSTM layers maintain information in a 'cell state' over time, which helps them learn from the temporal aspects of the data.
- The Dropout layer randomly sets a fraction (0.2 in this case) of the input units to 0 at each update during training, which helps prevent overfitting.
- The Dense layer is the output layer of the network. It has 1 unit with a linear activation function, which is suitable for our regression problem.

## Model Training

The model is trained using the Adam optimizer and the Mean Squared Error (MSE) loss function. The Adam optimizer is an extension of stochastic gradient descent, which is known for its effectiveness in practice. The MSE loss function is commonly used in regression problems and it measures the average squared difference between the actual and predicted values.

The model is trained for 100 epochs with a batch size of 32. An epoch is one complete pass through the entire training dataset, and the batch size is the number of samples that are passed through the network at once.

## Model Evaluation

The model's performance is evaluated using several metrics:

- **Mean Squared Error (MSE):** This is the same as the loss function used during training. It measures the average squared difference between the actual and predicted values.
- **Accuracy:** This is the proportion of correct predictions out of all predictions. It's a common metric for classification problems.
- **Precision:** This is the proportion of true positive predictions out of all positive predictions. It's a measure of how many of the positive predictions were actually correct.
- **Recall:** This is the proportion of true positive predictions out of all actual positives. It's a measure of how many of the actual positive cases the model was able to catch.
- **F1 Score:** This is the harmonic mean of precision and recall. It provides a balance between the two metrics.

## License

This project is licensed under the terms of the MIT License. See the [LICENSE](LICENSE) file for details.

# Why Use Our Product

Our application is designed to provide real-time insights into your stress levels, helping you understand how different tasks and activities impact your mental well-being. Here are a few reasons why you should consider using our application:

1. **Real-Time Stress Monitoring**: Our application uses physiological data to predict stress levels in real-time. This allows you to see how your stress levels fluctuate throughout the day and during different activities.

2. **Personalized Insights**: By monitoring your stress levels over time, our application can provide personalized insights into what tasks or activities cause you the most stress. This can help you identify potential stressors in your life.

3. **Informed Decision Making**: With a better understanding of what causes your stress, you can make more informed decisions about how to manage your time and activities. For example, you might decide to take more breaks during stressful tasks, or to schedule relaxing activities after them.

4. **Improved Well-Being**: By helping you manage your stress more effectively, our application can contribute to improved mental well-being. Lower stress levels can lead to better sleep, improved focus, and a more positive outlook.

5. **Easy to Use**: Our application is user-friendly and easy to use. You can start monitoring your stress levels with just a few clicks.

In today's fast-paced world, stress management is more important than ever. Our application provides a simple and effective way to monitor and manage your stress levels, helping you lead a healthier and happier life.

## Demonstration Videos
[Link to the Low Stress video](https://github.com/VinceIngram07/StressViz/blob/main/Videos/Low%20Stress%20-%20Made%20with%20Clipchamp.mp4)
[Link to the High Stress video](https://github.com/VinceIngram07/StressViz/blob/main/Videos/High%20Stress%20-%20Made%20with%20Clipchamp%20(1).mp4)
[Link to the Updated Build & Train video](https://github.com/VinceIngram07/StressViz/blob/main/Videos/Updated%20Build_%20Train%20-%20Made%20with%20Clipchamp.mp4)

## References
