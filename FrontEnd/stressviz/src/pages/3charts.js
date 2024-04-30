import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';
import Chart from 'chart.js/auto';

const App = () => {
  const [stream1Data, setStream1Data] = useState([]);
  const [stream2Data, setStream2Data] = useState([]);
  const [stream3Data, setStream3Data] = useState([]);
  const chart1Ref = useRef(null);
  const chart2Ref = useRef(null);
  const chart3Ref = useRef(null);

  useEffect(() => {
    const socket1 = io('/stream1');
    const socket2 = io('/stream2');
    const socket3 = io('/stream3');
  
    console.log('Connecting to stream1...');
    socket1.on('connect', () => {
      console.log('Connected to stream1');
    });
  
    console.log('Connecting to stream2...');
    socket2.on('connect', () => {
      console.log('Connected to stream2');
    });
  
    console.log('Connecting to stream3...');
    socket3.on('connect', () => {
      console.log('Connected to stream3');
    });
  
    socket1.on('stream1_data', (newData) => {
      console.log('Received data from stream1:', newData);
      setStream1Data((prevData) => [...prevData, newData]);
    });
  
    socket2.on('stream2_data', (newData) => {
      console.log('Received data from stream2:', newData);
      setStream2Data((prevData) => [...prevData, newData]);
    });
  
    socket3.on('stream3_data', (newData) => {
      console.log('Received data from stream3:', newData);
      setStream3Data((prevData) => [...prevData, newData]);
    });
  
    return () => {
      socket1.disconnect();
      socket2.disconnect();
      socket3.disconnect();
    };
  }, []);
  
  

  useEffect(() => {
    updateChart(chart1Ref, stream1Data);
  }, [stream1Data]);

  useEffect(() => {
    updateChart(chart2Ref, stream2Data);
  }, [stream2Data]);

  useEffect(() => {
    updateChart(chart3Ref, stream3Data);
  }, [stream3Data]);

  const updateChart = (chartRef, data) => {
    if (chartRef.current) {
      const ctx = chartRef.current.getContext('2d');
      if (ctx && chartRef.current.chart) {
        // Destroy previous chart instance if exists
        chartRef.current.chart.destroy();
      }
  
      chartRef.current.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: Array.from({ length: data.length }, (_, i) => i),
          datasets: [{
            label: 'Incoming Data',
            data: data.map((entry) => entry.data), // Assuming data format is { address: ..., data: ... }
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
          }]
        }
      });
    }
  };

  return (
    <div>
      <canvas id="chart1" ref={chart1Ref}></canvas>
      <canvas id="chart2" ref={chart2Ref}></canvas>
      <canvas id="chart3" ref={chart3Ref}></canvas>
    </div>
  );
};

export default App;
// Goes with test.py for straming data. (Not working)