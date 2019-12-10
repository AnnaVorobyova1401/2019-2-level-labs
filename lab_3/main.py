"""
Labour work #3
 Building an own N-gram model
"""

import math
import random

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
        if word in self.storage:
            return self.storage.get(word)

    def get_original_by(self, word_id: int) -> str:
        if word_id in self.storage.keys():
            return self.storage.pop(word_id)

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
                sentence = list(sentence)
            for index, element in enumerate(sentence):
                bi_gram = element, sentence[index + 1]
                self.bg_storage.append(bi_gram)
            for bi_gram in self.bg_storage:
                num = self.bg_storage.count(bi_gram)
                self.gram_frequencies[bi_gram] = num
            return "OK"
        except AssertionError:
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

    def predict_next_sentence(self, prefix: tuple) -> list:
        if not prefix or not isinstance(prefix, tuple):
            return []
        if len(prefix) != self.size - 1:
            return []

        prefix = list(prefix)
        

alf = 'QWERTYUIOPASDFGHJKLZXCVBNM'
signs = '!@#$%^&*,/'


def split_by_sentence(text: str) -> list:
    for elm in text:
        for al in elm:
            if al in signs and al != '.':
                text = text.replace(al, '')

    text = text.replace('\n', " ")
    while "  " in text:
        text = text.replace("  ", " ")
    words = text.split(" ")
    while "" in words:
        words.remove("")

    new_text_1 = []
    start = 0
    for i in range(len(text)):
        if text[i] == '.' and text[i + 1] == ' ' and text[i + 2] in alf:
            new_text_1.append(text[start: i])
            start = i + 3
            print(new_text_1)

    new_text_2 = []
    for elm in new_text_1:
        new_text_2.append('<s> ' + elm + ' </s>')
    print(new_text_2)

    new_text = []
    for elm in new_text_2:
        new_text.append(elm.split(' '))

    return new_text


def encode(storage_instance, corpus) -> list:
    code_sentences = []

    for sentence in corpus:
        code_sentence = []
        for word in sentence:
            code_word = storage_instance.get_id_of(word)
            code_sentence += [code_word]
        code_sentences += [code_sentence]

    return code_sentences


split_by_sentence('''Mary wa$nted, to swim!
                  #However, she was afraid of sharks.''')
