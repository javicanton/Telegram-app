// Configuración base para las llamadas al backend
const API_URL = process.env.REACT_APP_BACKEND_URL;

// Funciones para manejar errores
const handleResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Error en la petición');
  }
  return response.json();
};

// Funciones para interactuar con el backend
export const api = {
  // Obtener datos
  getData: async () => {
    try {
      const response = await fetch(`${API_URL}/api/data`);
      return handleResponse(response);
    } catch (error) {
      console.error('Error al obtener datos:', error);
      throw error;
    }
  },

  // Crear nuevo dato
  createData: async (data) => {
    try {
      const response = await fetch(`${API_URL}/api/data`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      return handleResponse(response);
    } catch (error) {
      console.error('Error al crear datos:', error);
      throw error;
    }
  },

  // Actualizar dato existente
  updateData: async (id, data) => {
    try {
      const response = await fetch(`${API_URL}/api/data/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      return handleResponse(response);
    } catch (error) {
      console.error('Error al actualizar datos:', error);
      throw error;
    }
  },

  // Eliminar dato
  deleteData: async (id) => {
    try {
      const response = await fetch(`${API_URL}/api/data/${id}`, {
        method: 'DELETE',
      });
      return handleResponse(response);
    } catch (error) {
      console.error('Error al eliminar datos:', error);
      throw error;
    }
  },
}; 