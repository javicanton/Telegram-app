import React, { useState, useEffect } from 'react';
import { Box, Typography, Button } from '@mui/material';
import { messagesAPI } from '../utils/api';

function DebugComponent() {
  const [debugInfo, setDebugInfo] = useState('');

  const testAPI = async () => {
    try {
      const response = await messagesAPI.getMessages({
        page: 1,
        per_page: 5
      });
      
      setDebugInfo(JSON.stringify(response, null, 2));
    } catch (error) {
      setDebugInfo(`Error: ${error.message}`);
    }
  };

  return (
    <Box sx={{ p: 2, border: '1px solid red', margin: 2 }}>
      <Typography variant="h6">Debug Info</Typography>
      <Button onClick={testAPI} variant="contained" sx={{ mb: 2 }}>
        Test API
      </Button>
      <pre style={{ fontSize: '12px', overflow: 'auto', maxHeight: '300px' }}>
        {debugInfo}
      </pre>
    </Box>
  );
}

export default DebugComponent;
