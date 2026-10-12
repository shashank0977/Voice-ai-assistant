"""Command routing kept separate from the GUI for easier testing."""
from dataclasses import dataclass
from datetime import datetime
import random
import webbrowser
from urllib.parse import quote_plus
import requests


@dataclass
class CommandResult:
    text: str
    speak: bool = True
    should_exit: bool = False


class AssistantCore:
    JOKES = [
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "There are 10 kinds of people: those who understand binary and those who don't.",
        "Why did the developer go broke? Because they used up all their cache."
    ]

    def handle_command(self, raw_text: str) -> CommandResult:
        text = raw_text.strip()
        normalized = " ".join(text.lower().split())
        if not normalized:
            return CommandResult("Please enter or say a command.", speak=False)

        if normalized in {"exit", "quit", "close assistant", "stop assistant"}:
            return CommandResult("Goodbye! See you next time.", should_exit=True)
        if any(phrase in normalized for phrase in ("what time", "current time", "tell me the time")):
            return CommandResult("The current time is " + datetime.now().strftime("%I:%M %p") + ".")
        if any(phrase in normalized for phrase in ("what date", "today's date", "current date", "what day")):
            return CommandResult("Today's date is " + datetime.now().strftime("%A, %d %B %Y") + ".")
        if normalized in {"open google", "google"}:
            webbrowser.open("https://www.google.com")
            return CommandResult("Opening Google.")
        if normalized in {"open youtube", "youtube"}:
            webbrowser.open("https://www.youtube.com")
            return CommandResult("Opening YouTube.")
        if normalized in {"open wikipedia", "wikipedia"}:
            webbrowser.open("https://www.wikipedia.org")
            return CommandResult("Opening Wikipedia.")
        if normalized.startswith("search for "):
            query = text[len("search for "):].strip()
            if not query:
                return CommandResult("Tell me what you want to search for.")
            webbrowser.open("https://www.google.com/search?q=" + quote_plus(query))
            return CommandResult(f"Searching Google for {query}.")
        if normalized.startswith("search wikipedia for "):
            query = text[len("search wikipedia for "):].strip()
            return self.wikipedia_summary(query)
        if normalized.startswith("tell me about "):
            query = text[len("tell me about "):].strip()
            return self.wikipedia_summary(query)
        if "wikipedia" in normalized and " for " in normalized:
            query = text.lower().split(" for ", 1)[1].strip()
            return self.wikipedia_summary(query)
        if "joke" in normalized:
            return CommandResult(random.choice(self.JOKES))
        if normalized in {"help", "what can you do", "commands"}:
            return CommandResult(
                "I can tell the time or date, open Google/YouTube/Wikipedia, search Google, "
                "summarize a Wikipedia topic, tell a joke, clear the chat using the button, or exit."
            )
        return CommandResult(
            "I don't know that command yet. Try “help”, “what time is it”, "
            "“search for Java tutorials”, “tell me about Python”, or “tell me a joke”."
        )

    def wikipedia_summary(self, query: str) -> CommandResult:
        if not query:
            return CommandResult("Please provide a topic to look up.")
        try:
            url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + quote_plus(query.replace(" ", "_"))
            response = requests.get(url, timeout=7, headers={"User-Agent": "VoiceAIAssistant/1.0"})
            if response.status_code == 404:
                return CommandResult(f"I couldn't find a Wikipedia summary for {query}.")
            response.raise_for_status()
            data = response.json()
            extract = data.get("extract")
            if extract:
                return CommandResult(extract[:900])
            return CommandResult(f"No summary was available for {query}.")
        except requests.RequestException:
            return CommandResult("Wikipedia lookup failed. Check your internet connection and try again.")
        except (ValueError, TypeError):
            return CommandResult("Wikipedia returned an unexpected response. Please try again.")
