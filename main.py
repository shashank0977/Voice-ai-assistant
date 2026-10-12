"""
Voice AI Assistant GUI
A Tkinter desktop assistant with typed commands, optional speech recognition,
text-to-speech, web shortcuts, time/date, Wikipedia summaries, and jokes.
"""
from __future__ import annotations

import queue
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
import webbrowser
from urllib.parse import quote_plus

from assistant_core import AssistantCore
from speech_service import SpeechService


class VoiceAssistantApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Voice AI Assistant")
        self.root.geometry("820x650")
        self.root.minsize(650, 520)
        self.root.configure(bg="#101820")

        self.events = queue.Queue()
        self.core = AssistantCore()
        self.speech = SpeechService()
        self.speaking_enabled = tk.BooleanVar(value=True)
        self.status = tk.StringVar(value="Ready • Type a message or use Speak")
        self._build_ui()
        self.root.after(100, self._process_events)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self._append_message("Assistant", "Hi! I'm your Voice AI Assistant. Try “what time is it”, “search for Java tutorials”, “open YouTube”, or “tell me a joke”.")

    def _build_ui(self):
        header = tk.Frame(self.root, bg="#172b3a", padx=18, pady=14)
        header.pack(fill="x")
        tk.Label(header, text="🎙 Voice AI Assistant", bg="#172b3a", fg="#ffffff",
                 font=("Segoe UI", 19, "bold")).pack(anchor="w")
        tk.Label(header, text="Voice commands • Quick actions • Spoken responses",
                 bg="#172b3a", fg="#b9cbd8", font=("Segoe UI", 10)).pack(anchor="w", pady=(3, 0))

        actions = tk.Frame(self.root, bg="#101820", padx=14, pady=10)
        actions.pack(fill="x")
        for label, command in [
            ("Time / Date", lambda: self._submit_text("what time is it")),
            ("Google", lambda: self._submit_text("open Google")),
            ("YouTube", lambda: self._submit_text("open YouTube")),
            ("Clear chat", self.clear_chat),
        ]:
            tk.Button(actions, text=label, command=command, relief="flat",
                      bg="#24536b", fg="white", activebackground="#36738f",
                      activeforeground="white", padx=12, pady=7).pack(side="left", padx=(0, 7))

        self.chat = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state="disabled", font=("Segoe UI", 11),
            bg="#f4f7fa", fg="#1d2730", padx=12, pady=12, relief="flat",
            insertbackground="#1d2730"
        )
        self.chat.pack(fill="both", expand=True, padx=14, pady=(0, 10))
        self.chat.tag_config("user", foreground="#155e75", font=("Segoe UI", 10, "bold"))
        self.chat.tag_config("assistant", foreground="#234e70", font=("Segoe UI", 10, "bold"))
        self.chat.tag_config("body", foreground="#1d2730")

        input_frame = tk.Frame(self.root, bg="#101820", padx=14, pady=(0, 10))
        input_frame.pack(fill="x")
        self.entry = tk.Entry(input_frame, font=("Segoe UI", 12), relief="flat",
                              bg="white", fg="#1d2730")
        self.entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 8))
        self.entry.bind("<Return>", lambda _event: self.send_typed())
        tk.Button(input_frame, text="Send", command=self.send_typed, bg="#167d6a",
                  fg="white", activebackground="#209b83", activeforeground="white",
                  relief="flat", padx=18, pady=10).pack(side="left", padx=(0, 7))
        tk.Button(input_frame, text="🎤 Speak", command=self.listen, bg="#b45f06",
                  fg="white", activebackground="#d97706", activeforeground="white",
                  relief="flat", padx=15, pady=10).pack(side="left")

        options = tk.Frame(self.root, bg="#101820", padx=16, pady=(0, 10))
        options.pack(fill="x")
        tk.Checkbutton(options, text="Speak responses aloud", variable=self.speaking_enabled,
                       bg="#101820", fg="#d8e2e8", selectcolor="#172b3a",
                       activebackground="#101820", activeforeground="white").pack(side="left")
        tk.Label(options, textvariable=self.status, bg="#101820", fg="#9fb3c1",
                 font=("Segoe UI", 9)).pack(side="right")

    def _append_message(self, speaker: str, text: str):
        self.chat.configure(state="normal")
        tag = "user" if speaker == "You" else "assistant"
        self.chat.insert(tk.END, f"{speaker}: ", tag)
        self.chat.insert(tk.END, text + "\n\n", "body")
        self.chat.configure(state="disabled")
        self.chat.see(tk.END)

    def _submit_text(self, text: str):
        text = text.strip()
        if not text:
            return
        self._append_message("You", text)
        self.entry.delete(0, tk.END)
        self.status.set("Working…")
        threading.Thread(target=self._handle_command, args=(text,), daemon=True).start()

    def send_typed(self):
        self._submit_text(self.entry.get())

    def _handle_command(self, text: str):
        try:
            result = self.core.handle_command(text)
            self.events.put(("response", result))
        except Exception as exc:
            self.events.put(("error", f"Something went wrong: {exc}"))

    def listen(self):
        self.status.set("Listening… speak after the prompt")
        threading.Thread(target=self._listen_worker, daemon=True).start()

    def _listen_worker(self):
        recognized, error = self.speech.listen_once()
        if error:
            self.events.put(("error", error))
        elif recognized:
            self.events.put(("recognized", recognized))
        else:
            self.events.put(("error", "No speech was recognized. Please try again."))

    def _process_events(self):
        try:
            while True:
                kind, payload = self.events.get_nowait()
                if kind == "recognized":
                    self._append_message("You (voice)", payload)
                    self.status.set("Processing voice command…")
                    threading.Thread(target=self._handle_command, args=(payload,), daemon=True).start()
                elif kind == "response":
                    self._append_message("Assistant", payload.text)
                    self.status.set("Ready")
                    if self.speaking_enabled.get() and payload.speak:
                        threading.Thread(target=self.speech.speak, args=(payload.text,), daemon=True).start()
                    if payload.should_exit:
                        self.root.after(500, self.close)
                elif kind == "error":
                    self._append_message("Assistant", payload)
                    self.status.set("Check microphone / connection")
        except queue.Empty:
            pass
        if self.root.winfo_exists():
            self.root.after(100, self._process_events)

    def clear_chat(self):
        self.chat.configure(state="normal")
        self.chat.delete("1.0", tk.END)
        self.chat.configure(state="disabled")
        self._append_message("Assistant", "Conversation cleared. What would you like to do?")
        self.status.set("Ready")

    def close(self):
        try:
            self.speech.stop()
        except Exception:
            pass
        self.root.destroy()


def main():
    root = tk.Tk()
    VoiceAssistantApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
