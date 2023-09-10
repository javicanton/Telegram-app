Copiar archivos de carpeta a tgapp

En Terminal:
    cd tgapp
    docker build -t flask-telegram-app -f tgapp .

docker run -p 5001:5001 flask-telegram-app
