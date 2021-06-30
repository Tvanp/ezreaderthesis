"""
Trigrams from BNC.
"""

from collections import Counter
import pickle

from marisa_trie import Trie

with open("bnc_trigrams_marisa1.pickle", "rb") as inp:
    trie = pickle.load(inp)

with open("bnc_trigrams_marisa2.pickle", "rb") as inp:
    condfreq = pickle.load(inp)

def find_frequency_prefix(prefix):
    """
    :tuple prefix: prefix of which frequency should be found
    >>> find_frequency_prefix(("who", "was"))
    """
    prefix = "__".join(prefix)
    prefix += "__"
    items = trie.items(prefix)
    total_freq = 0
    for item in items:
        total_freq += condfreq.get(item[1], 0)
    return total_freq

def find_frequency_trigram(trigram):
    """
    :tuple trigram: trigram of which frequency should be found
    >>> find_frequency_trigram(("who", "was" "Polish"))
    """
    trigram = "__".join(trigram)
    items = trie.items(trigram)
    total_freq = 0
    for item in items:
        total_freq += condfreq.get(item[1], 0)
    return total_freq

def calculate_trigram_probability(trigram):
    """
    :tuple trigram: trigram used to calculate trigram probability
    >>> calculate_trigram_probability(("who", "was" "Polish"))
    """
    bigram_freq = find_frequency_prefix((trigram[0], trigram[1]))
    trigram_freq = find_frequency_trigram(trigram)
    if bigram_freq:
        return trigram_freq/bigram_freq
    else:
        return 0

#print(calculate_trigram_probability(("the", "young", "man")))
