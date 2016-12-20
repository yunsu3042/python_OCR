import numpy as np
from PIL import Image
__all__ = ('image_into_array', 'image_into_array_byimg', 'image_into_gray_scale_array', 'zero_one_arrray_into_image',)


def image_into_array(img_url, size):
    np.set_printoptions(threshold=np.inf)
    img = Image.open(img_url).convert("RGB")
    img.thumbnail(size)
    width, height = img.size
    img_arr = np.array(img).reshape(height, width, 3)
    zero_or_one_arr = np.zeros((height, width), dtype=np.uint8)
    for x in range(0, height):
        for y in range(0, width):
            a = img_arr[x, y, 0]
            b = img_arr[x, y, 1]
            c = img_arr[x, y, 2]
            det = a*0.2989 + b*0.5870 + c*0.1140
            if det > 200:
                color = 0
            else:
                color = 1
            zero_or_one_arr[x, y] = color
    return zero_or_one_arr


def image_into_array_byimg(img):
    img = img.convert("RGB")
    np.set_printoptions(threshold=np.inf)
    width, height = img.size
    img_arr = np.array(img).reshape(height, width, 3)
    zero_or_one_arr = np.zeros((height, width), dtype=np.uint8)
    for x in range(0, height):
        for y in range(0, width):
            a = img_arr[x, y, 0]
            b = img_arr[x, y, 1]
            c = img_arr[x, y, 2]
            det = a*0.2989 + b*0.5870 + c*0.1140
            if det > 150:
                color = 0
            else:
                color = 1
            zero_or_one_arr[x, y] = color

    return zero_or_one_arr


#사이즈와 이미지 url을 받아, 이미지를 배열로 바꾼후, RGB 세인자를 적절한 계산을 통해 하나의 값으로 바꿔준다.
# 데이터타입이 np.uint8이 아니면 F타입이라는 오류가 난다.
# 이미지를 numpy array로 바꿔주는 함수
def image_into_gray_scale_array(img_url, size):
    img = Image.open(img_url)
    img.thumbnail(size)
    width, height = img.size
    img_array = np.array(img, dtype=np.uint8).reshape(height, width, 3)
    gray_array = np.zeros((height, width), dtype=np.uint8)
    # 이미지 배열을 흑백화 하는 과정 img = PIL.Image.open("foo.jpg").convert("L")
    #와 비슷함
    for x in range(0, height):
        for y in range(0, width):
            a = img_array[x, y, 0]
            b = img_array[x, y, 1]
            c = img_array[x, y, 2]
            gray = a*0.2989 + b*0.5870 + c*0.1140
            if gray > 255:
                gray = 255
            gray_array[x, y] = gray
    return gray_array


def zero_one_arrray_into_image(zero_or_one_arr):
    np.set_printoptions(threshold=np.inf)
    height = len(zero_or_one_arr)
    width = len(zero_or_one_arr[0])
    true_false_arr = np.zeros((height, width), dtype=np.bool)
    for x in range(0, height):
        for y in range(0, width):
            if zero_or_one_arr[x][y] == 0:
                true_false_arr[x][y] = True
            else:
                true_false_arr[x][y] = False

    img = Image.fromarray(true_false_arr, "L")
    return img
