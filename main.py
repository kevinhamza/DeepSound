from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import requests
import uuid
import base64
import subprocess
import tempfile
# from TTS.api import TTS
import io
import pyttsx3 # (comment for vercel)
import time
import re

app = Flask(__name__)
app.secret_key = "super-secret-for-login"


UPLOAD_FOLDER = "/tmp"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route('/uploads' ,methods = ["POST"])
def upload_audio():
    if 'audioFile' not in request.files:
        return jsonify({"error" : "No File uploaded"}), 400
    file = request.files["audioFile"]
    if file.filename == "":
        return jsonify({"error" : "Empty File"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error" : "File Type not allowed"}), 400
    unique_name = f"{uuid.uuid4()}.webm"
    file_path = os.path.join(UPLOAD_FOLDER, unique_name)
    file.save(file_path)
    transcription = Speech_to_Text(file_path)
    if isinstance(transcription, str) and transcription.startswith("Error"):
        return jsonify({"error" : f"{transcription}"}), 500
    text = transcription.get("text", "")
    clean_text = clean_text_for_tts(text)
    print(clean_text)
    if not text.strip():
        return jsonify({"error": "Empty transcription"}), 400
    ai_reply = ai_response(clean_text)
    if os.path.exists(file_path):
        os.remove(file_path)
    if isinstance(ai_reply, str) and ai_reply.startswith("Error"):
        return jsonify({"error": ai_reply}), 500
    message = ai_reply.get("content", "")
    if "**Final Answer:**" in message:
        message_to_spe = message.split("**Final Answer:**")[-1].strip().strip('"')
    else:
        message_to_spe = message.strip()
    message_to_speak = clean_text_for_tts(message_to_spe)
    voice_audio = Text_to_Speech(message_to_speak)
    if isinstance(voice_audio, str) and voice_audio.startswith("Error"):
        return jsonify({"error" : voice_audio}) , 500
    audio_base64 = base64.b64encode(voice_audio).decode("utf-8")
    return jsonify({
        "transcription": clean_text,
        "ai_response": message_to_speak,
        "audio": audio_base64
        })


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'flac', 'wav', 'mp3', 'webm'}


def Speech_to_Text(file_path):
    ext = file_path.rsplit('.', 1)[1].lower()
    API_URL = "https://router.huggingface.co/hf-inference/models/openai/whisper-large-v3"
    headers = {
                "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}",
                "Content-Type": f"audio/{ext}"
            }
    if not allowed_file(file_path):
        return f"Error: File {file_path} is not allowed."
    with open(file_path, "rb") as f :
        data = f.read()
    response = requests.post(API_URL, headers = headers, data = data)
    print(f"Whisper API Status: {response.status_code}, Response: {response.text[:200]}")
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"


def ai_response(transcription):
    API_URL = "https://router.huggingface.co/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}",
        "Content-Type": "application/json"
        }
    data = {
        "messages" : [
            {"role": "system", "content": "You are a helpful and expert assistant for all tasks."},
            {"role": "user", "content": f"Transcription: {transcription}."}
        ],
        "model": "deepseek-ai/DeepSeek-R1:novita"
    }
    ai_response = requests.post(API_URL, headers = headers, json = data)
    if ai_response.status_code == 200:
        response =  ai_response.json()
        return response["choices"][0]["message"]
    else:
        return f"Error: {ai_response.status_code} - {ai_response.text}"


def clean_text_for_tts(text):
    text = re.sub(r"\*\*|\#|\`", "", text)
    text = re.sub(r"\d+\.", "", text)
    text = re.sub(r"\n+", " ", text)
    return text.strip()
# comment for vercel

# engine = pyttsx3.init()


# def Text_to_Speech(text_of_ai_response):
#     filename = os.path.abspath(f"response_{uuid.uuid4()}.wav")
#     engine.save_to_file(text_of_ai_response , filename)
#     engine.runAndWait()
#     time.sleep(0.5)
#     with open(filename, "rb") as f:
#         audio_bytes = f.read()
#     os.remove(filename)
#     return audio_bytes

tts = TTS(model_name="Thorsten-Voice/Tacotron2-DDC") 
def Text_to_Speech(text):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        tmp_path = tmp_file.name
    tts.tts_to_file(text=text, file_path=tmp_path)
    with open(tmp_path, "rb") as f:
        audio_bytes = f.read()
    os.remove(tmp_path)
    return audio_bytes

@app.route("/login", methods=["GET", "POST"])
def login(): 
    if request.method == "POST":
        username = request.form["username"].strip()
        if username:
            session["user"] = username
            return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
