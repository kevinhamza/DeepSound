# Deepsound - AI Voice Assistant

Deepsound is an simple voice assistant application that converts speech to text, processes it with AI, and responds with synthesized voice. Built with Flask.

## Features

- **Speech-to-Text**: Convert audio files to text using OpenAI's Whisper Large V3 model
- **AI Response Generation**: Get intelligent responses using DeepSeek-R1 AI model
- **Text-to-Speech**: Synthesize natural-sounding voice responses
- **User Authentication**: Simple Userame based login system for user sessions
- **Audio Upload**: Support for multiple audio formats (FLAC, WAV, MP3, WEBM)

## Prerequisites

- Python 3.8+
- Hugging Face API Key
- Required Python packages

## Installation

1. **Clone or navigate to the project directory**:
```bash
cd Deepsound
```

2. **Create a virtual environment** :
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
Add a API-key to `.env` file and export your Hugging Face API key:
```bash
export HUGGINGFACE_API_KEY="your_api_key_here"
```

## Usage

1. **Start the application**:
```bash
python main.py
```

2. **Access the web interface**:
Open your browser and navigate to `http://localhost:5000`


## Supported Audio Formets

- FLAC
- MP3
- WEBM
- and some ohers

## Author

Developed by Devin

---
