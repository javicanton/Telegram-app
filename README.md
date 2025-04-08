# Telegram-app

**Description:**  
Telegram-app is a fact-checking tool designed to track and analyze high-performing messages on Telegram channels. The tool collects message data, calculates engagement metrics, and exports the results in both CSV and Excel formats for further analysis.

**Key features:**

1. **Message Collection:** Extracts messages from specified Telegram channels with configurable time range and message limits.
2. **Engagement Metrics:** Calculates message views, average views per day, and engagement scores.
3. **Data Processing:** Processes messages and their metadata, including forwarded messages, replies, and media content.
4. **Export Formats:** Generates both CSV and Excel outputs for flexible data analysis.
5. **Progress Tracking:** Shows real-time progress of channel extraction with detailed status messages.

## Installation

1. Clone this repository
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Before running the application, you need to configure:

1. **Telegram API Credentials:**  
   You need to configure your Telegram API credentials. There are two ways to do this:

   a) **Using Environment Variables (Recommended):**

   ```bash
   # Add these to your ~/.zshrc (macOS/Linux with zsh) or ~/.bashrc (Linux with bash)
   export TELEGRAM_API_ID="your_api_id"
   export TELEGRAM_API_HASH="your_api_hash"
   ```

   b) **Using credentials.txt:**
   - Create a `credentials.txt` file based on `credentials.example.txt`
   - Add your API credentials in the following format:

   ```
   API_ID=your_api_id
   API_HASH=your_api_hash
   ```

   To obtain your API credentials:
   1. Visit <https://my.telegram.org/auth>
   2. Log in with your phone number
   3. Go to "API development tools"
   4. Create a new application
   5. Copy your `api_id` (a number) and `api_hash` (a string)

2. **telegram_channels.csv:**  
   This file contains the list of Telegram channels you want to monitor. To set it up:

   1. Create a `telegram_channels.csv` file based on `telegram_channels.example.csv`
   2. Add one channel username per line (without the @ symbol)
   3. For example, if you want to monitor <https://t.me/example>, add just "example"

## Usage

Run the script with:

```bash
python scraper.py
```

You will be prompted to enter:

- Number of days to scrape (default: 7)
- Maximum messages per channel to collect (default: 500)

The script will show progress for each channel:

- ✓ Success messages showing the number of messages processed
- ✗ Error messages for invalid or inaccessible channels

## Output Files

The script generates two output files:

1. **telegram_messages.csv:**
   - Contains all collected messages and their metadata
   - Includes engagement metrics and scores
   - Useful for data analysis and processing

2. **telegram_data.xlsx:**
   - Excel version of the data
   - Same information as the CSV but in Excel format
   - Better for visual inspection and quick analysis

## Privacy and Security

The following files are ignored by git to protect sensitive information:

1. **Credentials and Environment:**
   - `credentials.txt` - Contains your Telegram API credentials
   - `.env` - Environment variables file
   - `telegram_channels.csv` - Your private list of monitored channels

2. **Session Files:**
   - `anon.session` - Telegram session file
   - `*.session` - Any other session files
   - `*.session-journal` - Session journal files

3. **Generated Data:**
   - `telegram_messages.csv` - Collected message data
   - `telegram_data.xlsx` - Excel export of collected data

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Contact

If you have questions, comments, or suggestions, please feel free to get in touch:

- **Twitter:** [@ProsumidorSoc](https://twitter.com/ProsumidorSoc)
- **Email:** [javicanton@ugr.es](mailto:javicanton@ugr.es)

---

# Telegram-app

**Descripción:**  
Telegram-app es una herramienta de verificación de hechos diseñada para rastrear y analizar mensajes de alto rendimiento en canales de Telegram. La herramienta recopila datos de mensajes, calcula métricas de engagement y exporta los resultados en formatos CSV y Excel para su posterior análisis.

**Características principales:**

1. **Recopilación de Mensajes:** Extrae mensajes de canales específicos de Telegram con rango de tiempo y límites de mensajes configurables.
2. **Métricas de Engagement:** Calcula vistas de mensajes, promedio de vistas por día y puntuaciones de engagement.
3. **Procesamiento de Datos:** Procesa mensajes y sus metadatos, incluyendo mensajes reenviados, respuestas y contenido multimedia.
4. **Formatos de Exportación:** Genera salidas en CSV y Excel para un análisis flexible de datos.
5. **Seguimiento de Progreso:** Muestra el progreso en tiempo real de la extracción de canales con mensajes de estado detallados.

## Instalación

1. Clona este repositorio
2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Configuración

Antes de ejecutar la aplicación, necesitas configurar:

1. **Credenciales de la API de Telegram:**  
   Necesitas configurar tus credenciales de la API de Telegram. Hay dos formas de hacerlo:

   a) **Usando Variables de Entorno (Recomendado):**

   ```bash
   # Añade esto a tu ~/.zshrc (macOS/Linux con zsh) o ~/.bashrc (Linux con bash)
   export TELEGRAM_API_ID="tu_api_id"
   export TELEGRAM_API_HASH="tu_api_hash"
   ```

   b) **Usando credentials.txt:**
   - Crea un archivo `credentials.txt` basado en `credentials.example.txt`
   - Añade tus credenciales de API en el siguiente formato:

   ```
   API_ID=tu_api_id
   API_HASH=tu_api_hash
   ```

   Para obtener tus credenciales de API:
   1. Visita <https://my.telegram.org/auth>
   2. Inicia sesión con tu número de teléfono
   3. Ve a "API development tools"
   4. Crea una nueva aplicación
   5. Copia tu `api_id` (un número) y `api_hash` (una cadena de texto)

2. **telegram_channels.csv:**  
   Este archivo contiene la lista de canales de Telegram que deseas monitorizar. Para configurarlo:

   1. Crea un archivo `telegram_channels.csv` basado en `telegram_channels.example.csv`
   2. Añade un nombre de usuario de canal por línea (sin el símbolo @)
   3. Por ejemplo, si quieres monitorizar <https://t.me/ejemplo>, añade solo "ejemplo"

## Uso

Ejecuta el script con:

```bash
python scraper.py
```

Se te pedirá que ingreses:

- Número de días a rastrear (por defecto: 7)
- Máximo de mensajes por canal a recolectar (por defecto: 500)

El script mostrará el progreso para cada canal:

- ✓ Mensajes de éxito mostrando el número de mensajes procesados
- ✗ Mensajes de error para canales inválidos o inaccesibles

## Archivos de Salida

El script genera dos archivos de salida:

1. **telegram_messages.csv:**
   - Contiene todos los mensajes recopilados y sus metadatos
   - Incluye métricas de engagement y puntuaciones
   - Útil para análisis y procesamiento de datos

2. **telegram_data.xlsx:**
   - Versión Excel de los datos
   - Misma información que el CSV pero en formato Excel
   - Mejor para inspección visual y análisis rápido

## Privacidad y Seguridad

Los siguientes archivos son ignorados por git para proteger la información sensible:

1. **Credenciales y Entorno:**
   - `credentials.txt` - Contiene tus credenciales de API de Telegram
   - `.env` - Archivo de variables de entorno
   - `telegram_channels.csv` - Tu lista privada de canales monitorizados

2. **Archivos de Sesión:**
   - `anon.session` - Archivo de sesión de Telegram
   - `*.session` - Cualquier otro archivo de sesión
   - `*.session-journal` - Archivos journal de sesión

3. **Datos Generados:**
   - `telegram_messages.csv` - Datos de mensajes recopilados
   - `telegram_data.xlsx` - Exportación Excel de datos recopilados

## Licencia

Este proyecto está licenciado bajo la **Licencia MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Si tienes preguntas, comentarios o sugerencias, no dudes en ponerte en contacto:

- **Twitter:** [@ProsumidorSoc](https://twitter.com/ProsumidorSoc)
- **Correo Electrónico:** [javicanton@ugr.es](mailto:javicanton@ugr.es)
