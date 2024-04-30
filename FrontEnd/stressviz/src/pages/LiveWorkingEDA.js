import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';
import Chart from 'chart.js/auto';

const App = () => {
  const [data, setData] = useState([]);
  const chartRef = useRef(null);

  useEffect(() => {
    const socket = io('http://localhost:5000');

    socket.on('message', (newData) => {
      setData((prevData) => [...prevData, newData]);
    });
  }, []);

  useEffect(() => {
    const ctx = document.getElementById('myChart');
    if (ctx) {
      // If a chart already exists, destroy it
      if (chartRef.current) {
        chartRef.current.destroy();
      }

      const newChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: Array.from({ length: data.length }, (_, i) => i),
          datasets: [{
            label: 'Incoming Data',
            data: data,
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
          }]
        }
      });
      chartRef.current = newChart;
    }
  }, [data]);

  return (
    <div>
      <canvas id="myChart"></canvas>
    </div>
  );
};

export default App;