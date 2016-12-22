__all__ = ('rec_spread', 'is_circle', 'rec_spread_4d', 'is_circle_4d')

# 상하좌우 대각선
def rec_spread(arr, start_h, start_w):
    possibles = []
    height, width = arr.shape
    go_by_h = start_h
    go_by_w = start_w

    if arr[go_by_h][go_by_w] == 1:
        return None
    if go_by_h - 1 >= 0 and go_by_w - 1 >= 0:
        possibles.append((go_by_h - 1, go_by_w - 1))
    if go_by_h - 1 >= 0 and go_by_w + 0 >= 0 and go_by_w + 0 <= width - 1:
        possibles.append((go_by_h - 1, go_by_w + 0))
    if go_by_h - 1 >= 0 and go_by_w + 1 <= width - 1:
        possibles.append((go_by_h - 1, go_by_w + 1))

    if go_by_h >= 0 and go_by_h <= height - 1 and go_by_w - 1 >= 0:
        possibles.append((go_by_h, go_by_w - 1))
    if go_by_h >= 0 and go_by_h <= height - 1 and go_by_w + 0 >= 0 and go_by_w + 0 <= width - 1:
        possibles.append((go_by_h, go_by_w))
    if go_by_h >= 0 and go_by_h <= height - 1 and go_by_w + 1 <= width - 1:
        possibles.append((go_by_h, go_by_w + 1))

    if go_by_h + 1 <= height - 1 and go_by_w - 1 >= 0:
        possibles.append((go_by_h + 1, go_by_w - 1))
    if go_by_h + 1 <= height - 1 and go_by_w + 0 >= 0 and go_by_w + 0 <= width - 1:
        possibles.append((go_by_h + 1, go_by_w + 0))
    if go_by_h + 1 <= height - 1 and go_by_w + 1 <= width - 1:
        possibles.append((go_by_h + 1, go_by_w + 1))

    if not possibles:
        return None
    check = 0
    for possible in possibles:
        if arr[possible[0]][possible[1]] == 0:
            arr[possible[0]][possible[1]] = 2
        else:
            check += 1
    if check == len(possibles):
        return None

    for possible in possibles:
        rec_spread(arr, possible[0], possible[1])


def is_circle(arr):
    for y in range(arr.shape[1] - 1):
        rec_spread(arr, 0, y)
        rec_spread(arr, arr.shape[0] - 1, y)
    for x in range(arr.shape[0] - 1):
        rec_spread(arr, x, 0)
        rec_spread(arr, x, arr.shape[1] - 1)

    if 0 in arr:
        return True
    return False

# 상하좌우
def rec_spread_4d(arr, start_h, start_w):
    possibles = []
    height, width = arr.shape
    go_by_h = start_h
    go_by_w = start_w
    if arr[go_by_h][go_by_w] == 1:
        return None

    if go_by_h - 1 >= 0 and go_by_w + 0 >= 0 and go_by_w + 0 <= width - 1:
        possibles.append((go_by_h - 1, go_by_w + 0))
    if go_by_h >= 0 and go_by_h <= height - 1 and go_by_w - 1 >= 0:
        possibles.append((go_by_h, go_by_w - 1))
    if go_by_h >= 0 and go_by_h <= height - 1 and go_by_w + 0 >= 0 and go_by_w + 0 <= width - 1:
        possibles.append((go_by_h, go_by_w))
    if go_by_h >= 0 and go_by_h <= height - 1 and go_by_w + 1 <= width - 1:
        possibles.append((go_by_h, go_by_w + 1))
    if go_by_h + 1 <= height - 1 and go_by_w + 0 >= 0 and go_by_w + 0 <= width - 1:
        possibles.append((go_by_h + 1, go_by_w + 0))

    if not possibles:
        return None
    check = 0
    for possible in possibles:
        if arr[possible[0]][possible[1]] == 0:
            arr[possible[0]][possible[1]] = 2
        else:
            check += 1
    if check == len(possibles):
        return None

    for possible in possibles:
        rec_spread_4d(arr, possible[0], possible[1])


def is_circle_4d(arr):
    for y in range(arr.shape[1] - 1):
        rec_spread_4d(arr, 0, y)
        rec_spread_4d(arr, arr.shape[0] - 1, y)
    for x in range(arr.shape[0] - 1):
        rec_spread_4d(arr, x, 0)
        rec_spread_4d(arr, x, arr.shape[1] - 1)

    if 0 in arr:
        return True
    return False