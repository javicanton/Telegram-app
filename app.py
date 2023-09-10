from flask import Flask, render_template, request, jsonify
import pandas as pd

MESSAGES_LIMIT = 48
global df
df = pd.read_csv('telegram_messages.csv')

app = Flask(__name__)

@app.route('/')
def index():
    global df
    if df.empty:
        return render_template('index.html', messages=[])
    sorted_df = df.sort_values(by='Score', ascending=False)
    displayed_df = sorted_df.head(48)
    messages = displayed_df[['Embed', 'Score', 'Message ID', 'URL', 'Label']].to_dict(orient='records')
    return render_template('index.html', messages=messages)

@app.route('/load_more/<int:offset>', methods=['GET'])
def load_more(offset=0):
    global df
    sorted_df = df.sort_values(by='Score', ascending=False)
    displayed_df = sorted_df.iloc[offset:offset+24]
    messages = displayed_df[['Embed', 'Score', 'Message ID']].to_dict(orient='records')
    return render_template('index.html', messages=messages)

@app.route('/label', methods=['POST'])
def label_message():
    global df  # Declare df as global
    data = request.json
    print(f"Received data: {data}")  # Debugging line

    try:
        message_id = int(request.json['message_id'])
        label = int(request.json['label'])
        
    except ValueError as e:
        print(f"Error: {e}")
        return jsonify(success=False, error=str(e))

    # Update the DataFrame
    df.loc[df['Message ID'] == message_id, 'Label'] = label
    print(df[df['Message ID'] == message_id])
    
    # Save the updated DataFrame back to the CSV file
    df.to_csv('telegram_messages.csv', index=False, encoding='utf-8')

    return jsonify(success=True)

@app.route('/export_relevants', methods=['GET'])
def export_relevants():
    global df
    try:
        # Filter the messages labeled as relevant
        relevant_df = df[df['Label'] == 1]
        # Save to a new CSV
        relevant_df.to_csv('telegram_messages_relevant.csv', index=False, encoding='utf-8')
        return jsonify(success=True)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify(success=False, error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
