# Deepsound - AI Voice Assistant

Deepsound is an intelligent voice assistant application that converts speech to text, processes it with AI, and responds with synthesized voice. Built with Flask, it leverages cutting-edge AI models from Hugging Face to deliver seamless voice interactions.

## Features

- 🎤 **Speech-to-Text**: Convert audio files to text using OpenAI's Whisper Large V3 model
- 🤖 **AI Response Generation**: Get intelligent responses using DeepSeek-R1 AI model
- 🔊 **Text-to-Speech**: Synthesize natural-sounding voice responses
- 🔐 **User Authentication**: Secure login system for user sessions
- 📁 **Audio Upload**: Support for multiple audio formats (FLAC, WAV, MP3, WEBM)
- 🎨 **Modern UI**: Beautiful glassmorphism design with animated gradients

## Tech Stack

- **Backend**: Flask (Python)
- **APIs**: Hugging Face Inference API
- **Models**:
  - Speech Recognition: `openai/whisper-large-v3`
  - Language Model: `deepseek-ai/DeepSeek-R1:novita`
- **Audio Processing**: pyttsx3 for text-to-speech
- **Frontend**: HTML5, CSS3 with modern styling

## Project Structure

```
Deepsound/
├── main.py              # Flask application and API endpoints
├── requirements.txt     # Requirement for this project
├── templates/
│   ├── index.html       # Main assistant interface
│   └── login.html       # User login page
├── Uploads/             # Temporary audio file storage
└── README.md            # Project documentation
```

## Prerequisites

- Python 3.8+
- Hugging Face API Key
- Required Python packages (see Installation section)

## Installation

1. **Clone or navigate to the project directory**:
```bash
cd Deepsound
```

2. **Create a virtual environment** (recommended):
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

3. **Login**:
Enter your credentials on the login page

4. **Interact with Deepsound**:
   - Click the microphone button to record audio
   - Deepsound will process your speech and respond with AI-generated audio
   - View transcriptions and responses in real-time

## API Endpoints

### POST `/uploads`
Upload audio file and get AI response

**Request**:
- Form data: `audioFile` (audio file in supported format)

**Response**:
```json
{
  "transcription": "user's speech transcribed",
  "ai_response": "AI's text response",
  "audio": "base64 encoded audio response"
}
```

### GET `/`
Main application interface (requires authentication)

### GET `/login`
User login page

## Supported Audio Formats

- FLAC
- WAV
- MP3
- WEBM

## Configuration

The application uses the following configuration:
- **Flask Secret Key**: `super-secret-for-login` (change this in production)
- **Upload Folder**: `Uploads/` directory for temporary file storage
- **API URLs**:
  - Whisper (Speech-to-Text): `https://router.huggingface.co/hf-inference/models/openai/whisper-large-v3`
  - DeepSeek (LLM): `https://router.huggingface.co/v1/chat/completions`

## Development Notes

- Audio files are temporarily stored in the `Uploads/` folder and automatically deleted after processing
- Files are renamed with UUID to avoid conflicts
- The application includes text cleaning for improved speech synthesis
- Session-based authentication prevents unauthorized access

## Future Enhancements

- User registration system
- Conversation history storage
- Support for multiple languages
- Custom voice profiles
- Advanced audio processing options

## Troubleshooting

**API Key Issues**: Ensure your Hugging Face API key is set correctly
```bash
echo $HUGGINGFACE_API_KEY
```

**File Upload Errors**: Check that uploaded files are in supported formats

**Empty Transcription**: Ensure audio quality is sufficient for speech recognition

## Author

Developed by Devin

---

**Note**: This is an interactive AI assistant. For best results, speak clearly and use supported audio formats.
