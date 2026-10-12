"""Optional speech input/output adapters. Import failures are reported gracefully."""
import threading


class SpeechService:
    def __init__(self):
        self._tts_lock = threading.Lock()
        self._engine = None
        self._sr = None
        try:
            import pyttsx3
            self._engine = pyttsx3.init()
            self._engine.setProperty("rate", 175)
        except Exception:
            self._engine = None
        try:
            import speech_recognition as sr
            self._sr = sr
        except Exception:
            self._sr = None

    def listen_once(self):
        if self._sr is None:
            return None, "Speech recognition is not installed. Run: pip install SpeechRecognition PyAudio"
        recognizer = self._sr.Recognizer()
        try:
            with self._sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            try:
                text = recognizer.recognize_google(audio)
                return text, None
            except self._sr.UnknownValueError:
                return None, "I couldn't understand that speech. Please speak clearly and try again."
            except self._sr.RequestError:
                return None, "Speech recognition service is unavailable. Check your internet connection."
        except self._sr.WaitTimeoutError:
            return None, "I didn't hear anything. Tap Speak and try again."
        except AttributeError:
            return None, "No compatible microphone input is available."
        except Exception as exc:
            return None, f"Microphone error: {exc}"

    def speak(self, text: str):
        if self._engine is None:
            return
        try:
            with self._tts_lock:
                self._engine.say(text)
                self._engine.runAndWait()
        except Exception:
            # GUI remains usable even if the system voice engine is unavailable.
            pass

    def stop(self):
        if self._engine is not None:
            try:
                self._engine.stop()
            except Exception:
                pass
