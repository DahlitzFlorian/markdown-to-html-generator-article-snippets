# blog.py

import re

WPM = 200
WORD_LENGTH = 5


def _count_words_in_text(text: str) -> int:
    return len(text) // WORD_LENGTH


def _filter_visible_text(text: str) -> str:
    clear_html_tags = re.compile("<.*?>")
    text = re.sub(clear_html_tags, "", text)
    return "".join(text.split())


def estimate_reading_time(text: str) -> int:
    filtered_text = _filter_visible_text(text)
    total_words = _count_words_in_text(filtered_text)
    return total_words // WPM
