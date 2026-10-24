"""Management command: ``python manage.py chat``.

The terminal client. It reads a line from the user, asks ChatterBot for a
response and prints it, until the user types an exit word or presses
Ctrl-C / Ctrl-D. The output looks like this::

    user: Good morning! How are you doing?
    bot: I am doing very well, thank you for asking.

Author : Sammy Sheu
Course : Artificial Intelligence -- Assignment 3
"""

from __future__ import annotations

from argparse import ArgumentParser

from django.core.management.base import BaseCommand

from chat.bot import build_chatbot, is_trained, train_chatbot

# Typing any of these words (any case) ends the session.
EXIT_COMMANDS: frozenset[str] = frozenset({"exit", "quit", "bye"})

USER_PROMPT: str = "user: "
BOT_PREFIX: str = "bot: "


class Command(BaseCommand):
    """Start an interactive chat session with the bot in the terminal."""

    help = "Chat with the bot in the terminal. Type 'exit' to leave."

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--learn",
            action="store_true",
            help="Let the bot learn from this conversation (off by default).",
        )

    def handle(self, *args, **options) -> None:
        bot = build_chatbot(read_only=not options["learn"])

        # Train on first run so the client works right after `migrate`,
        # without a separate `train_bot` step.
        if not is_trained(bot):
            self.stdout.write("No training data found. Training the bot...")
            train_chatbot(bot)

        self._print_banner(bot.name)

        while True:
            try:
                user_text = input(USER_PROMPT).strip()
            except (EOFError, KeyboardInterrupt):
                # Ctrl-D (EOF) or Ctrl-C: leave on a fresh line, no traceback.
                self.stdout.write("")
                break

            if not user_text:
                continue  # Ignore blank lines instead of sending them.
            if user_text.lower() in EXIT_COMMANDS:
                break

            response = bot.get_response(user_text)
            self.stdout.write(f"{BOT_PREFIX}{response.text}")

        self.stdout.write(self.style.SUCCESS("Goodbye!"))

    def _print_banner(self, bot_name: str) -> None:
        """Print a short header explaining how to use the client."""
        title = f"{bot_name} -- Django + ChatterBot terminal client"
        self.stdout.write(self.style.MIGRATE_HEADING(title))
        self.stdout.write("-" * len(title))
        self.stdout.write("Type a message and press Enter. Type 'exit' to quit.\n")
