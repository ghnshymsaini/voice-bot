import speech_recognition as sr


def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.AudioFile("your-audio-file.wav") as source:
        audio = recognizer.record(source)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except sr.RequestError:
        return "Speech recognition service is unavailable."
