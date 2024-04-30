// import React, { useState } from 'react';
// import axios from 'axios';

// const PredictionControlScreen = () => {
//   const [ipAddress, setIpAddress] = useState('127.0.0.1');
//   const [port, setPort] = useState(5006);
//   const [isPredictionStarted, setIsPredictionStarted] = useState(false);

//   const startPrediction = async () => {
//     try {
//       await axios.post('http://localhost:8080/start_prediction', {
//         ip: ipAddress,
//         port: port
//       });
//       setIsPredictionStarted(true);
//     } catch (error) {
//       console.error('Error starting prediction:', error);
//     }
//   };

//   const stopPrediction = async () => {
//     try {
//       await axios.post('http://localhost:8080/stop_prediction');
//       setIsPredictionStarted(false);
//     } catch (error) {
//       console.error('Error stopping prediction:', error);
//     }
//   };

//   return (
//     <div>
//       <h1>Prediction Control</h1>
//       <div>
//         <label>
//           IP Address:
//           <input
//             type="text"
//             value={ipAddress}
//             onChange={(e) => setIpAddress(e.target.value)}
//           />
//         </label>
//         <label>
//           Port:
//           <input
//             type="number"
//             value={port}
//             onChange={(e) => setPort(e.target.value)}
//           />
//         </label>
//       </div>
//       <button onClick={startPrediction} disabled={isPredictionStarted}>
//         Start Prediction
//       </button>
//       <button onClick={stopPrediction} disabled={!isPredictionStarted}>
//         Stop Prediction
//       </button>
//     </div>
//   );
// };

// export default PredictionControlScreen;

import React, { useState } from 'react';
import axios from 'axios';

const PredictionControlScreen = () => {
  const [ipAddress, setIpAddress] = useState('127.0.0.1');
  const [port, setPort] = useState(5005); // Change the default port to match the OSC server port
  const [isPredictionStarted, setIsPredictionStarted] = useState(false);

  const startPrediction = async () => {
    try {
      await axios.post('http://localhost:8080/start', {
        ip: ipAddress,
        port: port
      });
      setIsPredictionStarted(true);
    } catch (error) {
      console.error('Error starting prediction:', error);
    }
  };

  const stopPrediction = async () => {
    try {
      await axios.post('http://localhost:8080/stop');
      setIsPredictionStarted(false);
    } catch (error) {
      console.error('Error stopping prediction:', error);
    }
  };

  return (
    <div>
      <h1>Prediction Control</h1>
      <div>
        <label>
          IP Address:
          <input
            type="text"
            value={ipAddress}
            onChange={(e) => setIpAddress(e.target.value)}
          />
        </label>
        <label>
          Port:
          <input
            type="number"
            value={port}
            onChange={(e) => setPort(e.target.value)}
          />
        </label>
      </div>
      <button onClick={startPrediction} disabled={isPredictionStarted}>
        Start Prediction
      </button>
      <button onClick={stopPrediction} disabled={!isPredictionStarted}>
        Stop Prediction
      </button>
    </div>
  );
};

export default PredictionControlScreen;
