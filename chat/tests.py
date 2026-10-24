"""Tests for the chat app. Run with ``python manage.py test chat``.

Django runs these against a temporary test database, so they never touch the
bot's real training data in db.sqlite3.

Author : Sammy Sheu
Course : Artificial Intelligence -- Assignment 3
"""

from __future__ import annotations

from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from chat.bot import build_chatbot, is_trained, train_chatbot


class ChatBotTrainingTests(TestCase):
    """The bot learns the training conversations and answers from them."""

    def setUp(self) -> None:
        self.bot = build_chatbot()
        train_chatbot(self.bot)

    def test_training_stores_statements(self) -> None:
        self.assertTrue(is_trained(self.bot))

    def test_sample_dialog_from_assignment(self) -> None:
        # The exact input/output pairs given in the assignment instructions.
        expected = {
            "Good morning! How are you doing?": "I am doing very well, thank you for asking.",
            "You're welcome.": "Do you like hats?",
        }
        for prompt, reply in expected.items():
            with self.subTest(prompt=prompt):
                self.assertEqual(self.bot.get_response(prompt).text, reply)

    def test_math_question(self) -> None:
        response = self.bot.get_response("What is 4 + 9?")
        self.assertIn("13", response.text)


class ChatCommandTests(TestCase):
    """The terminal client's input loop."""

    def run_chat(self, *lines: str) -> str:
        """Run ``manage.py chat`` with ``lines`` as typed input; return stdout."""
        out = StringIO()
        with mock.patch("builtins.input", side_effect=list(lines)):
            call_command("chat", stdout=out)
        return out.getvalue()

    def test_trains_on_first_run_and_replies(self) -> None:
        output = self.run_chat("Good morning! How are you doing?", "exit")
        self.assertIn("Training the bot", output)
        self.assertIn("bot: I am doing very well, thank you for asking.", output)
        self.assertIn("Goodbye!", output)

    def test_ctrl_c_exits_cleanly(self) -> None:
        output = self.run_chat(KeyboardInterrupt())
        self.assertIn("Goodbye!", output)

    def test_blank_input_is_ignored(self) -> None:
        output = self.run_chat("", "   ", "quit")
        self.assertNotIn("bot:", output)
