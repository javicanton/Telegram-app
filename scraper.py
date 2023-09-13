## Telegram Scraper
# Import libraries
import asyncio
import csv
import os
from telethon import TelegramClient
from telethon.errors import ChannelInvalidError, ChatAdminRequiredError
from datetime import datetime, timedelta, timezone
import pandas as pd

# Set the working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Prompt the user for the number of days:
try:
    days_to_scrape = int(input("Enter the number of days to scrape (leave blank to default value, 7): "))
except ValueError:
    print("Invalid input. Using default of 7 days.")
    days_to_scrape = 7

# Prompt the user for the message limit
try:
    MAX_MESSAGES_PER_CHANNEL = int(input("Enter the maximum number of messages to scrape for each channel (leave blank to default value, 500): "))
except ValueError:
    print("Invalid input. Using default of 500 messages.")
    MAX_MESSAGES_PER_CHANNEL = 500

# Calculate the time for 24 hours ago with timezone information
time_days_ago = datetime.now(timezone.utc) - timedelta(days=days_to_scrape)

# Loading credentials from credentials.txt
def load_credentials(filename):
    credentials = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            credentials[key] = value
    return credentials
creds = load_credentials('credentials.txt')
API_ID = creds['API_ID']
API_HASH = creds['API_HASH']

# Initialize the client
client = TelegramClient('anon', API_ID, API_HASH)

# Load channels from the CSV file
def load_channels_from_csv(filename):
    channels = []
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Check if row is not empty
                channels.append(row[0])
    return channels

CHANNELS = load_channels_from_csv('telegram_channels.csv')

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
        'Message Text': message.text,
        'Date Sent': message.date,
        'Views': message.views,
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
    return {
        'Media Type': type(media).__name__,
        'Media Size': getattr(media, 'size', None),
        'Media Caption': getattr(media, 'caption', None)
    }

async def extract_participants(client, channel):
    try:
        participants = await client.get_participants(channel)
        return {p.id: p.participant for p in participants}
    except ChatAdminRequiredError:
        print(f"Admin privileges required for channel '{channel}'. Skipping participant extraction.")
        return {}

def load_existing_data(filename):
    try:
        return pd.read_csv(filename)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame()

existing_messages = load_existing_data('telegram_messages.csv')
existing_participants = load_existing_data('telegram_participants.csv')

def load_existing_message_ids(filename):
    try:
        existing_data = pd.read_csv(filename)
        # Create a set of tuples (Username, Message ID) for fast lookup
        existing_ids = set(zip(existing_data['Username'], existing_data['Message ID']))
        return existing_ids
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return set()

EXISTING_MESSAGE_IDS = load_existing_message_ids('telegram_messages.csv')

async def main():
    all_data = []
    participants_list = []

    for channel in CHANNELS:
        try:
            channel_details = await client.get_entity(channel)
            messages = await client.get_messages(channel, limit=MAX_MESSAGES_PER_CHANNEL)

            # Group messages by their date
            grouped_messages = {}
            for message in messages:
                date_str = message.date.strftime('%Y-%m-%d')
                if date_str not in grouped_messages:
                    grouped_messages[date_str] = []
                grouped_messages[date_str].append(message)

            # Calculate daily average views
            daily_average_views = {}
            for date_str, daily_messages in grouped_messages.items():
                views_list = [message.views for message in daily_messages if message.views is not None]
                daily_average_views[date_str] = sum(views_list) / len(views_list) if views_list else 0

            for message in messages:
                data = {}
                data.update(extract_channel_details(channel_details))
                data.update(extract_message_details(message))
                # If this message ID for the current channel already exists, skip it
                if (channel_details.username, message.id) in EXISTING_MESSAGE_IDS:
                    continue
    
                # Update the URL and Embed columns using the channel's username
                channel_username = data['Username']
                data['URL'] = f"https://t.me/s/{channel_username}/{message.id}"
                data['Embed'] = f'<script async src="https://telegram.org/js/telegram-widget.js?22" data-telegram-post="{channel_username}/{message.id}" data-width="100%"></script>'
                
                date_str = message.date.strftime('%Y-%m-%d')
                data['Average Views'] = daily_average_views.get(date_str, 0)
                data['Average Difference'] = message.views - data['Average Views'] if message.views is not None else None
                if data['Average Views'] == 0:
                    data['Score'] = 0
                else:
                    data['Score'] = message.views / data['Average Views'] if message.views is not None else None

                    # Convert Score values between 0 and 1 to negative
                    if data['Score'] is not None and 0 < data['Score'] < 1:
                        data['Score'] *= -1
                
                if message.media:
                    data.update(extract_media_details(message.media))

                all_data.append(data)                     
                
                last_date = messages[-1].date.replace(tzinfo=timezone.utc)
            
            # Extract participants (might be limited for large channels)
            participants_data = await extract_participants(client, channel)
            for user_id, role in participants_data.items():
                participants_list.append({
                    'Channel': channel,
                    'User ID': user_id,
                    'Role': role
                })

        except ChannelInvalidError:
            print(f"Channel '{channel}' is invalid or not accessible. Skipping to the next channel.")

    # Convert the new data to a DataFrame
    new_data_df = pd.DataFrame(all_data)

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

    df = pd.concat([existing_messages, new_data_df], ignore_index=True)
    df.drop_duplicates(subset=['Message ID', 'Username'], inplace=True, keep='first')
        
    if 'Label' not in df.columns:
        df['Label'] = ''
    df['Label'].fillna('', inplace=True)  
    
    participants_df = pd.concat([existing_participants, pd.DataFrame(participants_list)], ignore_index=True)
    participants_df.drop_duplicates(subset=['User ID', 'Channel'], inplace=True, keep='last')
    
    # Check if the CSV file exists
    file_exists = os.path.isfile('telegram_messages.csv')

    # Convert specific columns and save to CSV
    # Convertir columnas específicas a entero
    columnas_a_convertir = ['Message ID', 'Sender ID', 'Reply To', 'Forwarded From', 'Views', 'Members Count']
    for columna in columnas_a_convertir:
        if columna in df.columns and df[columna].dtype not in ['datetime64[ns]', 'timedelta64[ns]']:
            df[columna] = df[columna].fillna(0).astype(int)

    df.to_csv('telegram_messages.csv', index=False, encoding='utf-8')
    participants_df.to_csv('telegram_participants.csv', index=False, encoding='utf-8')

    # Do the same for participants CSV
    file_exists_participants = os.path.isfile('telegram_participants.csv')
    if file_exists_participants:
        participants_df.to_csv('telegram_participants.csv', index=False, encoding='utf-8', mode='a', header=False)
    else:
        participants_df.to_csv('telegram_participants.csv', index=False, encoding='utf-8')

    # Date conversion and save to Excel
    datetime_columns = df.select_dtypes(include=['datetime64[ns]']).columns
    # Date conversion and save to Excel
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].apply(lambda x: x.tz_localize(None) if isinstance(x, pd.Timestamp) and x.tzinfo is not None else x)
        
    with pd.ExcelWriter('telegram_data.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Messages', index=False)
        participants_df.to_excel(writer, sheet_name='Participants', index=False)

# Ensure the client is started before running the main coroutine
with client:
    client.loop.run_until_complete(main())