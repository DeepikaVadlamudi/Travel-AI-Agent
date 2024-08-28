import os
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound


def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "voice.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
            print(f"User said: {query}\n")
            return query
        except sr.UnknownValueError:
            print("Sorry, I did not catch that.")
            return None
        except sr.RequestError:
            print("Sorry, my speech service is down.")
            return None
