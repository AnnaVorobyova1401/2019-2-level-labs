Labour work #3
"""
 Building an own N-gram model
"""

import math
import random
from typing import List, Any

REFERENCE_TEXT = ''
if __name__ == '__main__':
    with open('not_so_big_reference_text.txt', 'r') as f:
        REFERENCE_TEXT = f.read()


class WordStorage:

    def __init__(self):
        self.storage = {}

    def put(self, word: str) -> int:
        if word not in self.storage and isinstance(word, str):
            num = random.randint(1, 10000000)
            self.storage[word] = num
            print(num)
            return num

    def get_id_of(self, word: str) -> int:
        identif = self.storage.get(word, -1)
        return identif

    def get_original_by(self, word_id: int) -> str:
        if isinstance(word_id, int):
            for key, value in self.storage.items():
                if word_id == value:
                    return key
        return "UNK"

    def from_corpus(self, corpus: tuple):
        if corpus and isinstance(corpus, tuple):
            for word in corpus:
                num = random.randint(1, 10000000)
                self.storage[word] = num
            return self.storage


class NGramTrie:
    def __init__(self, n):
        self.size = n
        self.gram_frequencies = {}
        self.gram_log_probabilities = {}
        self.bg_storage = []

    def fill_from_sentence(self, sentence: tuple) -> str:
        try:
            if isinstance(sentence, tuple):
                for index, element in enumerate(sentence):
                    bi_gram = (element, sentence[index + 1])
                    if bi_gram in self.gram_frequencies.keys():
                        self.gram_frequencies[bi_gram] += 1
                    else:
                        self.gram_frequencies[bi_gram] = 1
            return "OK"
        except (IndexError, TypeError):
            return "ERROR"

    def calculate_log_probabilities(self):
        for bi_gram, freq in self.gram_frequencies.items():
            sum_of_freq = 0
            for key in list(self.gram_frequencies.keys()):
                if bi_gram[0] == key[0]:
                    sum_of_freq += self.gram_frequencies.get(key)
                    probability = freq / sum_of_freq
                    final_probability = math.log(probability)
                    self.gram_log_probabilities[bi_gram] = final_probability
        return self.gram_log_probabilities

    def predict_next_sentence(self, prefix: tuple) -> list:
        if not prefix or not isinstance(prefix, tuple):
            return []

        if len(prefix) != self.size - 1:
            return []

        prediction = list(prefix)
        probability_lst = []
        for bi_gram in self.gram_log_probabilities.keys():
            if bi_gram[:-1] == prefix:
                probability_lst.append(self.gram_log_probabilities[bi_gram])

        if probability_lst == []:
            return prediction

        next_w = max(probability_lst)
        for word, probability in self.gram_log_probabilities.items():
            if next_w == probability:
                next_w = word[-1]
        prediction.append(next_w)

        new_prefix = prediction[0:]
        prefix = tuple(new_prefix)
        for bi_gram in self.gram_log_probabilities.keys():
            if bi_gram[:-1] == prefix:
                return self.predict_next_sentence(prefix)
            return prediction





def split_by_sentence(text: str) -> list:
    if not text or not isinstance(text, str):
        return []

    text = text.lower()
    for elm in text:
        if elm == "?" or elm == "!":
            text = text.replace(elm, ".")

    text = text.replace("\n", " ")
    while "  " in text:
        text = text.replace("  ", " ")

    new_text = ""
    for element in text:
        if element.isalpha() or element == ' ' or element == '.':
            new_text += element
    sentences = new_text.split('.')

    if '.' not in text:
        return []

    res = []
    for sent in sentences:
        new = ["<s>"]
        if sent != '':
            sent = sent.split()
            for word in sent:
                if word != "":
                    new.append(word)
            new.append("</s>")
            res.append(new)
    return res


def encode(storage_instance, corpus) -> list:
    code_sentences = []

    for sentence in corpus:
        code_sentence = []
        for word in sentence:
            code_word = storage_instance.get_id_of(word)
            code_sentence += [code_word]
        code_sentences += [code_sentence]

    return code_sentences