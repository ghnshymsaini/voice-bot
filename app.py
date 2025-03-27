from flask import Flask, render_template, request, jsonify
import subprocess
import edge_tts
import asyncio
import speech_recognition as sr

app = Flask(__name__)


# Function to process voice input
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"✅ You said: {text}")
        return text
    except sr.UnknownValueError:
        print("⚠️ Could not understand audio")
        return None
    except sr.RequestError:
        print("⚠️ Could not request results")
        return None


# Function to chat with Mistral-7B via Ollama
def chat_with_mistral(user_input):
    command = f'ollama run mistral "{user_input}"'
    response = subprocess.run(command, shell=True, capture_output=True, text=True)
    return response.stdout.strip()


# Function to convert text to speech
async def text_to_speech(text):
    tts = edge_tts.Communicate(text, "en-US-JennyNeural")
    await tts.save("static/response.mp3")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/voice", methods=["POST"])
def voice_interaction():
    user_text = recognize_speech()
    if not user_text:
        return jsonify({"error": "Could not understand speech"}), 400

    ai_response = chat_with_mistral(user_text)
    asyncio.run(text_to_speech(ai_response))

    return jsonify({"response": ai_response, "audio": "static/response.mp3"})


if __name__ == "__main__":
    app.run(debug=True)
