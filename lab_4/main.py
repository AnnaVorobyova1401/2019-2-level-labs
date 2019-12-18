import math


REFERENCE_TEXTS = []
if __name__ == '__main__':
    texts = ['5_7.txt', '15_2.txt', '10547_3.txt', '12230_7.txt']
    for text in texts:
        with open(text, 'r') as f:
            REFERENCE_TEXTS.append(f.read())

bad_signs = '!@#$%^&*()?/|№;%:,'


def clean_tokenize_corpus(texts: list) -> list:
    if not texts:
        return []

    clean_token_corpus = []
    for my_text in texts:
        if not my_text or not isinstance(my_text, str):
            continue

        text_1 = my_text.lower()
        text = text_1.replace('.', '')
        for elm in text:
            if elm in bad_signs:
                text = text.replace(elm, "")

        text = text.replace("\n", " ")
        while "  " in text:
            text = text.replace("  ", " ")

        new_text = ""
        for element in text:
            if element.isalpha() or element == ' ' or element == '.':
                new_text += element
        sentences = new_text.split('.')

        for sent in sentences:
            if sent != '':
                sent = sent.split()
        clean_token_corpus.append(sent)
    return clean_token_corpus


class TfIdfCalculator:
    def __init__(self, corpus):
        self.corpus = corpus
        self.tf_values = []
        self.idf_values = {}
        self.tf_idf_values = []

    def calculate_tf(self):
        if self.corpus:
            frequencies = {}
            for sentence in self.corpus:
                if not sentence:
                    continue

                for word in sentence:
                    if not isinstance(word, str):
                        continue
                    if word in frequencies:
                        value = frequencies[word]
                        frequencies[word] = (value + 1) / len(sentence)
                    else:
                        frequencies[word] = 1 / len(sentence)
                self.tf_values.append(frequencies)
                frequencies = {}
        return self.tf_values

    def calculate_idf(self):          # НЕ ПРОХОДИТ 1 ТЕСТ
        if self.corpus:
            doc_num = len(self.corpus)
            word_in_doc = []
            word_num = 0

            for ev_text in self.corpus:
                if ev_text is None:
                    continue

                for word in ev_text:
                    if not isinstance(word, str):
                        continue
                    if word not in word_in_doc:
                        word_in_doc.append(word)

                for word in word_in_doc:
                    for my_text in self.corpus:
                        if word in my_text:
                            word_num += 1

                    if word_num:
                        self.idf_values[word] = math.log(doc_num / word_num)
        return self.idf_values

    def calculate(self):
        if self.idf_values and self.tf_values:
            for ev_text in self.corpus:
                for word in ev_text:
                    tf_idf_calc = self.tf_values[word] * self.idf_values[word]
                self.tf_idf_values[word] = tf_idf_calc
        return self.tf_idf_values

    def report_on(self, word, document_index):
        if not self.tf_idf_values or document_index >= len(self.tf_idf_values):
            return ()
        tf_idf_dict = self.tf_idf_values[document_index]
        if word not in tf_idf_dict:
            return ()
        list_tf_idf = sorted(tf_idf_dict, key=tf_idf_dict.__getitem__, reverse=True)
        return tf_idf_dict.get(word.lower()), list_tf_idf.index(word.lower())
   
