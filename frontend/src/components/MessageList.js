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
      let endpoint, data;
      
      if (useNoAuth) {
        // En modo sin autenticación, usar el nuevo endpoint /api/cards
        endpoint = '/api/cards';
        console.log('Fetching cards from:', endpoint, 'useNoAuth:', useNoAuth);
        
        const response = await fetch(endpoint);
        console.log('Response status:', response.status);

        if (!response.ok) {
          const errorText = await response.text();
          console.error('Error response:', errorText);
          throw new Error(`Error al cargar los mensajes: ${response.status} - ${errorText}`);
        }

        data = await response.json();
        console.log('Response data:', data);
        
        // Convertir el formato de /api/cards al formato esperado por MessageCard
        if (data.items && Array.isArray(data.items)) {
          const convertedMessages = data.items.map(item => ({
            'Message ID': item.id,
            'Message Text': item.description,
            'Title': item.title,
            'Score': item.score,
            'URL': item.url,
            'Label': null,
            'Embed': `<p>${item.description || 'Sin descripción'}</p>`
          }));
          setMessages(convertedMessages);
          console.log('Converted messages set in state:', convertedMessages);
        } else {
          setMessages([]);
        }
      } else {
        // Modo con autenticación, usar el endpoint original
        endpoint = '/api/messages';
        console.log('Fetching messages from:', endpoint, 'useNoAuth:', useNoAuth);
        
        const token = localStorage.getItem('access_token');
        if (!token) {
          throw new Error('No hay token de autenticación');
        }

        const response = await fetch(endpoint, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        console.log('Response status:', response.status);

        if (!response.ok) {
          const errorText = await response.text();
          console.error('Error response:', errorText);
          throw new Error(`Error al cargar los mensajes: ${response.status} - ${errorText}`);
        }

        data = await response.json();
        console.log('Response data:', data);
        console.log('Messages array:', data.messages);
        console.log('Messages length:', data.messages ? data.messages.length : 'undefined');
        
        if (data.success) {
          setMessages(data.messages);
          console.log('Messages set in state:', data.messages);
        } else {
          throw new Error(data.error || 'Error al cargar los mensajes');
        }
      }
      setLoading(false);
    } catch (err) {
      console.error('Error in fetchMessages:', err);
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
        {messages.map((message, index) => {
          if (index === 0) {
            console.log('First message object:', message);
            console.log('Available properties:', Object.keys(message));
          }
          return (
            <Grid item xs={12} md={6} lg={4} key={message['Message ID'] || index}>
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
          );
        })}
      </Grid>
    </Box>
  );
};

export default MessageList;