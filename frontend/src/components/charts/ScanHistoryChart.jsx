// frontend/src/components/charts/ScanHistoryChart.jsx
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const ScanHistoryChart = ({ scans }) => {
  const historyData = React.useMemo(() => {
    const last30Days = {};
    const today = new Date();
    
    // Initialize last 30 days
    for (let i = 29; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(date.getDate() - i);
      const dateString = date.toISOString().split('T')[0];
      last30Days[dateString] = { date: dateString, scans: 0, findings: 0 };
    }

    // Populate with actual data
    scans.forEach(scan => {
      const scanDate = new Date(scan.created_at).toISOString().split('T')[0];
      if (last30Days[scanDate]) {
        last30Days[scanDate].scans += 1;
        last30Days[scanDate].findings += scan.findings?.length || 0;
      }
    });

    return Object.values(last30Days);
  }, [scans]);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={historyData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="scans"
          stroke="#1976d2"
          strokeWidth={2}
          name="Scans"
        />
        <Line
          type="monotone"
          dataKey="findings"
          stroke="#dc004e"
          strokeWidth={2}
          name="Findings"
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default ScanHistoryChart;