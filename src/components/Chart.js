// components/Chart.js
import React from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";
import { Line } from "react-chartjs-2";

// ✅ Register all pieces ONCE!
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default function Chart({ pair, data }) {
  if (!data || !data.labels) {
    return <p>No chart data available.</p>;
  }

  const options = {
    responsive: true,
    plugins: {
      legend: { position: "top" },
      title: { display: true, text: `Price Chart for ${pair}` },
    },
    interaction: {
      mode: 'index',
      intersect: false
    },
    scales: {
      x: { title: { display: true, text: "Time" } },
      y: { title: { display: true, text: "Last Trade Price" } }
    }
  };

  return <Line options={options} data={data} />;
}
