__all__ = ('y_high', 'y_low', 'x_left', 'x_right', 'make_center', 'delete_col', 'delete_row', 'add_col', 'add_row',
           'make_min_matrix', 'make_square_matrix')
import numpy as np


def y_high(arr):
    height, width = arr.shape
    for y in range(height):
        for x in range(width):
            if arr[y][x] == 1:
                return y


def y_low(arr):
    height, width = arr.shape
    for y in range(height)[::-1]:
        for x in range(width):
            if arr[y][x] == 1:
                return y


def x_left(arr):
    height, width = arr.shape
    for x in range(width):
        for y in range(height):
            if arr[y][x] == 1:
                return x


def x_right(arr):
    height, width = arr.shape
    for x in range(width)[::-1]:
        for y in range(height):
            if arr[y][x] == 1:
                return x


# 1 만약 가로 길이가 짝수이면 중간 좌표는 x.5이고 가로 길이가 홀수이면 중간 자표는 int이다.
def make_center(arr):
    y2 = y_high(arr)
    y1 = y_low(arr)
    x1 = x_left(arr)
    x2 = x_right(arr)
    return (x1 + x2)/2, (y1 + y2)/2


def delete_col(arr, where='right', n=1):
    for __ in range(n):
        height, width = arr.shape
        if where == 'right':
            arr = np.delete(arr, width-1, 1)
        elif where == 'left':
            arr = np.delete(arr, 0, 1)
    return arr


def delete_row(arr, where='high', n=1):
    for __ in range(n):
        height, width = arr.shape
        if where == 'high':
            arr = np.delete(arr, 0, 0)
        elif where == 'low':
            arr = np.delete(arr, height-1, 0)
    return arr


#2.2 row, col 추가 함수
def add_col(arr, where='right', n=1):
    for __ in range(n):
        height, width = arr.shape
        if where == 'right':
            arr = np.insert(arr, width, 0, axis=1)
        elif where == 'left':
            arr = np.insert(arr, 0, 0, axis=1)
    return arr


def add_row(arr, where='high',n=1):
    for __ in range(n):
        height, width = arr.shape
        if where == 'high':
            arr = np.insert(arr, 0, 0, axis=0)
        elif where == 'low':
            arr = np.insert(arr, height, 0, axis=0)
    return arr


# 2.1 최소 매트릭스 만들기.
def make_min_matrix(arr):
    height, width = arr.shape
    rm_col_left = x_left(arr)
    rm_col_right = width-1 - x_right(arr)
    rm_row_high = y_high(arr)
    rm_row_low = height-1 - y_low(arr)

    arr = delete_col(arr, where='right', n=rm_col_right)
    arr = delete_col(arr, where='left', n=rm_col_left)
    arr = delete_row(arr, where='high', n=rm_row_high)
    arr = delete_row(arr, where='low', n=rm_row_low)
    return arr


# 최소 매트릭스로 정 사각 matrix만들어주기. ()
def make_square_matrix(arr):
    arr = make_min_matrix(arr)
    row, col = arr.shape
    if col - row >= 1:
        m = col - row
        if m % 2 == 0:
            arr = add_row(arr, where='high', n=(m//2))
            arr = add_row(arr, where='low', n=(m//2))
        if m % 2 != 0:
            arr = add_row(arr, where='high', n=(m//2)+1)
            arr = add_row(arr, where='low', n=(m//2))
    if row - col >= 1:
        m = row - col
        if m % 2 == 0:
            arr = add_col(arr, where='right', n=(m//2))
            arr = add_col(arr, where='left', n=(m//2))
        if m % 2 != 0:
            arr = add_col(arr, where='right', n=(m//2)+1)
            arr = add_col(arr, where='left', n=(m//2))
    return arr
