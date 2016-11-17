##사이즈와 이미지 url을 받아, 이미지를 배열로 바꾼후, RGB 세인자를 적절한 계산을 통해 하나의 값으로 바꿔준다.
# 데이터타입이 np.uint8이 아니면 F타입이라는 오류가 난다.
# 이미지를 numpy array로 바꿔주는 함수
import numpy as np
def image_into_gray_scale_array(img_url,size):
    img = Image.open(img_url)
    img.thumbnail(size)
    width,height = img.size
    img_array = np.array(img,dtype=np.uint8).reshape(height,width,3)
    gray_array = np.zeros((height,width),dtype=np.uint8)
    # 이미지 배열을 흑백화 하는 과정 img = PIL.Image.open("foo.jpg").convert("L")
    #와 비슷함
    for x in range(0,height):
        for y in range(0,width):
            a = img_array[x,y,0]
            b = img_array[x,y,1]
            c = img_array[x,y,2]
            gray = a*0.2989 + b*0.5870 + c*0.1140
            if gray >255:
                gray = 255
            gray_array[x,y] = gray
    return gray_array
        

