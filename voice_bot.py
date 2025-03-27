import sounddevice as sd
import numpy as np
import speech_recognition as sr
import subprocess
import edge_tts
import asyncio


# Function to record audio from microphone and convert to text
def record_audio():
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


# Function to send text to Mistral model via Ollama and get response
def chat_with_mistral(user_input):
    command = f'ollama run mistral "{user_input}"'
    response = subprocess.run(command, shell=True, capture_output=True, text=True)
    return response.stdout.strip()


# Function to convert text to speech using Edge-TTS
async def text_to_speech(text):
    tts = edge_tts.Communicate(text, "en-US-JennyNeural")
    await tts.save("response.mp3")
    subprocess.run(["start", "response.mp3"], shell=True)


# Main loop to continuously listen, process, and respond
if __name__ == "__main__":
    print("🤖 Voice Bot is running... Speak to interact!")

    while True:
        user_text = record_audio()
        if user_text:
            chat_response = chat_with_mistral(user_text)
            print(f"🤖 Bot: {chat_response}")
            asyncio.run(text_to_speech(chat_response))
