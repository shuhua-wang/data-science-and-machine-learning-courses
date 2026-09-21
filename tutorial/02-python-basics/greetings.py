"""Tiny helper module for Lesson 2.4 - Functions and Modules.

This file lives right next to the notebook, so it can be imported the same
way you would import any Python file you write yourself.
"""


def say_hello(name):
    """Return a friendly greeting for `name`."""
    return f"Hello, {name}!"


def shout(text):
    """Return `text` in uppercase with an exclamation mark on the end."""
    return text.upper() + "!"


def count_vowels(text):
    """Count the vowels (a, e, i, o, u) in `text`, case-insensitive."""
    vowels = "aeiou"
    count = 0
    for character in text.lower():
        if character in vowels:
            count += 1
    return count
