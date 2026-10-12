# Voice AI Assistant GUI

A Python desktop voice assistant with a Tkinter chat interface, microphone speech recognition, spoken responses, and quick actions for time/date, Google, YouTube, Wikipedia, web search, and jokes.

## Requirements
- Python 3.9 or newer
- Working microphone and speakers
- Internet connection for Google speech recognition and browser search

## Setup

```bash
python -m venv .venv
```

Windows:
```powershell
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

macOS/Linux:
```bash
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

If `PyAudio` fails to install, install the platform's audio development dependencies or use a compatible Python version, then retry. On Windows, a compatible prebuilt PyAudio wheel may be needed.

## Usage
- Type in the message field and press **Send** or Enter.
- Click **Speak** and say a command.
- Try: `what time is it`, `what is the date`, `open Google`, `open YouTube`, `search for Java tutorials`, `search Wikipedia for Python`, or `tell me a joke`.
- Say `exit` to close the application.

## Architecture
- `main.py`: GUI, command routing, microphone input, and text-to-speech.
- `requirements.txt`: Python dependencies.
- `screenshots/`: place application screenshots here.

## Notes
Speech recognition uses Google's online recognition service, so it requires internet access and sends recorded speech to that service. This starter version uses rule-based command handling rather than an LLM. To add open-ended AI conversation, connect a language-model API inside `handle_text()` and store API keys in environment variables—never commit secrets to GitHub.
