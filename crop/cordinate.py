from PIL import Image

from python_ocr import image_into_array
from python_ocr import image_into_array_byimg

__all__ = ('y_cordinate', 'x_cordinate',)


# 문장들을 줄 단위로 자르기 위해서 만든 함수. 각 줄의 시작 좌표리스트(linetop)과 각 줄의 끝 좌표리스트(linebot)
def y_cordinate(url):
    arr = image_into_array(url, (1000, 1000))
    img = Image.open(url)
    width, height = img.size
    linetop = []
    linebot = []
    for h in range(height-1):
        if 1 not in arr[h] and 1 in arr[h+1]:
            linetop.append(h-1)
        elif 1 in arr[h] and 1 not in arr[h+1]:
            linebot.append(h+4)
    return linetop, linebot


# 한줄의 이미지를 한 글자별로 잘라서 시작 리스트와 끝 리스트로 리턴.
def x_cordinate(url=None, img=None):
    wordst = []
    wordnd = []
    if url:
        arr = image_into_array(url, (2000, 2000))
        width, height = len(arr[0]), len(arr[:, [0]])
        for w in range(width-1):
            if 1 not in arr[:, [w]] and 1 in arr[:, [w+1]]:
                wordst.append(w)
            if 1 in arr[:, [w]] and 1 not in arr[:, [w+1]]:
                wordnd.append(w)
        return wordst, wordnd
    elif img:
        arr = image_into_array_byimg(img)
        width, height = img.size
        for w in range(width-1):
            if 1 not in arr[:, [w]] and 1 in arr[:, [w+1]]:
                wordst.append(w-1)
            if 1 in arr[:, [w]] and 1 not in arr[:, [w+1]]:
                wordnd.append(w+4)
        return wordst, wordnd
