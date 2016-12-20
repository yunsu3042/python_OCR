from .discriminants import check_left_side, compare_diagonal_from_left_bottom,compare_diagonal_from_left_top, \
    compare_horizontal, compare_vertical
from .optimization import make_square_matrix, make_min_matrix
from ..conversion import image_into_array
from ..crop import search
__all__ = ('training', 'image_into_data_list', 'image_into_z_score', 'make_percent_dictionary', )


def training(alphabet):
    try:
        training_data
    except NameError:
        training_data = {}
    numbers = search("/Users/yunsu/Desktop/python_ocr/alphabet/Upper/{}".format(alphabet))
    img_urls = ["/Users/yunsu/Desktop/python_ocr/alphabet/Upper/{}/{}{}.jpg".format(alphabet, alphabet, x) for x in
                numbers]
    ar = []
    br = []
    cr = []
    dr = []
    er = []
    for url in img_urls:
        arr = image_into_array(url, (1000, 1000))
        arr = make_min_matrix(arr)
        arr = make_square_matrix(arr)
        a = round(check_left_side(arr), 8)
        b = round(compare_vertical(arr), 8)
        c = round(compare_horizontal(arr), 8)
        d = round(compare_diagonal_from_left_bottom(arr), 8)
        e = round(compare_diagonal_from_left_top(arr), 8)
        ar.append(a)
        br.append(b)
        cr.append(c)
        dr.append(d)
        er.append(e)
    ar.sort()
    br.sort()
    cr.sort()
    dr.sort()
    er.sort()
    training_data['{}0'.format(alphabet)] = ar
    training_data['{}1'.format(alphabet)] = br
    training_data['{}2'.format(alphabet)] = cr
    training_data['{}3'.format(alphabet)] = dr
    training_data['{}4'.format(alphabet)] = er
    return "{alpha}의 training data가 쌓였습니다. csv 저장 경로를 확인해주세요 ".format(alpha=alphabet)


def image_into_data_list(img_url, size):
    temp_arr = image_into_array(img_url, size)
    arr = make_square_matrix(temp_arr)
    a = check_left_side(arr)
    b = compare_vertical(arr)
    c = compare_horizontal(arr)
    d = compare_diagonal_from_left_bottom(arr)
    e = compare_diagonal_from_left_top(arr)
    return [a, b, c, d, e]


def image_into_z_score(img_url, size):
    arr = image_into_array(img_url, size)

    mean = [0.51207, 0.80240, 0.73793, 0.48870, 0.49100]
    sigma = [0.06285, 0.10405, 0.13713, 0.17777, 0.17747]
    a = (check_left_side(arr)-mean[0])/sigma[0]
    b = (compare_vertical(arr)-mean[1])/sigma[1]
    c = (compare_horizontal(arr)-mean[2])/sigma[2]
    d = (compare_diagonal_from_left_bottom(arr)-mean[3])/sigma[3]
    e = (compare_diagonal_from_left_top(arr)-mean[4])/sigma[4]
    return [a, b, c, d, e]


def make_percent_dictionary(url_list, size):
    result = {}
    for url in url_list:
        key = url.split("/")[-1].split(".")[0]
        values = image_into_data_list(url, size)
        for i, value in enumerate(values):
            values[i] = round(value, 5)
        result[key] = values
    return result