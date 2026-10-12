"""Voice AI Assistant GUI — desktop assistant with speech input and spoken replies."""
import datetime
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
import webbrowser

try:
    import speech_recognition as sr
except ImportError:
    sr = None
try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

APP_TITLE = "Voice AI Assistant"

class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("760x620")
        self.root.minsize(620, 500)
        self.root.configure(bg="#101827")
        self.recognizer = sr.Recognizer() if sr else None
        self.tts = pyttsx3.init() if pyttsx3 else None
        self._build_ui()
        self.add_message("Assistant", "Hi! I'm your Voice AI Assistant. Type a message or click 🎤 Speak.")

    def _build_ui(self):
        header = tk.Frame(self.root, bg="#17243a", padx=18, pady=15)
        header.pack(fill="x")
        tk.Label(header, text="🎙 Voice AI Assistant", font=("Segoe UI", 20, "bold"),
                 fg="white", bg="#17243a").pack(anchor="w")
        tk.Label(header, text="Voice commands • Quick actions • Spoken responses",
                 font=("Segoe UI", 10), fg="#b7c7df", bg="#17243a").pack(anchor="w", pady=(3, 0))

        self.chat = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state="disabled",
            font=("Segoe UI", 11), bg="#f4f7fb", fg="#182235", padx=12, pady=12,
            relief="flat", borderwidth=0)
        self.chat.pack(fill="both", expand=True, padx=16, pady=14)
        self.chat.tag_config("user", foreground="#155eef", font=("Segoe UI", 10, "bold"))
        self.chat.tag_config("assistant", foreground="#07805b", font=("Segoe UI", 10, "bold"))
        self.chat.tag_config("body", foreground="#182235")

        quick = tk.Frame(self.root, bg="#101827")
        quick.pack(fill="x", padx=16, pady=(0, 8))
        for label, command in [("🕒 Time", lambda: self.handle_text("what time is it")),
                               ("📅 Date", lambda: self.handle_text("what is the date")),
                               ("🌐 Google", lambda: self.handle_text("open google")),
                               ("▶ YouTube", lambda: self.handle_text("open youtube")),
                               ("🧹 Clear", self.clear_chat)]:
            tk.Button(quick, text=label, command=command, bg="#24344d", fg="white",
                      activebackground="#344967", activeforeground="white", relief="flat",
                      padx=10, pady=7, cursor="hand2").pack(side="left", padx=(0, 7))

        bottom = tk.Frame(self.root, bg="#101827", padx=16, pady=12)
        bottom.pack(fill="x")
        self.entry = tk.Entry(bottom, font=("Segoe UI", 11), bg="white", fg="#182235",
                              relief="flat", insertbackground="#182235")
        self.entry.pack(side="left", fill="x", expand=True, ipady=11, padx=(0, 8))
        self.entry.bind("<Return>", lambda _event: self.send_text())
        tk.Button(bottom, text="Send", command=self.send_text, bg="#2563eb", fg="white",
                  relief="flat", padx=16, pady=9).pack(side="left", padx=(0, 7))
        tk.Button(bottom, text="🎤 Speak", command=self.listen_async, bg="#07805b", fg="white",
                  relief="flat", padx=14, pady=9).pack(side="left")
        self.status = tk.Label(self.root, text="Ready", anchor="w", bg="#101827", fg="#9fb0c8",
                               font=("Segoe UI", 9), padx=17, pady=4)
        self.status.pack(fill="x")

    def add_message(self, speaker, text):
        self.chat.configure(state="normal")
        tag = "user" if speaker == "You" else "assistant"
        self.chat.insert(tk.END, f"{speaker}\n", tag)
        self.chat.insert(tk.END, f"{text}\n\n", "body")
        self.chat.configure(state="disabled")
        self.chat.see(tk.END)

    def speak(self, text):
        if not self.tts:
            return
        def run():
            try:
                self.tts.say(text)
                self.tts.runAndWait()
            except Exception:
                pass
        threading.Thread(target=run, daemon=True).start()

    def send_text(self):
        text = self.entry.get().strip()
        if text:
            self.entry.delete(0, tk.END)
            self.handle_text(text)

    def handle_text(self, text):
        self.add_message("You", text)
        query = text.lower().strip()
        now = datetime.datetime.now()
        if any(x in query for x in ("what time", "current time", "tell me the time")):
            response = "The current time is " + now.strftime("%I:%M %p") + "."
        elif any(x in query for x in ("what is the date", "today's date", "current date", "what day")):
            response = "Today is " + now.strftime("%A, %d %B %Y") + "."
        elif "open google" in query or query == "google":
            webbrowser.open("https://www.google.com")
            response = "Opening Google in your browser."
        elif "open youtube" in query or query == "youtube":
            webbrowser.open("https://www.youtube.com")
            response = "Opening YouTube in your browser."
        elif "wikipedia" in query:
            term = query.replace("search wikipedia for", "").replace("wikipedia", "").strip()
            if term:
                webbrowser.open("https://en.wikipedia.org/wiki/" + term.replace(" ", "_"))
                response = f"Opening Wikipedia results for {term}."
            else:
                webbrowser.open("https://www.wikipedia.org")
                response = "Opening Wikipedia."
        elif "search" in query:
            term = query.replace("search for", "").replace("search", "").strip()
            if term:
                webbrowser.open("https://www.google.com/search?q=" + term.replace(" ", "+"))
                response = f"Searching Google for {term}."
            else:
                response = "Tell me what you would like me to search for."
        elif "joke" in query:
            response = "Why do programmers prefer dark mode? Because light attracts bugs!"
        elif any(x in query for x in ("exit", "quit", "close assistant")):
            response = "Goodbye! Closing the assistant."
            self.add_message("Assistant", response)
            self.speak(response)
            self.root.after(900, self.root.destroy)
            return
        elif query in ("hi", "hello", "hey", "hi assistant", "hello assistant"):
            response = "Hello! How can I help you?"
        else:
            response = "I can help with the time, date, Google search, YouTube, Wikipedia, and jokes. For open-ended AI conversation, connect an LLM API in the response handler."
        self.add_message("Assistant", response)
        self.speak(response)

    def listen_async(self):
        if not sr:
            messagebox.showerror("Missing dependency", "Install SpeechRecognition and PyAudio from requirements.txt first.")
            return
        threading.Thread(target=self._listen, daemon=True).start()

    def _listen(self):
        try:
            self.root.after(0, lambda: self.status.config(text="Listening… speak now"))
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
            self.root.after(0, lambda: self.status.config(text="Recognizing speech…"))
            text = self.recognizer.recognize_google(audio)
            self.root.after(0, lambda: self.handle_text(text))
            self.root.after(0, lambda: self.status.config(text="Ready"))
        except sr.WaitTimeoutError:
            self.root.after(0, lambda: self.status.config(text="No speech detected. Try again."))
        except sr.UnknownValueError:
            self.root.after(0, lambda: self.status.config(text="Sorry, I couldn't understand that."))
        except Exception as exc:
            self.root.after(0, lambda: self.status.config(text=f"Microphone/recognition error: {exc}"))

    def clear_chat(self):
        self.chat.configure(state="normal")
        self.chat.delete("1.0", tk.END)
        self.chat.configure(state="disabled")
        self.add_message("Assistant", "Chat cleared. What can I do for you?")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    root.mainloop()
