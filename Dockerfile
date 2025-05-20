FROM python:3.10-slim

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Establecer directorio de trabajo
WORKDIR /app

# Copiar solo los archivos necesarios primero
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Crear usuario no root
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Exponer el puerto que usa Flask
EXPOSE 5001

# Comando para ejecutar la app
CMD ["python", "app.py"]