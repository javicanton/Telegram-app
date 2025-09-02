// frontend/src/components/MessageList.js
import React, { useState, useEffect } from 'react';
import { Box, Grid, CircularProgress, Typography } from '@mui/material';
import MessageCard from './MessageCard';

const MessageList = ({ filters }) => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMessages();
  }, []);

  useEffect(() => {
    if (Object.keys(filters).length > 0) {
      applyFilters(filters);
    }
  }, [filters]);

  const fetchMessages = async () => {
    try {
      // Detectar si usar endpoints sin autenticación
      const useNoAuth = !localStorage.getItem('access_token');
      const endpoint = useNoAuth ? '/noauth/api/messages' : '/api/messages';
      
      const headers = {};
      if (!useNoAuth) {
        const token = localStorage.getItem('access_token');
        if (!token) {
          throw new Error('No hay token de autenticación');
        }
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(endpoint, {
        headers
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

  const applyFilters = async (filters) => {
    try {
      setLoading(true);
      
      // Detectar si usar endpoints sin autenticación
      const useNoAuth = !localStorage.getItem('access_token');
      const endpoint = useNoAuth ? '/noauth/filter_messages' : '/filter_messages';
      
      const headers = {
        'Content-Type': 'application/json'
      };
      
      if (!useNoAuth) {
        const token = localStorage.getItem('access_token');
        if (token) {
          headers['Authorization'] = `Bearer ${token}`;
        }
      }

      const response = await fetch(endpoint, {
        method: 'POST',
        headers,
        body: JSON.stringify(filters)
      });

      if (!response.ok) {
        throw new Error('Error al aplicar filtros');
      }

      const data = await response.json();
      if (data.success) {
        setMessages(data.messages);
      } else {
        throw new Error(data.error || 'Error al aplicar filtros');
      }
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const handleLabel = async (messageId, label) => {
    try {
      // Detectar si usar endpoints sin autenticación
      const useNoAuth = !localStorage.getItem('access_token');
      
      // En modo sin autenticación, no permitir etiquetado
      if (useNoAuth) {
        alert('El etiquetado no está disponible en modo sin autenticación');
        return;
      }

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