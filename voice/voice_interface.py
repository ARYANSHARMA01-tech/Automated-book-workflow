import pyttsx3
import threading
import speech_recognition as sr

# Initialize globally
engine = pyttsx3.init()

def speak(text):
    def run_speech():
        engine.say(text)
        engine.runAndWait()

    threading.Thread(target=run_speech).start()

def stop_speaking():
    engine.stop()

def listen(timeout=5):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=timeout)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "Speech recognition service error"
