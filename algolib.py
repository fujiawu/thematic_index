"""
This is the module for algo library
"""

from datalib import *
import re


def compare_tokens(word, topic):
    """
    decide whether the topic include this word
    :param word: word to search in the topic
    :param topic: topic to search in
    :return: percentage of characters that matched
    """
    topic = topic.replace(".", "").replace("-", "").lower()
    word = word.replace(".", "").replace("-", "").lower()
    topics = re.split("[(/), !;?:.]+", topic)
    words = re.split("[ ]+", word)
    matched = 0
    for t in topics:
        for w in words:
            if t == w:
                matched += len(w)
    return float(matched) / float(max(len(topic), len(word)))


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
                    "thing", "person", "high", "service", "services", "staffing", "staff", "technology",
                    "information", "info", "corporation", "limited", "private", "municipal", "management",
                    "investment", "level", "income", "federal", "tax", "dollar", "bond", "bonds"]
    adjusted_word_list = []
    for word in words:
        word = word.lower()
        if is_ascii(word) and len(word) > 2 and word not in trivial_list:
            adjusted_word_list.append(word)
    two_grams = []
    for i in range(len(adjusted_word_list)-1):
        two_grams.append(adjusted_word_list[i]+" "+adjusted_word_list[i+1])
    matched = []
    for words in two_grams:
        for topic in topics:
            match_rate = compare_tokens(words, topic)
            if match_rate:
                matched.append({"topic": topic, "words": words, "match_rate": match_rate, "level": topics[topic]})
    return matched


def compute_score(matched):
    """
    given matched words found, compute score using custom function
    :param matched: a list of words found with level
    :return: score: numeric
    """
    level_to_score = [6, 2, 0.1, 0.05, 0.02, 0.01, 0.005]
    power = 5
    score = 0
    for m in matched:
        if m["level"] < len(level_to_score):
            # print "%s,%s,%d,%2.2f" % (m["words"], m["topic"], m["level"], m["match_rate"])
            score += level_to_score[m["level"]]*m["match_rate"]**power
    return score

