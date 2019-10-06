lines_limit = 3
path_to_file = open('data.txt', 'r')


def read_from_file(path_to_file, lines_limit):
    for line in path_to_file:
        if lines_limit == 0:
            break
        else:
            lines_limit -= 1
            return line



text = ''
freq_dict = {}


def calculate_frequences(text):
    freq_dict = {}
    if type(text) is str and text != '':
        text = text.lower()
        for sym in text:
            if sym not in 'abcdefghijklmnopqrstuvwxyz ':
                text = text.replace(sym, "")
        text = text.split(' ')
        for word in text:
            if word == '':
                continue
            elif word in freq_dict:
                freq_dict[word] = freq_dict[word] + 1
            else:
                freq_dict[word] = 1
        return freq_dict
    else:
        return freq_dict


stop_words = ()
frequencies = {}


def filter_stop_words(freq_dict, stop_words):
    if freq_dict == {} or stop_words == () or stop_words is None:
        return freq_dict
    elif freq_dict is None and stop_words is None or freq_dict is None:
        return {}
    if freq_dict != {} and stop_words != ():
        for elm in freq_dict.keys():
             if elm not in stop_words and type(elm) is str:
                frequencies[elm] = freq_dict[elm]
        return frequencies


top_n = 0
toplist = []


def get_top_n(frequencies, top_n):
    toplist = list(frequencies.items())
    toplist.sort(key=lambda i: i[1], reverse=True)
    toplist1 = []
    if top_n > 0:
        for elm in toplist:
            toplist1 += elm
            top_n -= 1
            if top_n == 0:
                break
        for elm in toplist1:
            if type(elm) is int:
                toplist1.remove(elm)
        toplist1 = tuple(toplist1)
        return toplist1
    else:
        return ()





