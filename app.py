from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

MESSAGES_LIMIT = 48

app = Flask(__name__)

def load_data():
    """Carga los datos del archivo CSV y maneja posibles errores."""
    try:
        if not os.path.exists('telegram_messages.csv'):
            return pd.DataFrame()
        return pd.read_csv('telegram_messages.csv')
    except Exception as e:
        print(f"Error al cargar el archivo CSV: {e}")
        return pd.DataFrame()

@app.route('/')
def index():
    """Renderiza la página principal con los mensajes ordenados por puntuación."""
    df = load_data()
    if df.empty:
        return render_template('index.html', messages=[])
    sorted_df = df.sort_values(by='Score', ascending=False)
    displayed_df = sorted_df.head(MESSAGES_LIMIT)
    messages = displayed_df[['Embed', 'Score', 'Message ID', 'URL', 'Label']].to_dict(orient='records')
    return render_template('index.html', messages=messages)

@app.route('/load_more/<int:offset>', methods=['GET'])
def load_more(offset=0):
    """Carga más mensajes a partir de un offset dado."""
    df = load_data()
    sorted_df = df.sort_values(by='Score', ascending=False)
    displayed_df = sorted_df.iloc[offset:offset+24]
    messages = displayed_df[['Embed', 'Score', 'Message ID']].to_dict(orient='records')
    return render_template('index.html', messages=messages)

@app.route('/label', methods=['POST'])
def label_message():
    """Etiqueta un mensaje con un valor específico."""
    try:
        data = request.json
        if not data or 'message_id' not in data or 'label' not in data:
            return jsonify(success=False, error="Datos incompletos"), 400

        message_id = int(data['message_id'])
        label = int(data['label'])
        
        df = load_data()
        if df.empty:
            return jsonify(success=False, error="No hay datos disponibles"), 404

        # Actualiza el DataFrame
        df.loc[df['Message ID'] == message_id, 'Label'] = label
        
        # Guarda el DataFrame actualizado
        df.to_csv('telegram_messages.csv', index=False, encoding='utf-8')

        return jsonify(success=True)
    except ValueError as e:
        return jsonify(success=False, error=f"Error en los datos: {str(e)}"), 400
    except Exception as e:
        return jsonify(success=False, error=f"Error inesperado: {str(e)}"), 500

@app.route('/export_relevants', methods=['GET'])
def export_relevants():
    """Exporta los mensajes etiquetados como relevantes a un nuevo archivo CSV."""
    try:
        df = load_data()
        if df.empty:
            return jsonify(success=False, error="No hay datos disponibles"), 404

        # Filtra los mensajes etiquetados como relevantes
        relevant_df = df[df['Label'] == 1]
        if relevant_df.empty:
            return jsonify(success=False, error="No hay mensajes relevantes"), 404

        # Guarda en un nuevo CSV
        relevant_df.to_csv('telegram_messages_relevant.csv', index=False, encoding='utf-8')
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
