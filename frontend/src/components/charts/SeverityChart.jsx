// frontend/src/components/charts/SeverityChart.jsx
import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const SeverityChart = ({ scans }) => {
  const severityData = React.useMemo(() => {
    const severityCounts = {
      critical: 0,
      high: 0,
      medium: 0,
      low: 0,
      info: 0,
    };

    scans.forEach(scan => {
      scan.findings?.forEach(finding => {
        severityCounts[finding.severity] = (severityCounts[finding.severity] || 0) + 1;
      });
    });

    return Object.entries(severityCounts).map(([name, value]) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1),
      value,
    })).filter(item => item.value > 0);
  }, [scans]);

  const COLORS = {
    Critical: '#f44336',
    High: '#ff9800',
    Medium: '#ffc107',
    Low: '#4caf50',
    Info: '#2196f3',
  };

  if (severityData.length === 0) {
    return (
      <Box sx={{ textAlign: 'center', py: 4 }}>
        <Typography color="textSecondary">
          No severity data available
        </Typography>
      </Box>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={severityData}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
          outerRadius={80}
          fill="#8884d8"
          dataKey="value"
        >
          {severityData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[entry.name]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
};

export default SeverityChart;