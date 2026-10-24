"""Conversations used to train the bot.

Each inner tuple is one conversation, in order. ChatterBot's ListTrainer
learns every line as the response to the line before it. For example, the
first conversation teaches the bot to answer "You're welcome." with
"Do you like hats?", as in the sample input/output in the assignment.

Author : Sammy Sheu
Course : Artificial Intelligence -- Assignment 3
"""

from __future__ import annotations

CONVERSATIONS: tuple[tuple[str, ...], ...] = (
    # Sample dialog from the assignment instructions.
    (
        "Good morning! How are you doing?",
        "I am doing very well, thank you for asking.",
        "You're welcome.",
        "Do you like hats?",
        "Yes, I like hats a lot.",
        "Hats are great. What kind of hat do you have?",
    ),
    # Greetings.
    (
        "Hello",
        "Hi there!",
        "How are you?",
        "I am doing great. How about you?",
        "I am fine, thanks.",
        "Glad to hear it.",
    ),
    (
        "Good evening!",
        "Good evening! How was your day?",
        "It was a long day.",
        "I hope you get some rest tonight.",
    ),
    # About the bot itself.
    (
        "What is your name?",
        "My name is Terminal Bot.",
        "Who made you?",
        "I was built with Python, Django and ChatterBot.",
        "What can you do?",
        "I can chat with you and do simple math, like 'what is 12 times 3'.",
    ),
    (
        "Are you a robot?",
        "Yes, I am a chat bot that learns from example conversations.",
        "How do you learn?",
        "I store example conversations and answer with the closest match I know.",
    ),
    # Small talk.
    (
        "Do you like hats?",
        "Yes, I like hats a lot.",
    ),
    (
        "What is your favorite color?",
        "I like blue. It is the color of a terminal on a good day.",
    ),
    (
        "Tell me a joke.",
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "That's funny.",
        "I'm glad you liked it!",
    ),
    (
        "Thank you.",
        "You're welcome.",
    ),
    # Farewells.
    (
        "Goodbye",
        "Goodbye! It was nice talking to you.",
    ),
)
