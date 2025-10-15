// frontend/src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { theme } from './theme';
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard';
import ScanList from './pages/ScanList';
import ScanDetail from './pages/ScanDetail';
import NewScan from './pages/NewScan';
import Settings from './pages/Settings';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/scans" element={<ScanList />} />
            <Route path="/scans/new" element={<NewScan />} />
            <Route path="/scans/:id" element={<ScanDetail />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  );
}

export default App;