# Telegram-app

**Description:**  
Telegram-app is a fact-checking tool designed to track and tag high-performing messages on Telegram with the goal of combating misinformation.

**Key features:**.

1. **Web interface:** The app uses Flask to provide a web interface where users can view and tag Telegram messages.
2. **Data Processing:** Telegram messages are processed and ranked by relevance using natural language processing and machine learning techniques.
3. **Telegram crawling:** The application has a crawler that extracts messages from different Telegram channels based on specific criteria.
4. **Message Tagging:** Users can manually tag messages in the web interface, which helps improve the accuracy of the machine learning model.

Instructions for Use:** **.  
To deploy the application, follow the instructions provided in `instructions.md`. Basically, you need to build and run a Docker container that hosts the application.

**Main Files:**

- app.py`: Contains the main logic of the web application, including paths and associated functions.
- `model.py`: Defines the machine learning model and data processing required to classify messages.
- `scraper.py`: Is responsible for crawling and extracting messages from Telegram.

---

**Descripción:**  
Telegram-app es una herramienta de verificación de hechos diseñada para rastrear y etiquetar mensajes de alto rendimiento en Telegram con el objetivo de combatir la desinformación.

**Características principales:**

1. **Interfaz Web:** La aplicación utiliza Flask para proporcionar una interfaz web donde los usuarios pueden visualizar y etiquetar mensajes de Telegram.
2. **Procesamiento de Datos:** Los mensajes de Telegram se procesan y se clasifican según su relevancia utilizando técnicas de procesamiento de lenguaje natural y aprendizaje automático.
3. **Rastreo de Telegram:** La aplicación cuenta con un rastreador que extrae mensajes de diferentes canales de Telegram basándose en criterios específicos.
4. **Etiquetado de Mensajes:** Los usuarios pueden etiquetar manualmente los mensajes en la interfaz web, lo que ayuda a mejorar la precisión del modelo de aprendizaje automático.

**Instrucciones de Uso:**  
Para desplegar la aplicación, sigue las instrucciones proporcionadas en `instructions.md`. Básicamente, necesitas construir y ejecutar un contenedor Docker que aloje la aplicación.

**Archivos Principales:**

- `app.py`: Contiene la lógica principal de la aplicación web, incluyendo las rutas y las funciones asociadas.
- `model.py`: Define el modelo de aprendizaje automático y el procesamiento de datos necesario para clasificar los mensajes.
- `scraper.py`: Es responsable de rastrear y extraer mensajes de Telegram.