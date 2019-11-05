"""
Labour work #2. Levenshtein distance.
"""
word1 = 'death'
word2 = 'life'
add_val = 1
rem_val = 1
sub_val = 2
path_to_csv_file = '../matrix.csv'


def generate_edit_matrix(num_rows: int, num_cols: int) -> list:
    if not isinstance(num_rows, int):
        try:
            num_rows = int(num_rows)
        except TypeError or ValueError:
            num_rows = 0
    if not isinstance(num_cols, int):
        try:
            num_cols = int(num_cols)
        except TypeError or ValueError:
            num_cols = 0
    if num_rows < 1 or num_cols < 1:
        return []
    else:
        return [[0] * num_cols for row in range(num_rows)]


def initialize_edit_matrix(edit_matrix: tuple, add_weight: int, remove_weight: int) -> list:
    if not isinstance(add_weight, int):
        try:
            add_weight = int(add_weight)
        except TypeError or ValueError:
            add_weight = 0
    if not isinstance(remove_weight, int):
        try:
            remove_weight = int(remove_weight)
        except TypeError or ValueError:
            remove_weight = 0
    result_matrix = list(edit_matrix)
    if result_matrix == [] or result_matrix[] == []:
        return []
    result_matrix[0][0] = 0
    for i in range(1, len(result_matrix)):
        result_matrix[i][0] = result_matrix[i - 1][0] + remove_weight
    for j in range(1, len(result_matrix[0])):
        result_matrix[0][j] = result_matrix[0][j - 1] + add_weight
    return result_matrix


def minimum_value(numbers: tuple) -> int:
    numbers = list(numbers)
    for i in range(len(numbers)):
        if not isinstance(numbers[i], int):
            numbers[i] = -1
    return min(numbers)


def fill_edit_matrix(edit_matrix: tuple,
                     add_weight: int,
                     remove_weight: int,
                     substitute_weight: int,
                     original_word: str,
                     target_word: str) -> list:
    result_matrix = list(edit_matrix)
    if not isinstance(original_word, str) or not isinstance(target_word, str):
        return result_matrix
    elif minimum_value((add_weight, remove_weight, substitute_weight)) < 0:
        return result_matrix
    elif len(result_matrix) != (len(original_word) + 1) or len(result_matrix[0]) != (len(target_word) + 1):
        return result_matrix
    for i in range(1, len(result_matrix)):
        for j in range(1, len(result_matrix[0])):
            if original_word[i - 1] != target_word[j - 1]:
                result_matrix[i][j] = minimum_value((result_matrix[i - 1][j] + remove_weight,
                                                    result_matrix[i][j - 1] + add_weight,
                                                    result_matrix[i - 1][j - 1] + substitute_weight))
            else:
                result_matrix[i][j] = minimum_value((result_matrix[i - 1][j] + remove_weight,
                                                    result_matrix[i][j - 1] + add_weight,
                                                    result_matrix[i - 1][j - 1]))
    return result_matrix


def find_distance(original_word: str,
                  target_word: str,
                  add_weight: int,
                  remove_weight: int,
                  substitute_weight: int) -> int:
    if not isinstance(original_word, str) or not isinstance(target_word, str):
        return -1
    elif minimum_value((add_weight, remove_weight, substitute_weight)) < 0:
        return -1
    i, j = len(original_word), len(target_word)
    matrix = generate_edit_matrix(i + 1, j + 1)
    matrix = initialize_edit_matrix(tuple(matrix),
                                    add_weight,
                                    remove_weight)
    matrix = fill_edit_matrix(tuple(matrix),
                              add_weight,
                              remove_weight,
                              substitute_weight,
                              original_word,
                              target_word)
    save_to_csv(tuple(matrix), path_to_csv_file)
    return matrix[i][j]


def save_to_csv(edit_matrix: tuple, path_to_file: str) -> None:
    with open(path_to_file, 'w') as f:
        for row in edit_matrix:
            f.write(','.join([str(element) for element in row]) + '\n')


def load_from_csv(path_to_file: str) -> list:
    matrix = []
    with open(path_to_file, 'r') as f:
        row = f.readline()
        while row != '':
            matrix += [[int(element) for element in row.split(',')]]
            row = f.readline()
    return matrix


def describe_edits(edit_matrix: tuple,
                   original_word: str,
                   target_word: str,
                   add_weight: int,
                   remove_weight: int,
                   substitute_weight: int) -> list:
    description = []
    if not isinstance(original_word, str) or not isinstance(target_word, str):
        return description
    elif minimum_value((add_weight, remove_weight, substitute_weight)) < 0:
        return description
    elif len(edit_matrix) != (len(original_word) + 1) or len(edit_matrix[0]) != (len(target_word) + 1):
        return description
    i, j = len(original_word), len(target_word)
    while i > 0 and j > 0:
        if original_word[i - 1] != target_word[j - 1]:
            sub_step = edit_matrix[i - 1][j - 1] + substitute_weight
            add_step = edit_matrix[i][j - 1] + add_weight
            rem_step = edit_matrix[i - 1][j] + remove_weight
            min_step = edit_matrix[i][j]
            if sub_step == min_step:
                description = ['substitute {} with {}'.format(original_word[i - 1], target_word[j - 1])] + description
                i -= 1
                j -= 1
            elif add_step == min_step:
                description = ['insert {}'.format(target_word[j - 1])] + description
                j -= 1
            elif rem_step == min_step:
                description = ['remove {}'.format(original_word[i - 1])] + description
                i -= 1
        else:
            i -= 1
            j -= 1
    if i == 0 and j != 0:
        while j > 0:
            description = ['insert {}'.format(target_word[j - 1])] + description
            j -= 1
    elif i != 0 and j == 0:
        while i > 0:
            description = ['remove {}'.format(original_word[i - 1])] + description
            i -= 1
    return description


print(find_distance(word1, word2, add_val, rem_val, sub_val))
# edited_matrix = tuple(load_from_csv(path_to_csv_file))
# print(describe_edits(edited_matrix, word1, word2, add_val, rem_val, sub_val))
