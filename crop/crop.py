from PIL import Image
from matplotlib import pyplot as plt

from .cordinate import x_cordinate, y_cordinate

__all__ = ('x_crop', 'y_crop', 'search', 'crop_alphabet', )


# 이미지 내의 한줄로 구성된 문자들이 있을 경우 문자들을 구분해서 각각 저장할 수 있으며, 리스트로 각 알파뱃을 저장해서 반환한다.
def x_crop(url):
    cropped = []
    img = Image.open(url)
    width, height = img.size
    cropby = x_cordinate(url=url)
    for i in range(len(cropby[0])):
        temp = img.crop((cropby[0][i], 0, cropby[1][i], height))
        cropped.append(temp)
    return cropped


# 이미지에 여러 줄로 글들이 구성되어 있을 때 줄들을 구분해서 각각 이미지화한다. 즉 각각의 줄을 이미지화해서 리스트로 반환한다.
def y_crop(url):
    cropped = []
    img = Image.open(url)
    width, height = img.size
    cropby = y_cordinate(url)
    for i in range(len(cropby[0])):
        temp = img.crop((0, cropby[0][i], width, cropby[1][i]))
        cropped.append(temp)
    return cropped


def search(dirname):
    import os
    splitnames = []
    filenames = os.listdir(dirname)
    for filename in filenames:
        splitnames.append(int(os.path.splitext(filename)[0][1:]))
    return sorted(splitnames)

    
#드디어 이미지 크롭!!
# url을 받아, y_crop을 통해 이미지에 있는 글로 이루어진 단락을 각각의 줄들로 분리한다.
# x_cordinate_img 함수를 사용해, 각 줄에 대해 알파뱃들 사이를 채우고 있는 흰 여백의 x 축 좌표를 구한다.(함수이름에 신경써야한다.)
# crop한 알파뱃을 저장하고 싶은 위치를 설정한다. 여기서는 (/Users/yunsu/Destop/python_ocr/<alphabet>)
# temp.show()가 이미지를 보여주면, 사용자는 알파뱃을 대소문자를 구분해서 값을 입력하면, 입력받은 알파뱃을 폴더명이 없다면 생성해준다.
# 알파뱃 이미지를 폴더 내에 저장할 때는, 나중에 다른 알파뱃 이미지들과 섞였을 때 구분할 수 있도록, 알파뱃과 숫자값을 결합한 "A11"의 형식으로 저장한다.
# 숫자를 차곡차곡 지정하기 위해서 폴더내에 이미 존재했던 파일들을 search함수를 통해 가장 높은 숫자값을 구한후 그 값에 1을 더한 값을 숫자값으로 저장한다.
# url을 받아, y_crop을 통해 이미지에 있는 글로 이루어진 단락을 각각의 줄들로 분리한다.
# x_cordinate_img 함수를 사용해, 각 줄에 대해 알파뱃들 사이를 채우고 있는 흰 여백의 x 축 좌표를 구한다.(함수이름에 신경써야한다.)
# crop한 알파뱃을 저장하고 싶은 위치를 설정한다. 여기서는 (/Users/yunsu/Destop/python_ocr/<alphabet>)
# temp.show()가 이미지를 보여주면, 사용자는 알파뱃을 대소문자를 구분해서 값을 입력하면, 입력받은 알파뱃을 폴더명이 없다면 생성해준다.
# 알파뱃 이미지를 폴더 내에 저장할 때는, 나중에 다른 알파뱃 이미지들과 섞였을 때 구분할 수 있도록, 알파뱃과 숫자값을 결합한 "A11"의 형식으로 저장한다.
# 숫자를 차곡차곡 지정하기 위해서 폴더내에 이미 존재했던 파일들을 search함수를 통해 가장 높은 숫자값을 구한후 그 값에 1을 더한 값을 숫자값으로 저장한다.
def crop_alphabet(url):
    import os
    lines = y_crop(url)
    for img in lines:
        width, height = img.size
        cropped = []
        cropby = x_cordinate(img=img)
        for i in range(len(cropby[0])):
            temp = img.crop((cropby[0][i], 0, cropby[1][i], height))
            plt.axis("off")
            plt.imshow(temp)
            plt.show()
            alphabet = input("눈에 보이는 알파뱃을 대소문자 가려서 입력해주세요")
            if alphabet == 'exit':
                return "이만 마칩니다."
            if alphabet.istitle():
                directory = "/Users/yunsu/Desktop/python_ocr/alphabet/Upper/{}/".format(alphabet)
            else:
                directory = "/Users/yunsu/Desktop/python_ocr/alphabet/Lower/{}/".format(alphabet)
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                num = search(directory)[-1]
                temp.save(directory + "{alphabet}{number}.jpg".format(alphabet=alphabet, number=num+1))
            except IndexError:
                temp.save(directory + "{alphabet}{number}.jpg".format(alphabet=alphabet, number=0))
            cropped.append(temp)
    return cropped