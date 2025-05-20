// frontend/src/components/MessageList.js
import React, { useState, useEffect } from 'react';
import { Box, Grid, CircularProgress, Typography } from '@mui/material';
import MessageCard from './MessageCard';

const MessageList = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        throw new Error('No hay token de autenticación');
      }

      const response = await fetch('/api/messages', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Error al cargar los mensajes');
      }

      const data = await response.json();
      if (data.success) {
        setMessages(data.messages);
      } else {
        throw new Error(data.error || 'Error al cargar los mensajes');
      }
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const handleLabel = async (messageId, label) => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        throw new Error('No hay token de autenticación');
      }

      const response = await fetch('/label', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ message_id: messageId, label }),
      });

      if (!response.ok) {
        throw new Error('Error al etiquetar el mensaje');
      }

      const data = await response.json();
      if (data.success) {
        setMessages(messages.map(msg => 
          msg['Message ID'] === messageId ? { ...msg, Label: label } : msg
        ));
      } else {
        throw new Error(data.error || 'Error al etiquetar el mensaje');
      }
    } catch (err) {
      console.error('Error al etiquetar:', err);
      alert(err.message);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ mt: 4 }}>
      <Grid container spacing={2}>
        {messages.map((message) => (
          <Grid item xs={12} md={6} lg={4} key={message['Message ID']}>
            <MessageCard 
              message={{
                Score: message['Score'] || 0,
                Message_ID: message['Message ID'],
                URL: message['URL'],
                Label: message['Label'],
                Embed: message['Embed']
              }}
              onLabelChange={handleLabel}
            />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default MessageList;