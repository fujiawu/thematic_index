"""
This is the module for algo library
"""

from datalib import *
import re


def compare_words(word, topic):
    """
    decide whether the topic include this word
    :param word: word to search in the topic
    :param topic: topic to search in
    :return: percentage of characters that matched
    """
    tokens = re.split("[(/), !;?:.]+", topic)
    matched = 0
    total = 0
    for token in tokens:
        t = token.replace(".", "").replace("-", "").lower()
        w = word.replace(".", "").replace("-", "")
        if t == w:
            matched += len(w)
        total += len(t)
    return float(matched) / float(total)


def find_word_match(description, topics):
    """
    this function find words that matches those in a string with those in a topic dictionary
    :param description: input string to find those matches
    :param topics: dictionary of topics, such as google trend, with level information
    :return: a list with matches words and levels
    """
    words = re.split("[(/), !;?:.]+", description)
    trivial_list = ["and", "inc", "company", "the", "are", "that", "have", "for", "not", "you",
                    "with", "this", "but", "his", "her", "from", "say", "she", "will", "one",
                    "would", "all", "there", "their", "what", "out", "about", "get", "which",
                    "when", "can", "just", "him", "know", "take", "into", "year", "your", "than",
                    "good", "your", "some", "could", "them", "see", "other", "then", "now", "look",
                    "after", "also", "over", "its", "two", "how", "our", "work", "well", "most",
                    "any", "want", "way", "day", "because", "place", "number", "group", "fact",
                    "thing", "person", "high"]
    matched = []
    for word in words:
        word = word.lower()
        if is_ascii(word) and len(word) > 2 and word not in trivial_list:
            for topic in topics:
                match_rate = compare_words(word, topic)
                if match_rate:
                    matched.append({"topic" : topic, "word" : word, "match_rate": match_rate, "level" : topics[topic]})
    return matched


def compute_score(matched):
    """
    given matched words found, compute score using custom function
    :param matched: a list of words found with level
    :return: socre: numeric
    """
    level_to_score = [100, 40, 10, 5, 2, 1 ]
    score = 0
    for m in matched:
        if m["level"] < len(level_to_score):
            print m["word"], m["level"], m["match_rate"]
            score += level_to_score[m["level"]]*m["match_rate"]
    return score

