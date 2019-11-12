def generate_edit_matrix(num_rows, num_cols):
    a = []
    m = []
    if type(num_rows) == int and type(num_cols) == int and num_cols is not None and num_rows is not None:
        if num_rows > 0 and num_cols > 0:
            a.append(0)
            for i in range(num_cols):
                a.append(0)
            for i in range(num_rows + 1):
                m.append(a)
            print(m)
            return m

    else:
        return []


def count_list(my_list):
    count = 0
    for elm in my_list:
        count = count + 1
    return count


def initialize_edit_matrix(edit_matrix_1, add_weight, remove_weight):
    if edit_matrix_1 and type(add_weight) == int and type(remove_weight) == int and remove_weight and add_weight:
        length_1 = len(edit_matrix_1[0])
        length_2 = count_list(edit_matrix_1)
        print(length_1, length_2)

        for i in range(length_1):
            edit_matrix_1[0][i] = edit_matrix_1[0][i - 1] + add_weight

        for i in range(length_2):
            edit_matrix_1[i][0] = edit_matrix_1[i - 1][0] + remove_weight
    return edit_matrix_1


def minimum_value(numbers):
    my_min = 999999999999
    for i in numbers:
        if i < my_min:
            my_min = i
    return my_min


def fill_edit_matrix(edit_matrix_2, add_weight, remove_weight, substitute_weight, original_word, target_word):
    numbers = []
    i = 0
    j = 0
    while i < num_rows:
        while j < num_cols:
            for elm in edit_matrix_2:
                numbers.append(edit_matrix_2[i - 1][j] + remove_weight)
                numbers.append(edit_matrix_2[i][j - 1] + add_weight)
                if original_word[i] != target_word[j]:
                    s = substitute_weight
                else:
                    s = 0
                numbers.append(edit_matrix_2[i - 1][j - 1] + s)
                edit_matrix_2[i][j] = minimum_value(numbers)
        i += 1
        j = 0
    return edit_matrix_2


def find_distance(original_word, target_word, add_weight, remove_weight, substitute_weight):
    m = generate_edit_matrix(original_word, target_word)
    m1 = initialize_edit_matrix(m, add_weight, remove_weight)
    m_final = fill_edit_matrix(m1, add_weight, remove_weight, substitute_weight, original_word, target_word)
    return m_final[len(target_word) + 1][len(original_word) + 1]
