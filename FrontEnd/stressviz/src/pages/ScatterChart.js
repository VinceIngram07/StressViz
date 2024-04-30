import React from "react";
import { Chart } from "react-google-charts";

// Some sample eda data
const data = [
  ["Age", "Weight"],
  [4, 5.5],
  [8, 12],
  [15, 14],
  [16, 15],
  [18, 16],
  [20, 18],
  [25, 20],
  [30, 22],
  [35, 23],
  [40, 25],
  [45, 26],
  [50, 28],
];

// Some options for the chart
const options = {
  title: "Age vs. Weight",
  hAxis: { title: "Age", minValue: 0, maxValue: 50 },
  vAxis: { title: "Weight", minValue: 0, maxValue: 30 },
  legend: "none",
};

// The chart component
const ScatterChart = () => {
  return (
    <div className="App">
      <Chart
        chartType="ScatterChart"
        data={data}
        options={options}
        width="100%"
        height="400px"
        legendToggle
      />
    </div>
  );
};

export default ScatterChart;
