import math


REFERENCE_TEXTS = []


def clean_tokenize_corpus(texts: list) -> list:
    tokenized_corpus = []
    if not isinstance(texts, list):
        return tokenized_corpus
    for text_sample in texts:
        if not isinstance(text_sample, str):
            continue
        temp_text = text_sample
        while '<br />' in temp_text:
            temp_text = temp_text.replace('<br />', ' ')
        temp_list = temp_text.split()
        for word_id, word in enumerate(temp_list):
            if not word.isalpha():
                temp_list[word_id] = ''.join([letter for letter in word if letter.isalpha()])
            if not temp_list[word_id].islower():
                temp_list[word_id] = temp_list[word_id].lower()
        while '' in temp_list:
            temp_list.remove('')
        tokenized_corpus.append(temp_list)
    return tokenized_corpus


class TfIdfCalculator:
    def __init__(self, corpus):
        self.corpus = corpus
        self.tf_values = []
        self.idf_values = {}
        self.tf_idf_values = []
        self.file_names = ['5_7.txt', '15_2.txt', '10547_3.txt', '12230_7.txt', 'test.txt']

    def calculate_tf(self):
        if isinstance(self.corpus, list):
            for document in self.corpus:
                if not isinstance(document, list):
                    continue
                total_words = 0
                frequencies = {}
                for word in document:
                    if not isinstance(word, str):
                        continue
                    frequencies[word] = frequencies.get(word, 0) + 1
                    total_words += 1
                for each_word in frequencies:
                    frequencies[each_word] /= total_words
                self.tf_values.append(frequencies)

    def calculate_idf(self):
        if isinstance(self.corpus, list):
            total_documents = 0
            docs_where_present = {}
            for document in self.corpus:
                if not isinstance(document, list):
                    continue
                total_documents += 1
                for word_occurrence in document:
                    if not isinstance(word_occurrence, str):
                        continue
                    if word_occurrence in docs_where_present:
                        continue
                    for doc in self.corpus:
                        if isinstance(doc, list) and word_occurrence in doc:
                            docs_where_present[word_occurrence] = docs_where_present.get(word_occurrence, 0) + 1
            for word in docs_where_present:
                self.idf_values[word] = math.log(total_documents / docs_where_present[word])

    def calculate(self):
        if isinstance(self.tf_values, list) and self.tf_values:
            if isinstance(self.idf_values, dict) and self.idf_values:
                for document in self.tf_values:
                    tf_idf_for_one_doc = {}
                    for word in document:
                        tf_idf_for_one_doc[word] = document[word] * self.idf_values[word]
                    self.tf_idf_values.append(tf_idf_for_one_doc)

    def report_on(self, word, document_index):
        result = ()
        if not isinstance(word, str) or not isinstance(document_index, int):
            return result
        if not self.tf_idf_values or not isinstance(self.tf_idf_values, list):
            return result
        if document_index > len(self.tf_idf_values) or document_index < 0:
            return result
        if word not in self.tf_idf_values[document_index]:
            return result
        if not word.isalpha() or not word.islower():
            return result
        sorted_by_tf_idf = sorted(self.tf_idf_values[document_index],
                                  key=lambda x: self.tf_idf_values[document_index][x],
                                  reverse=True)
        max_tf_idf_value = self.tf_idf_values[document_index][sorted_by_tf_idf[0]]
        rating = 0
        for one_word in sorted_by_tf_idf:
            if self.tf_idf_values[document_index][one_word] < max_tf_idf_value:
                max_tf_idf_value = self.tf_idf_values[document_index][one_word]
                rating += 1
            if one_word == word:
                return max_tf_idf_value, rating
        return ()

    def dump_report_csv(self):
        report_file = open('report.csv', 'w')
        if self.tf_values and self.idf_values and self.tf_idf_values:
            table_title = ['word']
            for document in self.file_names:
                table_title.append('tf_{}'.format(document))
            table_title.append('idf')
            for document in self.file_names:
                table_title.append('tf_idf_{}'.format(document))
            report_file.write(','.join(table_title) + '\n')
            for word in self.idf_values:
                new_entry = [word]
                for document in self.tf_values:
                    if word in document:
                        new_entry.append(str(round(document[word], 6)))
                    else:
                        new_entry.append('0')
                new_entry.append(str(round(self.idf_values[word], 6)))
                for document in self.tf_idf_values:
                    if word in document:
                        new_entry.append(str(round(document[word], 6)))
                    else:
                        new_entry.append('0')
                report_file.write(','.join(new_entry) + '\n')

    def cosine_distance(self, index_text_1: int, index_text_2: int) -> float:
        cos_value = 1000
        if not isinstance(self.tf_idf_values, list) or not self.tf_idf_values \
                or not isinstance(index_text_1, int) or not isinstance(index_text_2, int):
            return cos_value
        if index_text_1 < 0 or index_text_2 < 0 \
            or index_text_1 > len(self.file_names) \
                or index_text_2 > len(self.file_names):
            return cos_value
        words = []
        for word in self.corpus[index_text_1]:
            if word not in words:
                words.append(word)
        for word in self.corpus[index_text_2]:
            if word not in words:
                words.append(word)
        vector_text_1 = [0 for _each_word in words]
        vector_text_2 = [0 for _each_word in words]
        for word_index, word in enumerate(words):
            if word in self.corpus[index_text_1]:
                vector_text_1[word_index] = self.tf_idf_values[index_text_1][word]
            if word in self.corpus[index_text_2]:
                vector_text_2[word_index] = self.tf_idf_values[index_text_2][word]
        dot_product = 0
        for word_index, word_value in enumerate(vector_text_1):
            dot_product += word_value * vector_text_2[word_index]
        scalar_1 = 0
        for word_value in vector_text_1:
            scalar_1 += word_value * word_value
        scalar_2 = 0
        for word_value in vector_text_2:
            scalar_2 += word_value * word_value
        cos_value = dot_product / (math.sqrt(scalar_1) * math.sqrt(scalar_2))
        return cos_value


if __name__ == '__main__':
    texts = ['5_7.txt', '15_2.txt', '10547_3.txt', '12230_7.txt', 'test.txt']
    for text in texts:
        with open(text, 'r') as f:
            REFERENCE_TEXTS.append(f.read())
    # scenario to check your work
    test_texts = clean_tokenize_corpus(REFERENCE_TEXTS)
    tf_idf = TfIdfCalculator(test_texts)
    tf_idf.calculate_tf()
    tf_idf.calculate_idf()
    tf_idf.calculate()
    print(tf_idf.report_on('good', 0))
    print(tf_idf.report_on('and', 1))
