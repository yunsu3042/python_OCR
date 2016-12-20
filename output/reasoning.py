import pandas as pd
import numpy as np
from ..conversion import image_into_array
from ..data import make_min_matrix, make_square_matrix, check_left_side, compare_diagonal_from_left_bottom, \
    compare_diagonal_from_left_top, compare_horizontal, compare_vertical

__all__ = ('infer', 'infer_')


def infer(z_score, arr):
    result = []
    check = [[] for _ in range(5)]
    for i in range(5):
        for x in range(26):
            if abs(z_score[x][i+1]-arr[i]) <= 0.5:
                check[i].append(x)
    for alphabet in check[0]:
        count = 0
        for i in range(5):
            if alphabet in check[i]:
                count += 1
            else:
                break
        if count == 5:
            result.append(alphabet)

    return z_score[result[0]][0] if len(result) == 1 else check


def infer_(url):
    training_table = pd.read_csv("Upper_data/training_data_raw")
    alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z']
    arr = image_into_array(url, (1000, 1000))
    arr = make_min_matrix(arr)
    arr = make_square_matrix(arr)
    a = round(check_left_side(arr), 8)
    b = round(compare_vertical(arr), 8)
    c = round(compare_horizontal(arr), 8)
    d = round(compare_diagonal_from_left_bottom(arr), 8)
    e = round(compare_diagonal_from_left_top(arr), 8)
    test_data = [a, b, c, d, e]
    result_data = {}
    # method수가 많아지면 range값을 수정해주세요
    for alphabet in alphabets:
        for i in range(5):
            mean = np.mean(training_table['{}{}'.format(alphabet, i)])
            std = np.std(training_table['{}{}'.format(alphabet, i)])
            # result_data['a']의 값을 처음 설정해주는 코드
            try:
                result_data['{}'.format(alphabet)]
            except KeyError:
                result_data['{}'.format(alphabet)] = 0
            # give weight
            if abs((test_data[i] - mean)/std) < 0.3:
                result_data['{}'.format(alphabet)] += 4
            elif abs((test_data[i] - mean)/std) < 0.5:
                result_data['{}'.format(alphabet)] += 3
            elif abs((test_data[i] - mean)/std) < 1.0:
                result_data['{}'.format(alphabet)] += 2
            elif abs((test_data[i] - mean)/std) < 1.5:
                result_data['{}'.format(alphabet)] += 1
    return result_data