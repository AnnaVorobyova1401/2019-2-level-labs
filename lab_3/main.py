"""
Labour work #3
 Building an own N-gram model
"""

import math

REFERENCE_TEXT = ''
if __name__ == '__main__':
    with open('not_so_big_reference_text.txt', 'r') as f:
        REFERENCE_TEXT = f.read()


class WordStorage:
    def __init__(self):
        self.storage = {}

    def put(self, word: str) -> int:
        if word in self.storage:
            return self.storage[word]
        word_id = 0
        if not isinstance(word, str):
            return -1
        while word_id in self.storage.values():
            word_id += 1
        self.storage[word] = word_id
        return word_id

    def get_id_of(self, word: str) -> int:
        return self.storage.get(word, -1)

    def get_original_by(self, id: int) -> str:
        if id in self.storage.values():
            return [key for key, value in self.storage.items() if value == id][0]
        return 'UNK'

    def from_corpus(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            return
        for word in corpus:
            if isinstance(word, str):
                self.put(word)


class NGramTrie:
    def __init__(self, size=2):
        self.size = size
        self.gram_frequencies = {}
        self.gram_log_probabilities = {}

    def fill_from_sentence(self, sentence: tuple) -> str:
        code_0 = 'OK'
        code_1 = 'ERROR'
        if not isinstance(sentence, tuple):
            return code_1
        if self.size > len(sentence):
            return code_1
        for word_id in sentence:
            if not isinstance(word_id, int):
                return code_1
        i = 0
        while i <= len(sentence) - self.size:
            temp = tuple([sentence[t] for t in range(i, i + self.size)])
            self.gram_frequencies[temp] = self.gram_frequencies.get(temp, 0) + 1
            i += 1
        return code_0

    def calculate_log_probabilities(self):
        for gram in self.gram_frequencies:
            sum = 0
            for g in self.gram_frequencies:
                if gram[:-1] == g[:-1]:
                    sum += self.gram_frequencies[g]
            self.gram_log_probabilities[gram] = math.log(self.gram_frequencies[gram] / sum)

    def predict_next_sentence(self, prefix: tuple) -> list:
        if not isinstance(prefix, tuple):
            return []
        result = list(prefix)
        if len(prefix) != self.size - 1:
            return []
        for word_id in prefix:
            if not isinstance(word_id, int):
                return []
        list_of_prefixes = [(gram[:-1]) for gram in self.gram_log_probabilities]
        history = tuple(prefix)
        added_words = 0
        while history in list_of_prefixes:
            highest_probability = -math.inf
            new_word_id = 'UNK'
            for gram in self.gram_log_probabilities:
                if gram[:-1] == history and self.gram_log_probabilities[gram] > highest_probability:
                    highest_probability = self.gram_log_probabilities[gram]
                    new_word_id = gram[-1]
            if new_word_id != 'UNK':
                result += [new_word_id]
                added_words += 1
                history = tuple(result[added_words:])
        return result


def encode(storage_instance: WordStorage, corpus: tuple) -> list:
    result = []
    for num, sentence in enumerate(corpus):
        result.append([])
        for word in sentence:
            if isinstance(word, str):
                result[num] += [storage_instance.get_id_of(word)]
    return result


def split_by_sentence(text: str) -> list:
    result = []
    if not isinstance(text, str):
        return result
    i = 0
    end_of_text = len(text)
    while i < end_of_text:
        if not text[i].isupper():
            i += 1
            continue
        t = i
        while t < end_of_text and text[t] not in '.!?':
            t += 1
        if t < end_of_text and text[t] in '.!?':
            temp_list = text[i: t].split('\n')
            temp_str = ' '.join(temp_list)
            sentence = [sym for sym in temp_str]
            for num, sym in enumerate(sentence):
                if sym.isupper():
                    sentence[num] = sentence[num].lower()
                if sym in '!"#$%&()**+,./:;<=>?@[\'-]^_`\\\t{|}~':
                    sentence[num] = 'DEL'
                if sym == ' ' and (sentence[num - 1] == ' ' or (num + 1) < len(sentence) and sentence[num + 1] == ' '):
                    sentence[num] = 'DEL'
            num = 0
            while num < len(sentence):
                if sentence[num] == 'DEL':
                    del sentence[num]
                    continue
                num += 1
            result += [['<s>'] + ''.join(sentence).split(' ') + ['</s>']]
            i = t + 1
        else:
            i += 1
    return result
