# HeartGuard AI

HeartGuard AI is an innovative web application that uses artificial intelligence to predict potential heart attacks through ECG analysis. The system provides real-time predictions and medical chatbot assistance to help users understand their heart health better.

## Features

- 🫀 ECG Upload & Analysis
- 🤖 AI-powered Medical Chatbot
- 📊 Real-time Heart Attack Risk Prediction
- 📱 Responsive Web Interface
- 📝 Educational Blog Section
- ℹ️ Comprehensive Information About Heart Health

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **AI Model**: TensorFlow/Keras
- **Chat Model**: Ollama Integration
- **Data Processing**: Matplotlib, Joblib

## Installation

1. Clone the repository
```bash
git clone https://github.com/tripathiayushman/HeartGuard.git
cd HeartGuard
```

2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Pull misteral
```bash
ollama pull mistral
```

4. Activate Scripts
```bash
./venv/Scripts/activate 
```
Incase of already running Script
```bash
Set-ExecutionPolicy Unrestricted -Scope Process
```
5. Run the application
```bash
python app.py
```

## Project Structure

```
Heart_guard/
├── static/
│   ├── css/
│   │   └── style.css
│   └── image/
├── templates/
│   ├── index.html
│   ├── upload.html
│   ├── model.html
│   ├── about.html
│   ├── blog.html
│   └── ai-model.html
├── app.py
├── ecg_heart_attack_model.h5
├── scaler.joblib
└── chat_history.csv
```

## Usage

1. Access the web application at http://localhost:5000
2. Navigate to the Upload ECG section
3. Upload your ECG data for analysis
4. Get instant predictions and chat with the AI medical assistant
5. Browse educational content in the Blog section

## Contributing

Feel free to submit issues, fork the repository and create pull requests for any improvements.

## License

MIT License

## Authors

- [Ayushman Tripathi](https://github.com/tripathiayushman)
- [Swayam Kapoor](https://github.com/Super-cod)



## Disclaimer

This tool is meant for educational purposes only and should not replace professional medical advice. Always consult with healthcare professionals for medical decisions.

