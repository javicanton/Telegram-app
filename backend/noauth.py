from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import json
import boto3
from botocore.exceptions import ClientError

# Configuración S3 para datos reales
S3_BUCKET_REAL = 'monitoria-data'
S3_KEY_JSON = 'telegram_messages.json'  # Archivo JSON real de S3

# Inicializar cliente S3
s3_client = boto3.client('s3',
    region_name=os.environ.get('AWS_REGION', 'eu-north-1')
)

def load_real_data():
    """Carga los datos reales del archivo JSON desde S3."""
    try:
        # Intentar leer el archivo JSON desde S3
        response = s3_client.get_object(Bucket=S3_BUCKET_REAL, Key=S3_KEY_JSON)
        data = json.loads(response['Body'].read().decode('utf-8'))
        
        # Convertir los mensajes a DataFrame
        df = pd.DataFrame(data['messages'])
        
        # Verificar y limpiar la columna Title (usada como Channel)
        if 'Title' in df.columns:
            df['Title'] = df['Title'].fillna('Desconocido')
            df['Title'] = df['Title'].replace('', 'Desconocido')
        
        # Convertir columnas de fecha si existen
        date_columns = ['Date', 'Date Sent', 'Creation Date', 'Edit Date']
        for col in date_columns:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col]).dt.tz_localize(None)
                except Exception as e:
                    print(f"Error al convertir la columna '{col}': {e}")
                    if col in df.columns:
                        del df[col]
        
        return df
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            print(f"Advertencia: El archivo {S3_KEY_JSON} no existe en S3.")
            return pd.DataFrame()
        else:
            print(f"Error de S3: {e}")
            return pd.DataFrame()
    except json.JSONDecodeError as e:
        print(f"Error al decodificar el archivo JSON: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error crítico al cargar datos reales: {e}")
        return pd.DataFrame()

def register_noauth_routes(app):
    """Registra las rutas sin autenticación en la aplicación Flask."""
    
    @app.route('/noauth/')
    def noauth_index():
        """Redirige a la página principal del frontend."""
        return jsonify({"message": "Use the frontend at / for the web interface"})

    @app.route('/noauth/filter_messages', methods=['POST'])
    def noauth_filter_messages():
        """Filtra los mensajes sin autenticación usando datos reales."""
        try:
            filters = request.json
            if not filters:
                return jsonify(success=False, error="No se proporcionaron filtros"), 400

            df = load_real_data()
            if df.empty:
                return jsonify(success=True, messages=[], total_messages=0)

            # --- Aplicar filtros ---
            filtered_df = df.copy()

            # Filtro de Fecha (Rango)
            date_start_str = filters.get('dateStart')
            date_end_str = filters.get('dateEnd')
            if 'Date Sent' in filtered_df.columns:
                try:
                    filtered_df['Date Sent'] = pd.to_datetime(filtered_df['Date Sent']).dt.tz_localize(None)
                    
                    if date_start_str:
                        date_start = pd.to_datetime(date_start_str).normalize()
                        filtered_df = filtered_df[filtered_df['Date Sent'].dt.normalize() >= date_start]
                    
                    if date_end_str:
                        date_end = pd.to_datetime(date_end_str).normalize() + pd.Timedelta(days=1)
                        filtered_df = filtered_df[filtered_df['Date Sent'].dt.normalize() < date_end]
                    
                except Exception as e:
                    print(f"Error en filtro de fechas: {str(e)}")
                    return jsonify(success=False, error=f"Error en filtro de fechas: {str(e)}"), 400

            # Filtro de Canal (usando Title)
            channel = filters.get('channel')
            if channel and 'Title' in filtered_df.columns:
                try:
                    filtered_df = filtered_df[filtered_df['Title'] == channel]
                    print(f"Filtrado por canal: {channel}")
                except Exception as e:
                    print(f"Error en filtro de canal: {str(e)}")
                    return jsonify(success=False, error=f"Error en filtro de canal: {str(e)}"), 400

            # Filtro de Puntuación (Score) Mínima
            score_min_str = filters.get('scoreMin')
            if score_min_str and 'Score' in filtered_df.columns:
                try:
                    score_min = float(score_min_str)
                    filtered_df['Score'] = pd.to_numeric(filtered_df['Score'], errors='coerce')
                    filtered_df = filtered_df[filtered_df['Score'] >= score_min]
                    print(f"Filtrado por score mínimo: {score_min}")
                except Exception as e:
                    print(f"Error en filtro de score mínimo: {str(e)}")
                    return jsonify(success=False, error=f"Error en filtro de score mínimo: {str(e)}"), 400

            # Filtro de Puntuación (Score) Máxima
            score_max_str = filters.get('scoreMax')
            if score_max_str and 'Score' in filtered_df.columns:
                try:
                    score_max = float(score_max_str)
                    filtered_df['Score'] = pd.to_numeric(filtered_df['Score'], errors='coerce')
                    filtered_df = filtered_df[filtered_df['Score'] <= score_max]
                    print(f"Filtrado por score máximo: {score_max}")
                except Exception as e:
                    print(f"Error en filtro de score máximo: {str(e)}")
                    return jsonify(success=False, error=f"Error en filtro de score máximo: {str(e)}"), 400

            # Filtro de Tipo de Media
            media_type = filters.get('mediaType')
            if media_type and 'Media Type' in filtered_df.columns:
                try:
                    filtered_df['Media Type'] = filtered_df['Media Type'].astype(str).str.lower()
                    filtered_df = filtered_df[filtered_df['Media Type'] == str(media_type).lower()]
                    print(f"Filtrado por tipo de media: {media_type}")
                except Exception as e:
                    print(f"Error en filtro de tipo de media: {str(e)}")
                    return jsonify(success=False, error=f"Error en filtro de tipo de media: {str(e)}"), 400

            # Ordenar y preparar resultados
            sort_by = filters.get('sortBy', 'score')
            try:
                if sort_by == 'views' and 'Views' in filtered_df.columns:
                    filtered_df['Views'] = pd.to_numeric(filtered_df['Views'], errors='coerce')
                    sorted_df = filtered_df.sort_values(by='Views', ascending=False)
                elif 'Score' in filtered_df.columns:
                    filtered_df['Score'] = pd.to_numeric(filtered_df['Score'], errors='coerce')
                    sorted_df = filtered_df.sort_values(by='Score', ascending=False)
                else:
                    sorted_df = filtered_df
                print(f"Ordenado por: {sort_by}")
            except Exception as e:
                print(f"Error al ordenar los datos: {e}")
                sorted_df = filtered_df

            # Paginación
            try:
                page = filters.get('page')
                per_page = filters.get('per_page')
                
                try:
                    page = int(page) if page is not None else 1
                except (ValueError, TypeError):
                    page = 1
                    
                try:
                    per_page = int(per_page) if per_page is not None else 24
                except (ValueError, TypeError):
                    per_page = 24
                    
                page = max(1, page)
                per_page = max(1, min(per_page, 100))
                
                start_idx = (page - 1) * per_page
                end_idx = start_idx + per_page

                paginated_df = sorted_df.iloc[start_idx:end_idx]
                print(f"Paginación: página {page}, {per_page} mensajes por página")
            except Exception as e:
                print(f"Error en paginación: {str(e)}")
                return jsonify(success=False, error=f"Error en paginación: {str(e)}"), 400

            # Seleccionar columnas y convertir a dict
            try:
                required_columns = ['Embed', 'Score', 'Message ID', 'URL', 'Label']
                messages = []
                for _, row in paginated_df.iterrows():
                    msg = {}
                    for col in required_columns:
                        if col in row:
                            msg[col] = row[col] if pd.notna(row[col]) else None
                        else:
                            msg[col] = None
                    messages.append(msg)
                print(f"Total de mensajes filtrados: {len(messages)}")
            except Exception as e:
                print(f"Error al preparar mensajes: {str(e)}")
                return jsonify(success=False, error=f"Error al preparar mensajes: {str(e)}"), 400

            return jsonify(success=True, messages=messages, total_messages=len(sorted_df))

        except Exception as e:
            print(f"Error crítico en /noauth/filter_messages: {e}")
            return jsonify(success=False, error=f"Error al procesar los filtros: {str(e)}"), 500

    @app.route('/noauth/render_partial', methods=['POST'])
    def noauth_render_partial():
        """Renderiza el fragmento HTML de los mensajes sin autenticación."""
        try:
            data = request.json
            if data is None:
                messages = []
            else:
                messages = data.get('messages', [])
                
            # Asegúrate de que Score se maneje correctamente
            for msg in messages:
                if isinstance(msg.get('Score'), str):
                    pass  # Ya viene como 'N/A' desde filter_messages
                elif isinstance(msg.get('Score'), (int, float)):
                    msg['Score'] = round(msg['Score'], 2)
                else:
                    msg['Score'] = 'N/A'

            return render_template('message_cards_partial.html', messages=messages)
        except Exception as e:
            print(f"Error en /noauth/render_partial: {e}")
            return "<p>Error rendering messages.</p>", 500

    @app.route('/noauth/load_more/<int:offset>', methods=['GET'])
    def noauth_load_more(offset=0):
        """Carga más mensajes sin autenticación."""
        try:
            # Obtener los filtros de la URL
            filters = {
                'dateStart': request.args.get('dateStart'),
                'dateEnd': request.args.get('dateEnd'),
                'channel': request.args.get('channel'),
                'scoreMin': request.args.get('scoreMin'),
                'scoreMax': request.args.get('scoreMax'),
                'mediaType': request.args.get('mediaType'),
                'sortBy': request.args.get('sortBy', 'score')
            }

            df = load_real_data()
            if df.empty:
                return ('', 204)  # No Content

            # Aplicar los mismos filtros que en /filter_messages
            filtered_df = df.copy()

            # Filtro de Fecha (Rango)
            if 'Date Sent' in filtered_df.columns:
                try:
                    filtered_df['Date Sent'] = pd.to_datetime(filtered_df['Date Sent']).dt.tz_localize(None)
                    
                    if filters['dateStart']:
                        date_start = pd.to_datetime(filters['dateStart']).normalize()
                        filtered_df = filtered_df[filtered_df['Date Sent'].dt.normalize() >= date_start]
                    
                    if filters['dateEnd']:
                        date_end = pd.to_datetime(filters['dateEnd']).normalize() + pd.Timedelta(days=1)
                        filtered_df = filtered_df[filtered_df['Date Sent'].dt.normalize() < date_end]
                except Exception as e:
                    print(f"Error en filtro de fechas: {str(e)}")
                    return ('', 204)

            # Filtro de Canal
            if filters['channel'] and 'Title' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['Title'] == filters['channel']]

            # Filtro de Puntuación (Score) Mínima
            if filters['scoreMin'] and 'Score' in filtered_df.columns:
                try:
                    score_min = float(filters['scoreMin'])
                    filtered_df['Score'] = pd.to_numeric(filtered_df['Score'], errors='coerce')
                    filtered_df = filtered_df[filtered_df['Score'] >= score_min]
                except:
                    pass

            # Filtro de Puntuación (Score) Máxima
            if filters['scoreMax'] and 'Score' in filtered_df.columns:
                try:
                    score_max = float(filters['scoreMax'])
                    filtered_df['Score'] = pd.to_numeric(filtered_df['Score'], errors='coerce')
                    filtered_df = filtered_df[filtered_df['Score'] <= score_max]
                except:
                    pass

            # Filtro de Tipo de Media
            if filters['mediaType'] and 'Media Type' in filtered_df.columns:
                try:
                    filtered_df['Media Type'] = filtered_df['Media Type'].astype(str).str.lower()
                    filtered_df = filtered_df[filtered_df['Media Type'] == str(filters['mediaType']).lower()]
                except:
                    pass

            # Ordenar
            if filters['sortBy'] == 'views' and 'Views' in filtered_df.columns:
                filtered_df['Views'] = pd.to_numeric(filtered_df['Views'], errors='coerce')
                sorted_df = filtered_df.sort_values(by='Views', ascending=False)
            elif 'Score' in filtered_df.columns:
                filtered_df['Score'] = pd.to_numeric(filtered_df['Score'], errors='coerce')
                sorted_df = filtered_df.sort_values(by='Score', ascending=False)
            else:
                sorted_df = filtered_df

            # Asegúrate de que el índice no esté fuera de los límites
            if offset >= len(sorted_df):
                return ('', 204)  # No hay más mensajes que cargar

            displayed_df = sorted_df.iloc[offset:offset+24]

            # Si displayed_df está vacío después de iloc
            if displayed_df.empty:
                return ('', 204)

            # Preparar mensajes
            messages = []
            for _, row in displayed_df.iterrows():
                msg = {}
                msg['Embed'] = row.get('Embed', '')
                score = row.get('Score')
                msg['Score'] = round(score, 2) if pd.notna(score) and isinstance(score, (int, float)) else 'N/A'
                msg['Message ID'] = row.get('Message ID', '')
                msg['URL'] = row.get('URL', '')
                msg['Label'] = row.get('Label', None)
                messages.append(msg)

            return render_template('message_cards_partial.html', messages=messages)

        except Exception as e:
            print(f"Error en noauth_load_more: {str(e)}")
            return ('', 204)

    @app.route('/noauth/api/messages', methods=['GET'])
    def noauth_get_messages():
        """Endpoint para obtener los mensajes sin autenticación."""
        try:
            df = load_real_data()
            if df.empty:
                return jsonify(success=True, messages=[])

            print(f"Columnas disponibles en JSON: {list(df.columns)}")
            
            # Seleccionar las columnas necesarias para el frontend
            required_columns = ['Message ID', 'Message Text', 'Title', 'Views', 'Average Views', 'Label', 'Score', 'URL', 'Embed']
            messages = []
            
            for _, row in df.iterrows():
                msg = {}
                for col in required_columns:
                    if col in row:
                        msg[col] = row[col] if pd.notna(row[col]) else None
                    else:
                        msg[col] = None
                messages.append(msg)

            print(f"Total mensajes procesados: {len(messages)}")
            return jsonify(success=True, messages=messages)

        except Exception as e:
            print(f"Error en /noauth/api/messages: {e}")
            return jsonify(success=False, error=str(e)), 500

    @app.route('/noauth/api/channels', methods=['GET'])
    def noauth_get_channels():
        """Endpoint para obtener la lista de canales sin autenticación."""
        try:
            df = load_real_data()
            if df.empty:
                return jsonify([])

            if 'Title' in df.columns:
                channels = sorted(df['Title'].unique().tolist())
                return jsonify(channels)
            else:
                return jsonify([])

        except Exception as e:
            print(f"Error en /noauth/api/channels: {e}")
            return jsonify([]), 500
