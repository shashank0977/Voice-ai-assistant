import unittest
from unittest.mock import patch
from assistant_core import AssistantCore


class AssistantCoreTests(unittest.TestCase):
    def setUp(self):
        self.core = AssistantCore()

    @patch("assistant_core.datetime")
    def test_time_command(self, mock_datetime):
        mock_datetime.now.return_value.strftime.return_value = "10:30 AM"
        result = self.core.handle_command("what time is it")
        self.assertIn("10:30 AM", result.text)

    @patch("assistant_core.webbrowser.open")
    def test_open_youtube(self, mock_open):
        result = self.core.handle_command("open YouTube")
        mock_open.assert_called_once_with("https://www.youtube.com")
        self.assertIn("YouTube", result.text)

    @patch("assistant_core.webbrowser.open")
    def test_google_search(self, mock_open):
        result = self.core.handle_command("search for Java tutorials")
        mock_open.assert_called_once_with("https://www.google.com/search?q=Java+tutorials")
        self.assertIn("Searching Google", result.text)

    def test_joke_command(self):
        result = self.core.handle_command("tell me a joke")
        self.assertTrue(result.text)

    def test_exit_command(self):
        result = self.core.handle_command("exit")
        self.assertTrue(result.should_exit)

    def test_unknown_command_has_guidance(self):
        result = self.core.handle_command("launch a spaceship")
        self.assertIn("don't know", result.text.lower())


if __name__ == "__main__":
    unittest.main()
