import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';

function MessageCard({ message, onLabelChange }) {
  const { Score, Message_ID, URL, Label, Embed } = message;

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent>
        <Typography variant="h6" component="div" align="center" gutterBottom>
          Overperforming Score: <span style={{ color: 'red' }}>{Score.toFixed(2)}x</span>
        </Typography>

        <Box 
          sx={{ 
            mb: 2,
            '& iframe': {
              width: '100%',
              border: 'none'
            }
          }}
          dangerouslySetInnerHTML={{ __html: Embed }}
        />

        <Box sx={{ display: 'flex', gap: 1, justifyContent: 'center', mt: 2 }}>
          <Button
            variant="contained"
            color={Label === 1 ? 'success' : 'primary'}
            onClick={() => onLabelChange(Message_ID, 1)}
          >
            Relevant
          </Button>
          <Button
            variant="contained"
            color={Label === 0 ? 'error' : 'primary'}
            onClick={() => onLabelChange(Message_ID, 0)}
          >
            Not Relevant
          </Button>
          <Link
            href={URL}
            target="_blank"
            rel="noopener noreferrer"
            sx={{ textDecoration: 'none' }}
          >
            <Button
              variant="contained"
              color="primary"
              fullWidth
            >
              Go to message
            </Button>
          </Link>
        </Box>
      </CardContent>
    </Card>
  );
}

export default MessageCard; 