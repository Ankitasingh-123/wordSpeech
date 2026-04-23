import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox

from tts_engine import speak_text, speak_hindi, save_audio, get_voices
from file_handler import read_file

import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr

app = ttk.Window(themename="cosmo")
app.title("Smart AI Voice Assistant")
app.geometry("900x750")

voices = get_voices()

# 🌍 Language
lang_var = ttk.StringVar(value="English")

# 🎚 Speed & Volume
rate_var = ttk.IntVar(value=150)
volume_var = ttk.DoubleVar(value=1.0)

# 👨👩 Voice type
voice_var = ttk.StringVar(value="Male")

# 🌙 Theme
def toggle_theme():
    if app.style.theme.name == "cosmo":
        app.style.theme_use("darkly")
    else:
        app.style.theme_use("cosmo")

# ▶ Speak
def speak():
    text = text_box.get("1.0", "end").strip()
    if not text:
        messagebox.showwarning("Warning", "Enter text!")
        return

    try:
        voice_id = voices[0].id if voice_var.get() == "Male" else voices[1].id

        if lang_var.get() == "Hindi":
            speak_hindi(text)
        else:
            speak_text(text, rate_var.get(), volume_var.get(), voice_id)

        status_label.config(text="Speaking...")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# 💾 Save
def save():
    text = text_box.get("1.0", "end").strip()
    name = file_entry.get() or "output"

    try:
        lang = "hi" if lang_var.get() == "Hindi" else "en"
        save_audio(text, f"audio/{name}.mp3", lang)
        status_label.config(text="Saved!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# 📂 Upload
def upload():
    path = filedialog.askopenfilename(filetypes=[("Files", "*.txt *.pdf *.docx")])
    if path:
        content = read_file(path)
        text_box.delete("1.0", "end")
        text_box.insert("end", content)

# 🎤 Mic
def mic_input():
    try:
        status_label.config(text="Listening...")
        app.update()

        fs = 44100
        duration = 5

        rec = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()

        wav.write("temp.wav", fs, rec)

        r = sr.Recognizer()
        with sr.AudioFile("temp.wav") as source:
            audio = r.record(source)
            text = r.recognize_google(audio)

        text_box.insert("end", text + "\n")
        status_label.config(text="Converted!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# 🗑 Clear
def clear():
    text_box.delete("1.0", "end")

# 🎴 UI
card = ttk.Frame(app, padding=20)
card.pack(fill="both", expand=True)

ttk.Label(card, text="🎤 Smart AI Voice Assistant",
          font=("Arial", 22, "bold")).pack(pady=10)

text_box = ttk.Text(card, height=10)
text_box.pack(fill="x", pady=10)

ttk.Label(card, text="Enter File Name").pack()
file_entry = ttk.Entry(card)
file_entry.pack()
file_entry.pack(fill="x", pady=5)

# 🌍 Language
ttk.Label(card, text="Language").pack()
ttk.Combobox(card, textvariable=lang_var,
             values=["English", "Hindi"]).pack()

# 🎚 Speed
ttk.Label(card, text="Speed").pack()
ttk.Scale(card, from_=100, to=300, variable=rate_var).pack()

# 🔊 Volume
ttk.Label(card, text="Volume").pack()
ttk.Scale(card, from_=0, to=1, variable=volume_var).pack()

# 👨👩 Voice
ttk.Label(card, text="Voice Type").pack()
ttk.Radiobutton(card, text="Male", variable=voice_var, value="Male").pack()
ttk.Radiobutton(card, text="Female", variable=voice_var, value="Female").pack()

# 🔘 Buttons
frame = ttk.Frame(card)
frame.pack(pady=15)

ttk.Button(frame, text="▶ Speak", command=speak).grid(row=0, column=0, padx=5)
ttk.Button(frame, text="💾 Save", command=save).grid(row=0, column=1, padx=5)
ttk.Button(frame, text="📂 Upload", command=upload).grid(row=0, column=2, padx=5)
ttk.Button(frame, text="🎤 Mic", command=mic_input).grid(row=0, column=3, padx=5)
ttk.Button(frame, text="🌙 Mode", command=toggle_theme).grid(row=0, column=4, padx=5)
ttk.Button(frame, text="🗑 Clear", command=clear).grid(row=0, column=5, padx=5)

status_label = ttk.Label(card, text="")
status_label.pack()

app.mainloop()