# black or white array를 흑백 이미지로 바꿔주는 함수.
import numpy as np
from PIL import Image
def true_or_false_arr_into_image(true_or_false_arr):
    np.set_printoptions(threshold=np.inf)
    img = Image.fromarray(true_or_false_arr,"L")
    return img
