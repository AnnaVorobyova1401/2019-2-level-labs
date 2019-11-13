"""
Labour work #2. Levenshtein distance.
"""


def generate_edit_matrix(num_rows: int, num_cols: int) -> list:
    """
    Generates a matrix
    :param num_rows: number of rows, length of the original word + 1
    :param num_cols: number of columns, length of the target word + 1
    :return: generated matrix
    """
    if not isinstance(num_rows, int):
        num_rows = 0
    if not isinstance(num_cols, int):
        num_cols = 0
    if num_rows < 1 or num_cols < 1:
        return []
    return [[0] * num_cols for row in range(num_rows)]


def initialize_edit_matrix(edit_matrix: tuple, add_weight: int, remove_weight: int) -> list:
    """
    Initializes the matrix, fills in the first row & column
    :param edit_matrix: the generalized matrix
    :param add_weight: weight of the addition operation, user-defined
    :param remove_weight: weight of the removal operation, user-defined
    :return: initialized matrix
    """
    if not isinstance(add_weight, int):
        add_weight = 0
    if not isinstance(remove_weight, int):
        remove_weight = 0
    result_matrix = list(edit_matrix)
    if result_matrix == [] or result_matrix[0] == []:
        return result_matrix
    result_matrix[0][0] = 0
    for i in range(1, len(result_matrix)):
        result_matrix[i][0] = result_matrix[i - 1][0] + remove_weight
    for j in range(1, len(result_matrix[0])):
        result_matrix[0][j] = result_matrix[0][j - 1] + add_weight
    return result_matrix


def minimum_value(numbers: tuple) -> int:
    """
    Checks if the numbers in the tuple are of int type and chooses the minimal one
    :param numbers: a tuple of numbers
    :return: the minimal number
    """
    numbers = list(numbers)
    for i, num in enumerate(numbers):
        if not isinstance(num, int):
            numbers[i] = -1
    return min(numbers)


def fill_edit_matrix(edit_matrix: tuple,
                     add_weight: int,
                     remove_weight: int,
                     substitute_weight: int,
                     original_word: str,
                     target_word: str) -> list:
    """
    Fills the matrix according to the given operation weights
    :param edit_matrix: the initialized matrix
    :param add_weight:
    :param remove_weight:
    :param substitute_weight:
    :param original_word:
    :param target_word:
    :return: filled matrix
    """
    result_matrix = list(edit_matrix)
    if not isinstance(original_word, str) or not isinstance(target_word, str):
        return result_matrix
    if not isinstance(add_weight, int) or add_weight < 0:
        return result_matrix
    if not isinstance(remove_weight, int) or remove_weight < 0:
        return result_matrix
    if not isinstance(substitute_weight, int) or substitute_weight < 0:
        return result_matrix
    if len(result_matrix) != (len(original_word) + 1) or len(result_matrix[0]) != (len(target_word) + 1):
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
    """
    Counts the Levenshtein distance for two given words
    :param original_word: user-defined
    :param target_word: user-defined
    :param add_weight: user-defined
    :param remove_weight: user-defined
    :param substitute_weight: user-defined
    :return: the distance
    """
    if not isinstance(original_word, str) or not isinstance(target_word, str):
        return -1
    if minimum_value((add_weight, remove_weight, substitute_weight)) < 0:
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
    # save_to_csv(tuple(matrix), path_to_csv_file)
    return matrix[i][j]


def save_to_csv(edit_matrix: tuple, path_to_file: str) -> None:
    """
    Saves a matrix in csv format
    :param edit_matrix:
    :param path_to_file:
    :return:
    """
    with open(path_to_file, 'w') as f_out:
        for row in edit_matrix:
            f_out.write(','.join([str(element) for element in row]) + '\n')


def load_from_csv(path_to_file: str) -> list:
    """
    Takes a matrix from a csv file
    :param path_to_file:
    :return: the matrix
    """
    matrix = []
    with open(path_to_file, 'r') as f_in:
        row = f_in.readline()
        while row != '':
            matrix += [[int(element) for element in row.split(',')]]
            row = f_in.readline()
    return matrix


def describe_edits(edit_matrix: tuple,
                   original_word: str,
                   target_word: str,
                   add_weight: int,
                   remove_weight: int,
                   substitute_weight: int) -> list:
    """
    Gives an interpretation of editing operations
    :param edit_matrix: the filled matrix for two words
    :param original_word:
    :param target_word:
    :param add_weight:
    :param remove_weight:
    :param substitute_weight:
    :return: a list of short descriptions of each operation
    """
    description = []
    if not isinstance(original_word, str) or not isinstance(target_word, str) \
            or len(edit_matrix) != (len(original_word) + 1) \
            or len(edit_matrix[0]) != (len(target_word) + 1):
        return description
    if minimum_value((add_weight, remove_weight, substitute_weight)) < 0:
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
