import collections
import pandas as pd

from .dataization import make_percent_dictionary

__all__ = ('data_dict_to_excel', 'data_dict_to_table', 'img_url_arr_into_excel',)


def data_dict_to_excel(my_dict, file_name):
    import collections
    od = collections.OrderedDict(sorted(my_dict.items()))
    data = {}
    data['alphabet'] = []
    data['left_side_pixels'] = []
    data['verical_coincidence'] = []
    data['horizontal_coincidence'] = []
    data['from_bottom_dia_coincidence'] = []
    data['from_top_dia_coincidence'] = []

    for key, value in od.items():
        data['alphabet'] += [key]
        data['left_side_pixels'] += [value[0]]
        data['verical_coincidence'] += [value[1]]
        data['horizontal_coincidence'] += [value[2]]
        data['from_bottom_dia_coincidence'] += [value[3]]
        data['from_top_dia_coincidence'] += [value[4]]
    table = pd.DataFrame(data, columns=['alphabet', 'left_side_pixels', 'verical_coincidence', 'horizontal_coincidence',
                                        'from_bottom_dia_coincidence', 'from_top_dia_coincidence'])
    writer = pd.ExcelWriter('{}.xlsx'.format(file_name))
    table.to_excel(writer, 'lowercase 1')
    writer.save()


def data_dict_to_table(my_dict):
    import collections
    od = collections.OrderedDict(sorted(my_dict.items()))
    data = {}
    data['alphabet'] = []
    data['left_side_pixels'] = []
    data['verical_coincidence'] = []
    data['horizontal_coincidence'] = []
    data['from_bottom_dia_coincidence'] = []
    data['from_top_dia_coincidence'] = []

    for key, value in od.items():
        data['alphabet'] += [key]
        data['left_side_pixels'] += [value[0]]
        data['verical_coincidence'] += [value[1]]
        data['horizontal_coincidence'] += [value[2]]
        data['from_bottom_dia_coincidence'] += [value[3]]
        data['from_top_dia_coincidence'] += [value[4]]
    table = pd.DataFrame(data, columns=['alphabet', 'left_side_pixels', 'verical_coincidence', 'horizontal_coincidence',
                                       'from_bottom_dia_coincidence', 'from_top_dia_coincidence'])
    return table


def img_url_arr_into_excel(url_arr, size, file_name):
    my_dict = make_percent_dictionary(url_arr, size)
    od = collections.OrderedDict(sorted(my_dict.items()))
    data = {}
    data['alphabet'] = []
    data['left_side_pixels'] = []
    data['vertical_coincidence'] = []
    data['horizontal_coincidence'] = []
    data['from_bottom_dia_coincidence'] = []
    data['from_top_dia_coincidence'] = []

    for key, value in od.items():
        data['alphabet'] += [key]
        data['left_side_pixels'] += [value[0]]
        data['vertical_coincidence'] += [value[1]]
        data['horizontal_coincidence'] += [value[2]]
        data['from_bottom_dia_coincidence'] += [value[3]]
        data['from_top_dia_coincidence'] += [value[4]]
    table = pd.DataFrame(data, columns=['alphabet', 'left_side_pixels', 'verical_coincidence', 'horizontal_coincidence',
                                        'from_bottom_dia_coincidence', 'from_top_dia_coincidence'])
    writer = pd.ExcelWriter('{}.xlsx'.format(file_name))
    table.to_excel(writer, 'lowercase 1')
    writer.save()