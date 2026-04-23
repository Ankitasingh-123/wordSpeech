# import tkinter as tk

# root = tk.Tk()
# root.title("Test Window")
# root.geometry("300x200")

# label = tk.Label(root, text="Tkinter Working!", font=("Arial", 14))
# label.pack(pady=50)

# root.mainloop()
# import pyttsx3

# def get_voices():
#     engine = pyttsx3.init()
#     voices = engine.getProperty('voices')
#     return voices

from deep_translator import GoogleTranslator

text = "Hello, how are you?"
translated = GoogleTranslator(source='auto', target='hi').translate(text)

print(translated)