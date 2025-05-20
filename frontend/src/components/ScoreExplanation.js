import React from 'react';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

function ScoreExplanation() {
  return (
    <Paper 
      elevation={0}
      sx={{
        bgcolor: '#f8f9fa',
        borderLeft: '4px solid #007bff',
        p: 2,
        my: 2,
        borderRadius: 1
      }}
    >
      <Typography variant="body1" color="text.secondary">
        El "Overperforming Score" es una métrica que indica cuánto mejor se desempeña un mensaje en comparación con el promedio de su canal. 
        Un score de 1.0 significa que el mensaje tiene un rendimiento promedio, mientras que un score mayor a 1.0 indica que el mensaje está 
        superando las expectativas. Por ejemplo, un score de 2.0 significa que el mensaje está obteniendo el doble de interacciones de lo esperado.
      </Typography>
    </Paper>
  );
}

export default ScoreExplanation; 