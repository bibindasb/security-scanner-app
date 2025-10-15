// frontend/src/components/Layout/Layout.jsx
import React from 'react';
import { Box, AppBar, Toolbar, Typography, Container } from '@mui/material';
import { Security } from '@mui/icons-material';

const Layout = ({ children }) => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="static">
        <Toolbar>
          <Security sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Security Scanner
          </Typography>
        </Toolbar>
      </AppBar>
      
      <Container component="main" sx={{ flexGrow: 1, py: 3 }}>
        {children}
      </Container>
      
      <Box component="footer" sx={{ py: 2, bgcolor: 'background.paper', textAlign: 'center' }}>
        <Typography variant="body2" color="text.secondary">
          Security Scanner App © 2025
        </Typography>
      </Box>
    </Box>
  );
};

export default Layout;