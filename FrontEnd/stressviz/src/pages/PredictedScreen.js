import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import BreathingExercises from './TestAPI'; // Import the BreathingExercises component

const PredictScreen = () => {
  const [prediction, setPrediction] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showVideos, setShowVideos] = useState(false);
  const [data, setData] = useState({
    labels: [],
    datasets: [
      {
        label: 'HR',
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        data: [],
        fill: false,
      },
      {
        label: 'EDA',
        borderColor: 'rgb(54, 162, 235)',
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
        data: [],
        fill: false,
      },
      {
        label: 'TEMP',
        borderColor: 'rgb(255, 206, 86)',
        backgroundColor: 'rgba(255, 206, 86, 0.5)',
        data: [],
        fill: false,
      },
      {
        label: 'Stress Level',
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
        data: [],
        fill: false,
      },
    ],
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.post('http://localhost:8080/predict');
        setPrediction(response.data);
        setData(prevData => ({
          labels: [...prevData.labels, new Date().toISOString()],
          datasets: [
            {
              ...prevData.datasets[0],
              data: [...prevData.datasets[0].data, response.data.hr],
            },
            {
              ...prevData.datasets[1],
              data: [...prevData.datasets[1].data, response.data.eda],
            },
            {
              ...prevData.datasets[2],
              data: [...prevData.datasets[2].data, response.data.temp],
            },
            {
              ...prevData.datasets[3],
              data: [...prevData.datasets[3].data, response.data.stress_level],
            },
          ],
        }));
      } catch (error) {
        setError('Error fetching prediction data');
      } finally {
        setLoading(false);
      }
    };

    const interval = setInterval(() => {
      fetchData();
    }, 1000); // Fetch data every 5 seconds

    fetchData(); // Fetch data immediately when the component mounts

    return () => clearInterval(interval); // Cleanup interval on unmount
  }, []);

  const containerStyle = {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    backgroundColor: '#f5f5f5',
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
  };

  const titleStyle = {
    color: '#007BFF',
    fontSize: '32px',
    marginBottom: '20px',
  };

  const dataStyle = {
    backgroundColor: '#fff',
    borderRadius: '5px',
    padding: '20px',
    margin: '10px 0',
    width: '100%',
    maxWidth: '600px',
    boxShadow: '0 0 10px rgba(0,0,0,0.1)',
  };

  const errorStyle = {
    color: 'red',
    fontSize: '20px',
  };

  return (
    <div style={containerStyle}>
      <BreathingExercises /> {/* Move this to the top */}
      <div style={{ marginLeft: '20px' }}> {/* Add this div */}
        <h2 style={titleStyle}>Predict Screen</h2>
        {loading && <p>Loading...</p>}
        {error && <p style={errorStyle}>{error}</p>}
        {!loading && !error && (
          <div style={dataStyle}>
            <p>Latest HR: {prediction.hr}</p>
            <p>Latest EDA: {prediction.eda}</p>
            <p>Latest TEMP: {prediction.temp}</p>
            <p>Stress Level: {prediction.stress_level}</p>
            <p>Probability: {prediction.probability}%</p> {/* Add this line */}
            <Line data={data} />
          </div>
        )}
      </div>
    </div>
  );
};

export default PredictScreen;