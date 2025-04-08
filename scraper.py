## Telegram Scraper
# Import libraries
import asyncio
import csv
import os
from telethon import TelegramClient
from telethon.errors import ChannelInvalidError, ChatAdminRequiredError
from telethon.tl.types import Message, Channel, User
from telethon.tl.custom import Message as CustomMessage
from telethon.tl.types.messages import Messages
from telethon.tl.types.messages import ChannelMessages
from datetime import datetime, timedelta, timezone
import pandas as pd
import sys
from typing import List, Optional, Dict, Any, Union, cast

# Set the working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_credentials_from_user():
    """Solicita las credenciales al usuario y las guarda en un archivo"""
    print("\nPrimera vez usando la aplicación. Necesitamos tus credenciales de Telegram.")
    print("Para obtenerlas:")
    print("1. Visita https://my.telegram.org/auth")
    print("2. Inicia sesión con tu número de teléfono")
    print("3. Ve a 'API development tools'")
    print("4. Crea una nueva aplicación")
    print("5. Copia tu api_id (número) y api_hash (cadena de texto)\n")
    
    while True:
        try:
            api_id = input("Ingresa tu API ID (número): ").strip()
            if not api_id:
                raise ValueError("El API ID no puede estar vacío")
            api_id = int(api_id)
            break
        except ValueError:
            print("Error: El API ID debe ser un número entero válido")
    
    while True:
        api_hash = input("Ingresa tu API Hash: ").strip()
        if not api_hash:
            print("Error: El API Hash no puede estar vacío")
            continue
        break
    
    # Guardar las credenciales en el archivo
    with open('credentials.txt', 'w') as f:
        f.write(f"API_ID={api_id}\n")
        f.write(f"API_HASH={api_hash}\n")
    
    print("\n✓ Credenciales guardadas correctamente en credentials.txt")
    return {'API_ID': api_id, 'API_HASH': api_hash}

def ask_use_existing_file(filename, file_description):
    """Pregunta al usuario si quiere usar un archivo existente"""
    if os.path.exists(filename):
        while True:
            respuesta = input(f"\n¿Quieres usar el archivo {filename} existente para {file_description}? (s/n): ").strip().lower()
            if respuesta in ['s', 'n']:
                return respuesta == 's'
            print("Por favor, responde 's' para sí o 'n' para no")

def load_credentials(filename='credentials.txt'):
    """
    Carga las credenciales desde un archivo o variables de entorno.
    Si no existen o el usuario no quiere usarlas, solicita las credenciales al usuario.
    """
    # Preguntar si quiere usar el archivo existente
    if ask_use_existing_file(filename, "las credenciales de Telegram"):
        try:
            credentials = {}
            with open(filename, 'r') as file:
                for line in file:
                    key, value = line.strip().split('=')
                    if key == 'API_ID':
                        try:
                            credentials[key] = int(value)
                        except ValueError:
                            print(f"Error: API_ID debe ser un número entero válido en {filename}")
                            return get_credentials_from_user()
                    else:
                        credentials[key] = value
            return credentials
        except Exception as e:
            print(f"Error al leer {filename}: {str(e)}")
            return get_credentials_from_user()
    else:
        return get_credentials_from_user()

def get_user_input():
    """Obtiene la configuración del usuario"""
    try:
        days = input("Ingresa el número de días a scrapear (deja en blanco para usar 7 días): ")
        days = int(days) if days.strip() else 7
        
        messages = input("Ingresa el número máximo de mensajes por canal (deja en blanco para usar 500): ")
        messages = int(messages) if messages.strip() else 500
        
        return days, messages
    except ValueError:
        print("Valor inválido. Usando valores por defecto (7 días, 500 mensajes)")
        return 7, 500

def get_channels_from_user():
    """Solicita los canales al usuario y los guarda en un archivo CSV"""
    # Preguntar si quiere usar el archivo existente solo si existe
    if os.path.exists('telegram_channels.csv'):
        if ask_use_existing_file('telegram_channels.csv', "la lista de canales"):
            channels = load_channels_from_csv('telegram_channels.csv')
            if channels:
                return channels
    
    # Si llegamos aquí, es porque el archivo no existe o el usuario no quiere usarlo
    print("\n¿Cómo quieres proporcionar los canales?")
    print("1. Ingresar un solo canal")
    print("2. Proporcionar un archivo CSV con la lista de canales")
    
    while True:
        try:
            opcion = input("\nElige una opción (1-2): ").strip()
            if opcion not in ['1', '2']:
                raise ValueError("Opción no válida")
            break
        except ValueError:
            print("Error: Debes elegir una opción entre 1 y 2")
    
    channels = []
    
    if opcion == '1':
        while True:
            channel = input("\nIngresa el nombre del canal (sin @): ").strip()
            if not channel:
                print("Error: El nombre del canal no puede estar vacío")
                continue
            channels.append(channel)
            break
    
    elif opcion == '2':
        while True:
            csv_path = input("\nIngresa la ruta al archivo CSV: ").strip()
            if not csv_path:
                print("Error: La ruta no puede estar vacía")
                continue
            if not os.path.exists(csv_path):
                print(f"Error: No se encontró el archivo {csv_path}")
                continue
            try:
                channels = load_channels_from_csv(csv_path)
                break
            except Exception as e:
                print(f"Error al leer el archivo CSV: {str(e)}")
                continue
    
    # Guardar los canales en el archivo
    with open('telegram_channels.csv', 'w', encoding='utf-8') as f:
        for channel in channels:
            f.write(f"{channel}\n")
    
    print(f"\n✓ Se han guardado {len(channels)} canales en telegram_channels.csv")
    return channels

def load_channels_from_csv(filename):
    """Carga los canales desde un archivo CSV"""
    channels = []
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and row[0].strip():  # Check if row is not empty and first element is not empty
                    channel = row[0].strip()
                    if not channel.startswith('#'):  # Ignorar líneas de comentario
                        channels.append(channel)
    except Exception as e:
        print(f"Error al leer {filename}: {str(e)}")
        return []
    return channels

def extract_channel_details(channel):
    return {
        'Channel ID': channel.id,
        'Username': channel.username,
        'Title': channel.title,
        'Description': getattr(channel, 'description', 'N/A'),
        'Photo': channel.photo,
        'Creation Date': getattr(channel, 'date', 'N/A'),
        'Verified': getattr(channel, 'verified', False),
        'Restricted': getattr(channel, 'restricted', False),
        'Members Count': getattr(channel, 'participants_count', 0)
    }

def extract_message_details(message):
    # Construct the URL
    url = f"https://t.me/s/{message.sender_id}/{message.id}"
    
    # Construct the Embed
    embed = f'<script async src="https://telegram.org/js/telegram-widget.js?22" data-telegram-post="{message.sender_id}/{message.id}" data-width="100%"></script>'
    
    return {
        'Message ID': message.id,
        'Message Text': message.text or '',
        'Date Sent': message.date,
        'Views': message.views or 0,
        'Forwarded From': getattr(message.forward, 'sender_id', None) if message.forward else None,
        'Reply To': message.reply_to_msg_id,
        'Mentions': message.mentioned,
        'Media': message.media,
        'Entities': message.entities,
        'Edit Date': message.edit_date,
        'Sender ID': message.sender_id,
        'URL': url,
        'Embed': embed
    }

def extract_media_details(media):
    media_type = type(media).__name__
    
    # Simplificar los tipos de medios
    if media_type == 'MessageMediaPhoto':
        simplified_type = 'Photo'
    elif media_type == 'MessageMediaDocument':
        # Verificar atributos específicos del documento
        if hasattr(media.document, 'attributes'):
            for attr in media.document.attributes:
                if hasattr(attr, 'video'):
                    simplified_type = 'Video'
                    break
                elif hasattr(attr, 'audio'):
                    if hasattr(attr, 'voice'):
                        simplified_type = 'Voice'
                    else:
                        simplified_type = 'Audio'
                    break
                elif hasattr(attr, 'sticker'):
                    simplified_type = 'Sticker'
                    break
                elif hasattr(attr, 'gif'):
                    simplified_type = 'GIF'
                    break
            else:
                simplified_type = 'Document'
    elif media_type == 'MessageMediaWebPage':
        simplified_type = 'Webpage'
    elif media_type == 'MessageMediaPoll':
        simplified_type = 'Poll'
    elif media_type == 'MessageMediaContact':
        simplified_type = 'Contact'
    elif media_type == 'MessageMediaGeo':
        simplified_type = 'Geo'
    elif media_type == 'MessageMediaGame':
        simplified_type = 'Game'
    else:
        simplified_type = media_type
    
    return {
        'Media Type': simplified_type,
        'Media Size': getattr(media, 'size', None),
        'Media Caption': getattr(media, 'caption', None)
    }

def load_existing_data(filename):
    try:
        return pd.read_csv(filename)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame()

def load_existing_message_ids(filename):
    try:
        existing_data = pd.read_csv(filename)
        # Create a set of tuples (Username, Message ID) for fast lookup
        existing_ids = set(zip(existing_data['Username'], existing_data['Message ID']))
        return existing_ids
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return set()

async def main():
    print("1. Iniciando script...")
    
    # Cargar credenciales
    print("2. Cargando credenciales...")
    creds = load_credentials()
    if not creds:
        print("Error: No se pudieron cargar las credenciales")
        return
    
    # Cargar canales
    print("3. Cargando lista de canales...")
    channels = get_channels_from_user()
    if not channels:
        print("Error: No se pudieron cargar los canales")
        return
    print(f"4. Se encontraron {len(channels)} canales para procesar")
    
    # Obtener configuración del usuario
    print("5. Configuración...")
    days_to_scrape, max_messages = get_user_input()
    time_days_ago = datetime.now(timezone.utc) - timedelta(days=days_to_scrape)
    print(f"6. Configuración: {days_to_scrape} días, {max_messages} mensajes por canal")
    
    # Cargar datos existentes
    print("7. Cargando datos existentes...")
    existing_messages = load_existing_data('telegram_messages.csv')
    existing_ids = load_existing_message_ids('telegram_messages.csv')
    
    # Crear cliente
    print("8. Creando cliente...")
    client = TelegramClient('anon', creds['API_ID'], creds['API_HASH'])
    
    try:
        # Conectar
        print("9. Conectando...")
        await client.connect()
        
        # Verificar autorización
        print("10. Verificando autorización...")
        if not await client.is_user_authorized():
            print("11. Necesitas autorizar el acceso:")
            print("   - Abre Telegram en tu dispositivo")
            print("   - Busca un mensaje con un código de verificación")
            print("   - Ingresa el código cuando se te solicite")
            await client.start()
        
        print("12. Conexión exitosa!")
        
        all_data = []
        for channel in channels:
            try:
                print(f"Procesando canal: {channel}")
                channel_details = await client.get_entity(channel)
                messages = await client.get_messages(
                    channel,
                    limit=max_messages,
                    offset_date=time_days_ago
                )
                
                if not messages:
                    print(f"No se encontraron mensajes para el canal '{channel}'. Continuando con el siguiente.")
                    continue

                # Convert messages to list for easier handling
                messages_list = list(messages)

                # Group messages by their date
                grouped_messages: Dict[str, List[Message]] = {}
                for message in messages_list:
                    if message and message.date:
                        date_str = message.date.strftime('%Y-%m-%d')
                        if date_str not in grouped_messages:
                            grouped_messages[date_str] = []
                        grouped_messages[date_str].append(message)

                # Calculate daily average views
                daily_average_views: Dict[str, float] = {}
                for date_str, daily_messages in grouped_messages.items():
                    views_list = [message.views for message in daily_messages if message.views is not None]
                    daily_average_views[date_str] = sum(views_list) / len(views_list) if views_list else 0

                # Contadores para mensajes
                mensajes_existentes = 0
                mensajes_nuevos = 0

                for message in messages_list:
                    if not message or not message.date:
                        continue
                        
                    data: Dict[str, Any] = {}
                    data.update(extract_channel_details(channel_details))
                    data.update(extract_message_details(message))
                    
                    # Verificar si el mensaje ya existe en el dataset
                    message_key = (data['Username'], message.id)
                    if message_key in existing_ids:
                        mensajes_existentes += 1
                        continue
        
                    # Update the URL and Embed columns using the channel's username
                    channel_username = data['Username']
                    if not channel_username:  # Si no hay username, usar el ID
                        channel_username = str(data['Channel ID'])
                    data['URL'] = f"https://t.me/s/{channel_username}/{message.id}"
                    data['Embed'] = f'<script async src="https://telegram.org/js/telegram-widget.js?22" data-telegram-post="{channel_username}/{message.id}" data-width="100%"></script>'
                    
                    date_str = message.date.strftime('%Y-%m-%d')
                    data['Average Views'] = daily_average_views.get(date_str, 0)
                    
                    # Calcular la diferencia con el promedio
                    if data['Average Views'] > 0:
                        data['Average Difference'] = (message.views or 0) - data['Average Views']
                        # Calcular el score normalizado entre -1 y 1
                        if data['Average Difference'] > 0:
                            data['Score'] = min(data['Average Difference'] / data['Average Views'], 1)
                        else:
                            data['Score'] = max(data['Average Difference'] / data['Average Views'], -1)
                    else:
                        data['Average Difference'] = 0
                        data['Score'] = 0

                    # Añadir información de medios si existe
                    if message.media:
                        media_details = extract_media_details(message.media)
                        data.update(media_details)
                    else:
                        # Si no hay medios, establecer valores por defecto
                        data['Media Type'] = ''
                        data['Media Size'] = None
                        data['Media Caption'] = None
                    
                    # Inicializar Label como vacío
                    data['Label'] = ''

                    all_data.append(data)
                    mensajes_nuevos += 1

                print(f"✓ Canal '{channel}': {mensajes_existentes} mensajes existentes, {mensajes_nuevos} nuevos mensajes añadidos")

            except ChannelInvalidError:
                print(f"✗ Canal '{channel}' inválido o no accesible. Continuando con el siguiente.")
            except Exception as e:
                print(f"Error al procesar {channel}: {str(e)}")
                continue

        if all_data:
            print("13. Guardando datos...")
            # Convert the new data to a DataFrame
            new_data_df = pd.DataFrame(all_data)

            # Asegurarse de que las columnas coincidan entre los DataFrames
            if not existing_messages.empty:
                # Añadir columnas faltantes a existing_messages
                for col in new_data_df.columns:
                    if col not in existing_messages.columns:
                        existing_messages[col] = None
                
                # Añadir columnas faltantes a new_data_df
                for col in existing_messages.columns:
                    if col not in new_data_df.columns:
                        new_data_df[col] = None

            # Set the 'Message ID' and 'Username' columns as the index for both DataFrames
            if 'Message ID' in existing_messages.columns and 'Username' in existing_messages.columns:
                existing_messages.set_index(['Message ID', 'Username'], inplace=True)

            if 'Message ID' in new_data_df.columns and 'Username' in new_data_df.columns:
                new_data_df.set_index(['Message ID', 'Username'], inplace=True)

            # Update the existing data with the new data
            existing_messages.update(new_data_df)

            # Reset the index of the existing data
            existing_messages.reset_index(inplace=True)
            new_data_df.reset_index(inplace=True)

            # Concatenar los DataFrames asegurando que las columnas coincidan
            df = pd.concat([existing_messages, new_data_df], ignore_index=True)
            df.drop_duplicates(subset=['Message ID', 'Username'], inplace=True, keep='first')
                
            # Convertir columnas específicas a entero de manera segura
            columnas_a_convertir = ['Message ID', 'Views', 'Members Count', 'Forwards', 'Replies']
            for columna in columnas_a_convertir:
                if columna in df.columns and df[columna].dtype not in ['datetime64[ns]', 'timedelta64[ns]']:
                    df[columna] = pd.to_numeric(df[columna], errors='coerce').fillna(0).astype(int)

            # Asegurar que las columnas de texto no sean nulas
            columnas_texto = ['Message Text', 'URL', 'Embed', 'Label', 'Media Type', 'Media Caption']
            for columna in columnas_texto:
                if columna in df.columns:
                    df[columna] = df[columna].fillna('')

            # Asegurar que el score esté entre -1 y 1
            if 'Score' in df.columns:
                df['Score'] = df['Score'].clip(-1, 1)

            # Eliminar columnas vacías o no deseadas
            columnas_a_eliminar = []  # Ya no eliminamos ninguna columna
            for columna in columnas_a_eliminar:
                if columna in df.columns:
                    df = df.drop(columns=[columna])

            df.to_csv('telegram_messages.csv', index=False, encoding='utf-8')
            print("14. Datos guardados en telegram_messages.csv")

            # Convertir todas las columnas de fecha a datetime sin zona horaria
            for col in ['Date Sent', 'Creation Date', 'Edit Date']:
                if col in df.columns:
                    try:
                        # Primero convertir a datetime si no lo es
                        df[col] = pd.to_datetime(df[col])
                        # Luego eliminar la zona horaria
                        df[col] = df[col].dt.tz_localize(None)
                    except (AttributeError, TypeError):
                        # Si la columna no tiene zona horaria o ya está en el formato correcto
                        df[col] = pd.to_datetime(df[col])
            
            # Guardar en Excel
            with pd.ExcelWriter('telegram_data.xlsx', engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Messages', index=False)
            print("15. Datos guardados en telegram_data.xlsx")
        else:
            print("13. No hay datos para guardar")
        
        print("16. Cerrando conexión...")
        await client.disconnect()
        print("17. Script completado!")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    print("Iniciando ejecución...")
    asyncio.run(main())