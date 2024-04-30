import React from 'react';
import { BrowserRouter as Router, Route, NavLink, Routes } from 'react-router-dom';
import Screen1 from './pages/LiveWorkingEDA';
import Screen2 from './pages/LiveChart';
import Screen3 from './pages/CSVCreator';
import Screen4 from './pages/TestAPI';
import Screen5 from './pages/PredictedScreen';

const App = () => {
  return (
    <Router>
      <div>
        <nav style={navStyle}>
          <ul style={ulStyle}>
            <li style={liStyle}>
              <NavLink to="/screen1" style={linkStyle} activeStyle={activelink}>Live Data</NavLink>
            </li>
            <li style={liStyle}>
              <NavLink to="/screen2" style={linkStyle} activeStyle={activelink}>Example Display</NavLink>
            </li>
            <li style={liStyle}>
              <NavLink to="/screen3" style={linkStyle} activeStyle={activelink}>Build/Train</NavLink>
            </li>
            <li style={liStyle}>
              <NavLink to="/screen4" style={linkStyle} activeStyle={activelink}>Video</NavLink>
            </li>
            <li style={liStyle}>
              <NavLink to="/screen5" style={linkStyle} activeStyle={activelink}>Predictions</NavLink>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/screen1" element={<Screen1 />} />
          <Route path="/screen2" element={<Screen2 />} />
          <Route path="/screen3" element={<Screen3 />} />
          <Route path="/screen4" element={<Screen4 />} />
          <Route path="/screen5" element={<Screen5 />} />
        </Routes>
      </div>
    </Router>
  );
};

const navStyle = {
  backgroundColor: '#333',
  padding: '10px 0',
};

const ulStyle = {
  listStyleType: 'none',
  margin: 0,
  padding: 0,
  overflow: 'hidden',
};

const liStyle = {
  float: 'left',
};

const linkStyle = {
  display: 'block',
  color: 'white',
  textAlign: 'center',
  padding: '14px 16px',
  textDecoration: 'none',
};

const activelink = {
  color: '#4CAF50', 
};

export default App;