import React, { useState, useEffect } from 'react';
import { Box, Typography, CircularProgress } from '@mui/material';
import { messagesAPI } from '../utils/api';

function SimpleMessageList() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      setLoading(true);
      setError(null);

      console.log('Fetching messages...');
      const response = await messagesAPI.getMessages({
        page: 1,
        per_page: 5
      });

      console.log('Response:', response);

      if (response.success) {
        setMessages(response.messages || []);
        console.log('Messages set:', response.messages);
      } else {
        throw new Error(response.error || 'Error al cargar los mensajes');
      }
    } catch (err) {
      console.error('Error al cargar mensajes:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={4}>
        <Typography color="error">Error: {error}</Typography>
      </Box>
    );
  }

  return (
    <Box p={4}>
      <Typography variant="h6" gutterBottom>
        Mensajes ({messages.length})
      </Typography>
      {messages.map((message, index) => (
        <Box key={index} sx={{ mb: 2, p: 2, border: '1px solid #ccc' }}>
          <Typography variant="body1">
            ID: {message['Message ID']} - Score: {message.Score}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            URL: {message.URL}
          </Typography>
        </Box>
      ))}
    </Box>
  );
}

export default SimpleMessageList;
