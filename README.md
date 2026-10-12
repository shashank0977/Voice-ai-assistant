# Voice AI Assistant GUI

A Python desktop voice assistant built with Tkinter. It supports typed commands, optional microphone speech recognition, spoken responses, browser shortcuts, Google search, Wikipedia summaries, time/date queries, jokes, and a chat-style interface.

## Features

- Tkinter desktop GUI with chat history
- Type commands or use the **Speak** button
- Text-to-speech responses (when a system TTS engine is available)
- Time and date
- Open Google, YouTube, and Wikipedia
- Google web search
- Wikipedia topic summaries
- Built-in jokes and help command
- Clear-chat button and exit command
- Background workers for network/speech tasks so the GUI stays responsive
- Graceful error messages when optional speech services are unavailable

## Requirements

- Python 3.9+
- Desktop OS with Tkinter (usually included with standard Windows Python; Linux may require `python3-tk`)
- Internet for Google speech recognition, Google searches, and Wikipedia summaries
- Microphone for voice input
- Speakers/headphones for spoken responses

## Setup

### Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

If PyAudio installation fails, install a compatible PyAudio wheel for your Python version or run the app without microphone input. Typed commands and the GUI remain available.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

On Debian/Ubuntu, you may need OS packages first:

```bash
sudo apt install python3-tk portaudio19-dev python3-dev
```

Then install the Python requirements. Package names can differ by distribution.

## Example commands

- `help`
- `what time is it`
- `what date is it`
- `open Google`
- `open YouTube`
- `open Wikipedia`
- `search for Java tutorials`
- `search Wikipedia for Python`
- `tell me about machine learning`
- `tell me a joke`
- `exit`

Use the **Clear chat** button to clear the visible conversation.

## Project structure

```text
voice-ai-assistant/
├── main.py
├── assistant_core.py
├── speech_service.py
├── requirements.txt
├── README.md
├── .gitignore
├── docs/
│   └── project_report.docx
├── screenshots/
└── tests/
    └── test_assistant_core.py
```

## Testing

Run the command-routing tests:

```bash
python -m unittest discover -s tests -v
```

The tests mock browser opening and do not require a microphone. Microphone and audio output should be tested on the target computer.

## Notes and limitations

- This is a command-based assistant, not an LLM-powered open-ended chatbot.
- Google speech recognition needs an internet connection and sends recorded audio to Google's recognition service.
- Wikipedia lookups use the public Wikipedia REST API.
- Text-to-speech depends on the operating system's available voice engine.
- Do not put API keys, passwords, or private data in the repository.

## Future improvements

LLM integration, multilingual support, wake-word detection, reminders, and configurable desktop actions can be added later.
