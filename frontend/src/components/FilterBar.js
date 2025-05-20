import React, { useState, useEffect } from 'react';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import axios from 'axios';

function FilterBar({ onFilterChange }) {
  const [channels, setChannels] = useState([]);
  const [filters, setFilters] = useState({
    dateStart: '',
    dateEnd: '',
    channel: '',
    scoreMin: '',
    scoreMax: '',
    mediaType: '',
    sortBy: 'score'
  });

  useEffect(() => {
    // Cargar canales al montar el componente
    const fetchChannels = async () => {
      try {
        const response = await axios.get('/api/channels');
        setChannels(response.data);
      } catch (error) {
        console.error('Error fetching channels:', error);
      }
    };
    fetchChannels();
  }, []);

  const handleFilterChange = (field) => (event) => {
    const newFilters = {
      ...filters,
      [field]: event.target.value
    };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const handleReset = () => {
    const resetFilters = {
      dateStart: '',
      dateEnd: '',
      channel: '',
      scoreMin: '',
      scoreMax: '',
      mediaType: '',
      sortBy: 'score'
    };
    setFilters(resetFilters);
    onFilterChange(resetFilters);
  };

  return (
    <Paper sx={{ p: 2, mb: 2 }}>
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            fullWidth
            type="date"
            label="Desde"
            value={filters.dateStart}
            onChange={handleFilterChange('dateStart')}
            InputLabelProps={{ shrink: true }}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            fullWidth
            type="date"
            label="Hasta"
            value={filters.dateEnd}
            onChange={handleFilterChange('dateEnd')}
            InputLabelProps={{ shrink: true }}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            fullWidth
            select
            label="Canal"
            value={filters.channel}
            onChange={handleFilterChange('channel')}
          >
            <MenuItem value="">Todos</MenuItem>
            {channels.map((channel) => (
              <MenuItem key={channel} value={channel}>
                {channel}
              </MenuItem>
            ))}
          </TextField>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            fullWidth
            type="number"
            label="Puntuación Mín"
            value={filters.scoreMin}
            onChange={handleFilterChange('scoreMin')}
            inputProps={{ step: 0.1 }}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            fullWidth
            type="number"
            label="Puntuación Máx"
            value={filters.scoreMax}
            onChange={handleFilterChange('scoreMax')}
            inputProps={{ step: 0.1 }}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            fullWidth
            select
            label="Tipo Media"
            value={filters.mediaType}
            onChange={handleFilterChange('mediaType')}
          >
            <MenuItem value="">Todos</MenuItem>
            <MenuItem value="text">Texto</MenuItem>
            <MenuItem value="photo">Foto</MenuItem>
            <MenuItem value="video">Video</MenuItem>
            <MenuItem value="link">Enlace</MenuItem>
            <MenuItem value="document">Documento</MenuItem>
          </TextField>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <TextField
            fullWidth
            select
            label="Ordenar por"
            value={filters.sortBy}
            onChange={handleFilterChange('sortBy')}
          >
            <MenuItem value="score">Puntuación (Score)</MenuItem>
            <MenuItem value="views">Número de Vistas</MenuItem>
          </TextField>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Button
              variant="contained"
              color="primary"
              onClick={() => onFilterChange(filters)}
            >
              Aplicar Filtros
            </Button>
            <Button
              variant="contained"
              color="secondary"
              onClick={handleReset}
            >
              Limpiar Filtros
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Paper>
  );
}

export default FilterBar; 