"""Factory and helpers for the project's ChatterBot instance.

Every part of the project (the training command, the chat command and the
tests) builds its bot through :func:`build_chatbot`. That keeps the
configuration in one place: the ``CHATBOT_CONFIG`` dictionary in
``chatbot_project/settings.py``.

Author : Sammy Sheu
Course : Artificial Intelligence -- Assignment 3
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from django.conf import settings

from chat.training_data import CONVERSATIONS


def build_chatbot(read_only: bool = True) -> ChatBot:
    """Create a ChatBot backed by Django's database.

    Args:
        read_only: When True (the default) the bot does not learn from the
            user's messages during a chat, so its answers stay predictable.
            Pass False to let it store every exchange as new knowledge.

    Returns:
        A configured :class:`chatterbot.ChatBot`.
    """
    # Copy the settings so the shared dictionary is never mutated. ChatBot()
    # takes the name positionally and everything else as keyword arguments.
    config = dict(settings.CHATBOT_CONFIG)
    name = config.pop("name")
    return ChatBot(name, read_only=read_only, **config)


def train_chatbot(
    bot: ChatBot,
    conversations: Iterable[Sequence[str]] = CONVERSATIONS,
) -> int:
    """Teach ``bot`` every conversation in ``conversations``.

    ListTrainer treats each line of a conversation as the reply to the line
    before it. It saves those (statement, response) pairs through the storage
    adapter, so here they become rows in Django's Statement table.

    Args:
        bot: The bot to train.
        conversations: Ordered lists of lines, one list per conversation.

    Returns:
        The number of conversations used for training.
    """
    trainer = ListTrainer(bot, show_training_progress=False)
    count = 0
    for conversation in conversations:
        trainer.train(list(conversation))
        count += 1
    return count


def is_trained(bot: ChatBot) -> bool:
    """Return True if the bot's database already holds learned statements."""
    return bot.storage.count() > 0
