__all__ = ('check_letter_pixels', 'check_left_side', 'compare_vertical', 'compare_horizontal',
           'compare_diagonal_from_left_top', 'compare_diagonal_from_left_bottom')


def check_letter_pixels(array):
    count = 0
    height, width = array.shape
    for x in range(height):
        for y in range(width):
            if array[x][y] == 1:
                count += 1
    return count


def check_left_side(array):
    count = 0
    height, width = array.shape
    check = width % 2
    if check == 0:
        for x in range(height):
            for y in range(width // 2):
                if array[x][y] == 1:
                    count += 1
    if check == 1:
        for x in range(height):
            for y in range((width - 1) // 2):
                if array[x][y] == 1:
                    count += 1
            if array[x][(width - 1) // 2] == 1:
                count += 0.5
    a = check_letter_pixels(array)
    percent = count / a
    return percent


def compare_vertical(array):
    height, width = array.shape
    count = 0
    if width % 2 == 0:
        limit = width // 2
        for x in range(height):
            for y in range(limit):
                if array[x][y] == 1 and array[x][width - 1 - y] == 1:
                    count += 2
    if width % 2 != 0:
        limit = (width - 1) // 2
        for x in range(height):
            for y in range(limit):
                if array[x][y] == 1 and array[x][width - 1 - y] == 1:
                    count += 2
            if array[x][limit] == 1:
                count += 1
    a = check_letter_pixels(array)
    percent = count / a
    return percent


def compare_horizontal(array):
    height, width = array.shape
    count = 0
    if height % 2 == 0:
        limit = height // 2
        for x in range(limit):
            for y in range(width):
                if array[x][y] == 1 and array[height - x - 1][y] == 1:
                    count += 2
    if width % 2 != 0:
        limit = (height - 1) // 2
        for x in range(limit):
            for y in range(width):
                if array[x][y] == 1 and array[height - x - 1][y] == 1:
                    count += 2
        for y in range(width):
            if array[limit][y] == 1:
                count += 1
    a = check_letter_pixels(array)
    percent = count / a
    return percent


# 대각선의 개수까지 포함.
def compare_diagonal_from_left_bottom(array):
    count = 0
    height, width = array.shape
    for x in range(height):
        for y in range(width):
            if array[x][y] == 1 and array[height - y - 1][width - x - 1] == 1:
                count += 1

    a = check_letter_pixels(array)
    percent = count / a
    return percent


def compare_diagonal_from_left_top(array):
    count = 0
    height, width = array.shape
    for y in range(width):
        for x in range(height):
            if array[x][y] == 1 and array[y][x] == 1:
                count += 1

    a = check_letter_pixels(array)
    percent = count / a
    return percent

