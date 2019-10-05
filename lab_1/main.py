"""
Labour work #1
Count frequencies dictionary by the given arbitrary text
"""


user_stop_words = ('of', 'to', 'a', 'and')
# path_to_input_file = '../data.txt'
# path_to_output_file = '../report.txt'
punctuation = '!"#$%&\'()*+,-./:;<=>?@[]\\^_`{|}~'


test_text = '''Knowledge Representation
For the semantic's web-to-function, computers must
have access to structured collections of information
and sets of inference rules that they can use to
conduct automated reasoning. Artificial-intelligence
researchers have studied such systems since long
before the Web was developed. Knowledge
representation, as this technology is often called, is
currently in a state comparable to that of hypertext
before the advent of the Web: it is clearly a good
idea, and some very nice demonstrations exist, but
it has not yet changed the world. It contains the
seeds of important applications, but to realize its full
potential it must be linked into a single global
system.'''


def calculate_frequences(text: str) -> dict:
    """
    Calculates number of times each word appears in the text
    """
    if type(text) != str:
        return {}
    list_of_words = text.split()
    frequencies = {}
    for word in list_of_words:
        symbol_index = -1
        while len(word) > -symbol_index and word[symbol_index] in punctuation:
            symbol_index -= 1
        if symbol_index < -1:
            word = word[:symbol_index + 1]
        symbol_index = 0
        while len(word) > symbol_index and word[symbol_index] in punctuation:
            symbol_index += 1
        word = word[symbol_index:]
        if not word.isalpha():
            if word[-2:] == "'s":
                word = word[:-2]
            elif '-' in word:
                pass
            else:
                continue
        word = word.lower()
        frequencies[word] = frequencies.get(word, 0) + 1
    return frequencies


def filter_stop_words(frequencies: dict, stop_words: tuple) -> dict:
    """
    Removes all stop words from the given frequencies dictionary
    """
    if type(stop_words) != tuple:
        stop_words = ()
    if type(frequencies) != dict:
        return {}
    filtered_dictionary = {}
    for word in frequencies:
        if type(word) != str:
            continue
        if word not in stop_words:
            filtered_dictionary[word] = frequencies[word]
    return filtered_dictionary


def get_top_n(frequencies: dict, top_n: int) -> tuple:
    """
    Takes first N popular words
    """
    if type(top_n) != int:
        try:
            top_n = int(top_n)
        except TypeError:
            top_n = len(frequencies)
    if type(frequencies) != dict:
        return ()
    if top_n > len(frequencies):
        top_n = len(frequencies)
    n_popular = ()
    # ordered_frequencies = sorted(frequencies.items())
    ordered_frequencies = sorted(frequencies.items(), key=lambda word_freq: word_freq[1], reverse=True)
    for word_number in range(top_n):
        n_popular += ordered_frequencies[word_number][0],
    return n_popular


def read_from_file(path_to_file: str, lines_limit: int) -> str:
    if type(lines_limit) != int:
        try:
            lines_limit = int(lines_limit)
        except TypeError:
            lines_limit = 0
    text = ''
    with open(path_to_file, 'r') as file_input:
        for line in range(lines_limit):
            text += file_input.readline()
    return text


def write_to_file(path_to_file: str, content: tuple):
    with open(path_to_file, 'w') as file_output:
        for item in content:
            file_output.write(item + '\n')


# word_frequencies = calculate_frequencies(read_from_file(path_to_input_file, 400))
word_frequencies = calculate_frequences(test_text)
filtered_frequencies = filter_stop_words(word_frequencies, user_stop_words)
result = get_top_n(filtered_frequencies, 10)
# write_to_file(path_to_output_file, result)
print(result)
