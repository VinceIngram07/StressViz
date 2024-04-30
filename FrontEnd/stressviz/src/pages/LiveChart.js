import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';

const LiveChart = () => {
  const [data, setData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Heart Rate',
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
        label: 'Temperature',
        borderColor: 'rgb(255, 206, 86)',
        backgroundColor: 'rgba(255, 206, 86, 0.5)',
        data: [],
        fill: false,
      },
    ],
  });

  useEffect(() => {
    const interval = setInterval(() => {
      // Fetch or generate new data here
      const heartRate = Math.random() * 100;
      const eda = Math.random() * 10;
      const temperature = Math.random() * 30;

      // Update chart with new data
      setData(prevData => ({
        labels: [...prevData.labels, new Date().toISOString()],
        datasets: [
          {
            ...prevData.datasets[0],
            data: [...prevData.datasets[0].data, heartRate],
          },
          {
            ...prevData.datasets[1],
            data: [...prevData.datasets[1].data, eda],
          },
          {
            ...prevData.datasets[2],
            data: [...prevData.datasets[2].data, temperature],
          },
        ],
      }));
    }, 1000); // Update every second

    return () => clearInterval(interval);
  }, []);

  return <Line data={data} />;
};

export default LiveChart;
