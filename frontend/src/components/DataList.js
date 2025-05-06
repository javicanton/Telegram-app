import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

const DataList = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Cargar datos al montar el componente
  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await api.getData();
        setData(result);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Función para crear nuevo dato
  const handleCreate = async (newData) => {
    try {
      const result = await api.createData(newData);
      setData([...data, result]);
    } catch (err) {
      setError(err.message);
    }
  };

  // Función para actualizar dato
  const handleUpdate = async (id, updatedData) => {
    try {
      const result = await api.updateData(id, updatedData);
      setData(data.map(item => item.id === id ? result : item));
    } catch (err) {
      setError(err.message);
    }
  };

  // Función para eliminar dato
  const handleDelete = async (id) => {
    try {
      await api.deleteData(id);
      setData(data.filter(item => item.id !== id));
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Lista de Datos</h2>
      {data.map(item => (
        <div key={item.id}>
          {/* Renderizar los datos aquí */}
          <button onClick={() => handleDelete(item.id)}>Eliminar</button>
        </div>
      ))}
    </div>
  );
};

export default DataList; 