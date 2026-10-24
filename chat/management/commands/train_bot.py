"""Management command: ``python manage.py train_bot``.

Rebuilds the bot's knowledge from the conversations in
:mod:`chat.training_data`. Existing statements are cleared first, so running
the command again never stores duplicate rows. Use ``--keep`` to add the
training data on top of what the bot already knows (for example, statements
it learned with ``chat --learn``).

Author : Sammy Sheu
Course : Artificial Intelligence -- Assignment 3
"""

from __future__ import annotations

from argparse import ArgumentParser

from django.core.management.base import BaseCommand

from chat.bot import build_chatbot, train_chatbot


class Command(BaseCommand):
    """Train the ChatterBot instance on the project's example conversations."""

    help = "Train the chat bot on the conversations in chat/training_data.py."

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            "--keep",
            action="store_true",
            help="Keep existing statements instead of clearing them first.",
        )

    def handle(self, *args, **options) -> None:
        bot = build_chatbot()

        if not options["keep"]:
            # drop() removes every Statement and Tag row the bot has stored.
            bot.storage.drop()
            self.stdout.write("Cleared existing training data.")

        count = train_chatbot(bot)
        self.stdout.write(
            self.style.SUCCESS(
                f"Trained on {count} conversations "
                f"({bot.storage.count()} statements stored)."
            )
        )
