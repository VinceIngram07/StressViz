import React, { useState } from 'react';
import axios from 'axios';
import BreathingExercises from './TestAPI';

function StartStop() {
  const [status, setStatus] = useState('');
  const [label, setLabel] = useState(0);
  const [username, setUsername] = useState('');

  const start = async () => {
    const response = await axios.post('http://localhost:8080/start', {
      label: label,
      username: username,
    });
    setStatus(response.data);
  };

  const stop = async () => {
    const response = await axios.post('http://localhost:8080/stop');
    setStatus(response.data);
  };

  const train = async () => {
    const response = await axios.post('http://localhost:8080/train', {});
    setStatus(response.data);
  };

  const handleLabelChange = (event) => {
    setLabel(event.target.value);
  };

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const appStyle = {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    backgroundColor: '#f5f5f5',
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
  };

  const inputStyle = {
    margin: '10px 0',
    padding: '10px',
    borderRadius: '5px',
    border: '1px solid #ccc',
  };

  const buttonStyle = {
    margin: '10px 2px',
    padding: '10px 20px',
    borderRadius: '5px',
    border: 'none',
    backgroundColor: '#007BFF',
    color: 'white',
    cursor: 'pointer',
  };

  const statusStyle = {
    marginTop: '20px',
    fontSize: '20px',
    color: '#333',
  };

  return (
    <div className="App" style={appStyle}>
      <BreathingExercises />
      <div style={{ marginLeft: '20px' }}>
        <label style={inputStyle}>
          Label:
          <input type="number" value={label} onChange={handleLabelChange} style={inputStyle} />
        </label>
        <label style={inputStyle}>
          Username:
          <input type="text" value={username} onChange={handleUsernameChange} style={inputStyle} />
        </label>
        <div>
          <button style={buttonStyle} onClick={start}>Start</button>
          <button style={buttonStyle} onClick={stop}>Stop</button>
          <button style={buttonStyle} onClick={train}>Train</button>
        </div>
        <p style={statusStyle}>Status: {status}</p>
      </div>
    </div>
  );
}

export default StartStop;