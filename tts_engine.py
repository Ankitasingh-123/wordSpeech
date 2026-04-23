import pyttsx3
from gtts import gTTS
from playsound import playsound
import os

engine = pyttsx3.init()

# 🔊 Speak (English offline)
def speak_text(text, rate=150, volume=1.0, voice_id=None):
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    if voice_id:
        engine.setProperty('voice', voice_id)

    engine.say(text)
    engine.runAndWait()

# 🇮🇳 Hindi (online)
def speak_hindi(text):
    try:
        tts = gTTS(text=text, lang='hi')
        filename = "temp.mp3"
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
    except Exception as e:
        print("Error:", e)

# 💾 Save
def save_audio(text, filename, lang="en"):
    try:
        if lang == "hi":
            tts = gTTS(text=text, lang='hi')
            tts.save(filename)
        else:
            engine.save_to_file(text, filename)
            engine.runAndWait()
    except Exception as e:
        print("Error:", e)

# 🎤 Voice list
def get_voices():
    return engine.getProperty('voices')