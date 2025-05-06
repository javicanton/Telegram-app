FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar todos los archivos del proyecto
COPY . /app

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que usa Flask
EXPOSE 5001

# Comando para ejecutar la app
CMD ["python", "app.py"]