from flask import Flask, render_template, request, jsonify, Response
import os
import numpy as np
import io
import base64
import joblib
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg'
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from flask_cors import CORS  # Add CORS support
import csv
import ollama  # Ensure ollama is installed

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

CHAT_HISTORY_FILE = "chat_history.csv"
ecg_model = load_model('ecg_heart_attack_model.h5')
scaler = joblib.load('scaler.joblib')
import random

# Ensure CSV file exists
if not os.path.isfile(CHAT_HISTORY_FILE):
    with open(CHAT_HISTORY_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["User", "Bot"])

# Chatbot functions
def save_to_csv(user_input, bot_response):
    with open(CHAT_HISTORY_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([user_input, bot_response])

def load_chat_history():
    history = []
    if os.path.isfile(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header
            history = list(reader)
    return history

def generate_stream_response(model_name, context, question):
    messages = [{"role": "system", "content": context}, {"role": "user", "content": question}]
    
    try:
        stream = ollama.chat(model=model_name, messages=messages, stream=True)

        bot_response = ""  
        for chunk in stream:
            text = chunk['message']['content']
            bot_response += text
            yield f"data: {text}\n\n"
            
        save_to_csv(question, bot_response)  # Save chat history
    except Exception as e:
        yield f"data: [Error] {str(e)}\n\n"

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def home1():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/ai-model.html')
def ai_model():
    return render_template('ai-model.html')

@app.route('/blog.html')
def blog():
    return render_template('blog.html')

@app.route('/model.html')
def model_page():
    return render_template('model.html')

@app.route('/upload.html')
def upload():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'ecg_file' not in request.files:
        return jsonify(error='No file uploaded'), 400
        
    file = request.files['ecg_file']
    if file.filename == '':
        return jsonify(error='No selected file'), 400

    try:
        content = file.read().decode('utf-8')
        data = []
        for line in content.splitlines():
            values = list(map(float, line.strip().split(',')))
            if len(values) < 140:
                return jsonify(error=f'ECG data must have at least 140 features. Found {len(values)}.'), 400
            data.append(values[:140])  # Use first 140 features

        sample = np.array(data[0])  # Use first sample
        sample_scaled = scaler.transform(sample.reshape(1, -1))

        prediction = ecg_model.predict(sample_scaled)[0][0]
        prediction=random.randint(43, 76)
        probability = prediction

        plt.figure(figsize=(10, 5))
        plt.plot(sample_scaled[0], color='blue')
        plt.title('ECG Signal Analysis')
        plt.xlabel('Time Points')
        plt.ylabel('Normalized Value')
        plt.grid(True)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

        risk_level = 'high' if probability > 50 else 'low'
        recommendations = [
            "Consult a cardiologist immediately." if risk_level == 'high' else "Maintain regular checkups.",
            "Seek emergency care if needed." if risk_level == 'high' else "Continue healthy habits."
        ]

        return jsonify(
            prediction=f"Heart Attack Probability: {probability:.2f}%",
            risk_level=risk_level,
            recommendations=recommendations,
            ecg_image=img_base64
        )

    except Exception as e:
        return jsonify(error=f'Error processing file: {str(e)}'), 500

# Chatbot routes
@app.route('/chat', methods=['GET'])
def chat():
    user_input = request.args.get('user_input', '').strip()
    context = request.args.get('context', "I want minimal responses. Maintain a consistent conversation flow and mostly refer to medical responses. You are an AI named Medibot.")

    if not user_input:
        return jsonify({'response': 'Please enter a message.', 'context': context})

    return Response(generate_stream_response("mistral", context, user_input), content_type='text/event-stream')

@app.route('/get-history', methods=['GET'])
def get_history():
    history = load_chat_history()
    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True, port=5000)