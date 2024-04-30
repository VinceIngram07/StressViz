# StressViz


## Abstract

"StressViz is a comprehensive system designed to detect and visualize stress levels in real-time using Emotibit EDA data and neural networks. The system leverages physiological measurements and machine learning techniques to provide insightful feedback through an easy-to-use application. The goal of StressViz is to promote effective stress management and enhance overall well-being. The application is built with a React frontend and a Flask backend, and it integrates with the EmotiBit device for real-time data collection. This project, developed as a senior project at Morgan State University, aims to contribute to the field of mental health by providing a tool that helps individuals understand and manage their stress levels more effectively."

## Credits

StressViz was developed as a senior project at Morgan State University by the following team members:

Vincent Ingram
Emmanuel Olaleye
Marcus Cusaac
Savannah Sales
Tyrese Knight


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

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

## Usage

This application consists of a frontend developed with React and a backend developed with Flask. Here's how to run the application:

1. **Frontend**: Navigate to the frontend directory and start the React application:
    ```bash
    cd frontend/stressviz
    npm start
    ```
    This will start the React application, which by default runs on `http://localhost:3000`.

2. **Backend**: In a new terminal window, navigate to the `datasetmaker` directory and start the Flask application:
    ```bash
    cd Backend
    python app.py
    ```
    This will start the Flask application, which by default runs on `http://localhost:5000`.

Once both applications are running, you can use the application by opening a web browser and navigating to `http://localhost:3000`.

The application allows users to monitor their stress levels in real-time. Users can perform various tasks and see how these tasks affect their stress levels, helping them understand and manage their stress more effectively.

## Setup

1. **EmotiBit Setup**: Follow the [EmotiBit Documentation](https://github.com/EmotiBit/EmotiBit_Docs) to set up your EmotiBit device.

2. **File Replacement**: After setting up your EmotiBit, navigate to the `EmotiBit Oscilloscope` data directory, typically located at `C:\Program Files\EmotiBit\EmotiBit Oscilloscope\data`. Replace the existing files in this directory with the files from the `emotibit` directory in this repository. You can find the `emotibit` directory [here](link-to-emotibit-directory-in-your-repo).



## Project Structure

An overview of the files and directories in your project. For each file or directory, provide a brief description of what it does.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please make sure to update tests as appropriate.

## About This Project

This project was developed as a senior project for Morgan State University. It represents the culmination of years of study and was designed to provide real-world experience in developing and managing a full-stack application. The goal of the project was to create a system that could help people understand and manage their stress levels more effectively, contributing to overall well-being and mental health.

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

## References
