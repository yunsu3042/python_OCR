# 0과 1로만 이루어진 zero_one array를 흑백 이미지로 바꿔주는 함수.
import numpy as np
from PIL import Image
def zero_one_arrray_into_image(zero_or_one_arr):
    np.set_printoptions(threshold=np.inf)
    height = len(zero_or_one_arr)
    width = len(zero_or_one_arr[0])
    true_false_arr = np.zeros((height,width),dtype=np.bool)
    for x in range(0,height):
        for y in range(0,width):
            if zero_or_one_arr[x][y] == 0:
                true_false_arr[x][y] = True
            else:
                true_false_arr[x][y] = False
    
    img = Image.fromarray(true_false_arr,"L")
    return img

