"""
Labour work #2. Levenshtein distance.
"""


def generate_edit_matrix(num_rows, num_cols):
    m = []
    if num_rows.isinstance()  and num_cols.isinstance():
        for i in range(num_rows):
            m.append([])
            for j in range(num_cols):
                m[i].append(0)
    return m


def initialize_edit_matrix(edit_matrix, add_weight, remove_weight):
    if type(edit_matrix) != tuple or not edit_matrix:
        return []
    if not add_weight.isinstance() or not remove_weight.isinstance():
        return list(edit_matrix)
    if edit_matrix.count([]) != 0:
        return list(edit_matrix)

    edit_matrix = list(edit_matrix)
    length_1 = len(edit_matrix[0])
    length_2 = len(edit_matrix)

    for i in range(1, length_1):
        edit_matrix[0][i] = edit_matrix[0][i - 1] + add_weight

    for i in range(1, length_2):
        edit_matrix[i][0] = edit_matrix[i - 1][0] + remove_weight
        
    return edit_matrix


def minimum_value(numbers):
    return min(numbers)


def fill_edit_matrix(edit_matrix, add_weight, remove_weight, substitute_weight, original_word, target_word):
    if type(edit_matrix) != tuple or not edit_matrix:
        return []
    if not add_weight.isinstance() or not remove_weight.isinstance() or not substitute_weight.isinstance():
        return list(edit_matrix)
    if not original_word.isalpha() or not target_word.isalpha() or not original_word or not target_word:
        return list(edit_matrix)
    if edit_matrix.count([]) != 0:
        return list(edit_matrix)

    original_word = ' ' + original_word
    target_word = ' ' + target_word

    for i in range(1, len(original_word)):
        for j in range(1, len(target_word)):
            l_var = edit_matrix[i - 1][j] + remove_weight
            m_var = edit_matrix[i][j - 1] + add_weight
            n_var = edit_matrix[i - 1][j - 1]
            if original_word[i] != target_word[j]:
                n += substitute_weight
            num = (l_var, m_var, n_var)
            minimum = minimum_value(num)
            edit_matrix[i][j] = minimum
    return list(edit_matrix)


def find_distance(original_word, target_word, add_weight, remove_weight, substitute_weight):
    if not add_weight.isinstance() or not remove_weight.isinstance() or not substitute_weight.isinstance():
        return -1
    if not original_word.isalpha() or not target_word.isalpha():
        return -1
    m = generate_edit_matrix(len(original_word) + 1, len(target_word) + 1)
    m1 = initialize_edit_matrix(tuple(m), add_weight, remove_weight)
    m_final = fill_edit_matrix(tuple(m1), add_weight, remove_weight, substitute_weight, original_word, target_word)
    return m_final[-1][-1]


def save_to_csv(edit_martix: list, path_to_file: str):
    if type(edit_martix) != list or not path_to_file.isalpha():
        return None
    with open(path_to_file, 'w') as f:
        for i in edit_martix:
            for elm in i:
                f.write(str(elm) + ',')
            f.write('\n')


def load_from_csv(path_to_file):
    if not path_to_file.isalpha():
        return []
    with open(path_to_file, 'r') as f:
        m = f.readlines()
        mtr = []
        for i in m:
            i = i.replace('\n', '')
            i = i.split(',')
            lis = []
            for elm in i:
                if elm.isdigit():
                    elm = int(elm)
                    lis.append(elm)
            mtr.append(lis)
    return mtr


