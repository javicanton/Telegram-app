FROM python:3.9-slim

WORKDIR /app

# Instala curl para el healthcheck y dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Actualiza pip antes de instalar dependencias
RUN pip install --upgrade pip

# Copia e instala dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación
COPY . .

EXPOSE 5001

CMD ["python", "app.py"] 