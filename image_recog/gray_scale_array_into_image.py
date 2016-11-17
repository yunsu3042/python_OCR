from PIL import Image
import numpy as np

def gray_scale_array_into_image(gray_scale_arr):
    img = Image.fromarray(gray_scale_arr)
    return img
