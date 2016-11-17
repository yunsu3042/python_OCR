# 이미지를 False과 True로 이루어진 배열로 바꿔주는 함수. 흰색이면 True 검정색이면 False로 바꿔준다.
## 이미지를 배열로 바꾼후, RGB 세 인자를 적절한 계산을 통해.
#np.set_printoptions는 numpy리스트를 생략하지 않고 끝까지 출력하라는 명령.
import numpy as np
def image_into_true_or_false_array(img_url,size):
    np.set_printoptions(threshold=np.inf)
    img = Image.open(img_url).convert("RGB")
    img.thumbnail(size)
    width,height = img.size
    img_arr = np.array(img).reshape(height,width,3)
    true_or_false_arr = np.zeros((height,width),dtype=np.bool)
    # 이미지 배열을 흑백화 하는 과정 img = PIL.Image.open("foo.jpg").convert("L")로도 가능하지만 나중에 커스터마이징을 위해 짰음.
    for x in range(0,height):
        for y in range(0,width):
            a = img_arr[x,y,0]
            b = img_arr[x,y,1]
            c = img_arr[x,y,2]
            det = a*0.2989 + b*0.5870 + c*0.1140
            if det >150:
                color = 1
            else:
                color = 0
            true_or_false_arr[x,y] = color

    return true_or_false_arr

