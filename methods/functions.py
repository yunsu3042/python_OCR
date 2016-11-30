__all__ = ["image_into_gray_scale_array", "image_into_array", "check_letter_pixels", "check_left_side", "compare_vertical", "compare_horizontal", "compare_diagonal_from_left_bottom", "compare_diagonal_from_left_top", "image_into_data_list", "make_percent_dictionary", "y_high", "y_low", "x_left", "x_right", "make_center", "add_col", "add_row", "make_min_matrix", "make_square_matrix", "image_into_z_score", "zero_one_arrray_into_image","data_dict_to_table", "data_dict_to_excel", "img_url_arr_into_excel","infer"]

#functionList
#자주쓰는 완성 함수
#1. image_into_array(img_url,size), return zero_one_array
#2. make_percent_dictionary(url_arr,size), return {dict} - url 배열을 입력받아,url의 .jpg앞에있는 문자를 key값으로 하고, count5개를 value로 하는 dict
#3. make_min_matrix(arr) return 중심을 맞춘 직사각 matrix
#4. make_square_matrix(arr) return 중심을 맞추고 정사각화한 정사각 matrix
#5. image_into_z_score(img_url, size) 이미지를 z-score  : 함수 만들때마다 커스터마이징 필요.
#6. crop_alphabet(url)




# 잘게 나눠진 기능 함수.

##1. 이미지를 배열로
#a. image_into_gray_scale_array(img_url,size), return gray_array
##2. 배열을 받아, 픽셀을 체크하는 함수.
#a. check_letter_pixels(array), return count
#b. check_left_side(array), return percent
#c. compare_vertical(array), return percent
#d. compare_horizontal(array), return percent
#e. compare_diagonal_from_left_bottom(array), return percent
#f. compare_diagonal_from_left_top(array), return count
#g. image_into_data_list(array), return [a,b,c,d,e] 위의 함수 count 5개를 배열로 리턴해주는 함수(check_letter_pixels 제외)
#h. url_arr_into_dic(array,size), return {dict}_ url 배열을 입력받아,url의 .jpg앞에있는 문자를 key값으로 하고, count5개를 value로 하는 dict
##3. 배열을 받아 중심을 맞춘 배열로 리턴해주기 위해 사용하는 함수.
#a. y_high(arr)
#b. y_low(arr)
#c. x_left(arr)
#d. x_right
#e. make_center
#f. add_col(arr,where='right',n=1)
#g. add_row(arr,where='high',n=1)
##4.배열을 입력받아,url의 .jpg앞에있는 문자를 key값으로 하고, count5개 각각 글자를 이루는 픽셀로 나누어준 퍼세트 데이터를 value로 하는 dict
#배열을 이미지로
#a. zero_one_arrray_into_image(zero_or_one_arr): 아직 완성못함.
# 이미지 크롭
#x_cordinate(url)
#x_cordinate_img(img)
#y_cordinate(url)
#search(dirname)


# 자주쓰는 함수들
##사이즈와 이미지 url을 받아, 이미지를 배열로 바꾼후, RGB 세인자를 적절한 계산을# 통해 하나의 값으로 바꿔준다.
# 데이터타입이 np.uint8이 아니면 F타입이라는 오류가 난다.
# 이미지를 numpy array로 바꿔주는 함수
def image_into_array(img_url,size):
    np.set_printoptions(threshold=np.inf)
    img = Image.open(img_url).convert("RGB")
    img.thumbnail(size)
    width,height = img.size
    img_arr = np.array(img).reshape(height,width,3)
    zero_or_one_arr = np.zeros((height,width),dtype=np.uint8)
    for x in range(0,height):
        for y in range(0,width):
            a = img_arr[x,y,0]
            b = img_arr[x,y,1]
            c = img_arr[x,y,2]
            det = a*0.2989 + b*0.5870 + c*0.1140
            if det >200:
                color = 0
            else:
                color = 1
            zero_or_one_arr[x,y] = color

    return zero_or_one_arr

def make_percent_dictionary(url_list,size):
    result = {}
    for url in url_list:
        key = url.split("/")[-1].split(".")[0]
        values = image_into_data_list(url,size)
        for i,value in enumerate(values):
            values[i] = round(value,5)
        result[key] = values
    return result

def image_into_z_score(img_url,size):
    temp_arr = image_into_array(img_url)
    arr = make_square_matrix(temp_arr)
    mean = [0.51207,0.80240,0.73793,0.48870,0.49100]
    sigma = [0.06285,0.10405,0.13713,0.17777,0.17747]
    a = (check_left_side(arr)-mean[0])/sigma[0]
    b = (compare_vertical(arr)-mean[1])/sigma[1]
    c = (compare_horizontal(arr)-mean[2])/sigma[2]
    d = (compare_diagonal_from_left_bottom(arr)-mean[3])/sigma[3]
    e = (compare_diagonal_from_left_top(arr)-mean[4])/sigma[4]
    return [a,b,c,d,e]


def infer(z_score,arr):
    result = []
    check = [[] for x in range(5)]
    for i in range(5):
        for x in range(26):
            if abs(z_score[x][i+1]-arr[i]) <= 0.5:
                check[i].append(x)
    for alphabet in check[0]:
        count = 0
        for i in range(5):
            if alphabet in check[i]:
                count+=1
            else:
                break
        if count ==5:
            result.append(alphabet)
    
    return z_score[result[0]][0] if len(result)==1 else check
# 2.1 최소 매트릭스 만들기.
def make_min_matrix(arr):
    height = len(arr)
    width = len(arr[0])
    rm_col_left = x_left(arr)
    rm_col_right = width-1 - x_right(arr)
    rm_row_high = y_high(arr)
    rm_row_low = height-1 - y_low(arr)
    
    arr = delete_col(arr,where='right',n=rm_col_right)
    arr = delete_col(arr,where='left',n=rm_col_left)
    arr = delete_row(arr,where='high',n=rm_row_high)
    arr = delete_row(arr,where='low',n=rm_row_low)
    return arr

## 최소 매트릭스로 정 사각 matrix만들어주기. ()
def make_square_matrix(arr):
    arr = make_min_matrix(arr)
    col = len(arr[0])
    row = len(arr)
    if col - row >= 1:
        m = col - row 
        if m %2 ==0:
            arr = add_row(arr,where='high',n=(m//2))
            arr = add_row(arr,where='low',n=(m//2))
        if m % 2 !=0:
            arr = add_row(arr,where='high',n=(m//2)+1)
            arr = add_row(arr,where='low',n=(m//2))
    if row - col >= 1:
        m = row - col
        if m %2 ==0:
            arr = add_col(arr,where='right',n=(m//2))
            arr = add_col(arr,where='left',n=(m//2))
        if m % 2 !=0:
            arr = add_col(arr,where='right',n=(m//2)+1)
            arr = add_col(arr,where='left',n=(m//2))
    return arr

# z 스코어 리스트

z_score = []
alpahbet_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
left_z_score = [-0.921349,1.087498,1.71044,-1.602049,0.559549,0.169555,-0.466434,0.911197,-2.152275,-1.107356,1.488631,-0.192117,0.48747,-0.192117,0.118637,1.249797,-2.066988,0.912788,-0.192117,0.287142,-0.600092,-0.454341,-0.290292,-0.039047,1.099909,0.194059]
vertical_z_score = [0.377394,-1.125417,-1.652881,0.074256,0.839598,-0.285204,0.683896,0.425931,-0.468874,-0.567485,-1.485069,1.89914,-0.081061,1.465577,0.622673,-0.203316,-0.978077,-2.10557,0.02793,-0.301062,-0.401019,0.94859,1.305839,1.714316,-0.483099,-0.247047]
horizontal_z_score = [-0.03356,-0.587709,0.32581,-0.535058,0.418205,-0.077752,-0.435882,0.260981,1.171291,0.684961,0.678616,1.50594,0.628518,-0.007963,1.45533,0.088005,-0.736474,-0.519671,0.555885,0.241729,0.851519,-2.496423,-1.96014,0.789169,-2.264889,-0.000525]
bottom_z_score = [0.62608,-0.31014,1.225288,-0.292477,1.281654,-1.214915,-0.259737,0.453608,-1.444709,-1.60413,0.420081,-1.811535,-0.713812,1.226694,1.997249,0.977662,0.905545,-0.952157,0.536469,-1.393631,0.712597,0.094432,0.133022,0.550363,-0.633595,-0.509895]
top_z_score = [0.567244,0.503851,0.846905,-0.020646,1.182126,-1.165943,-0.273147,0.235799,-1.460141,-1.520097,0.288767,-1.827594,-0.89789,1.131074,2.295867,1.142456,0.104505,-1.358037,0.47455,-1.069529,1.086163,0.26741,0.050692,0.484129,-0.599465,-0.469016]

z_score = [[] for x in range(26)]
for i in range(26):
    z_score[i].append(alpahbet_list[i])
    z_score[i].append(left_z_score[i])
    z_score[i].append(vertical_z_score[i])
    z_score[i].append(horizontal_z_score[i])
    z_score[i].append(bottom_z_score[i])
    z_score[i].append(top_z_score[i])
z_score

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
    
# 이미지를 0과 1로 이루어진 배열로 바꿔주는 함수. 흰색이면 0 검정색이면 1로 바꿔준다.
## 이미지를 배열로 바꾼후, RGB 세 인자를 적절한 계산을 통해 픽셀이 흰색이면0 검정이면 1로 바꿔준다.
#np.set_printoptions는 numpy리스트를 생략하지 않고 끝까지 출력하라는 명령.
import numpy as np
def image_into_array(img_url,size):
    np.set_printoptions(threshold=np.inf)
    img = Image.open(img_url).convert("RGB")
    img.thumbnail(size)
    width,height = img.size
    img_arr = np.array(img).reshape(height,width,3)
    zero_or_one_arr = np.zeros((height,width),dtype=np.uint8)
    for x in range(0,height):
        for y in range(0,width):
            a = img_arr[x,y,0]
            b = img_arr[x,y,1]
            c = img_arr[x,y,2]
            det = a*0.2989 + b*0.5870 + c*0.1140
            if det >200:
                color = 0
            else:
                color = 1
            zero_or_one_arr[x,y] = color

    return zero_or_one_arr

# 이미지 내의 한줄로 구성된 문자들이 있을 경우 문자들을 구분해서 각각 저장할 수 있으며, 리스트로 각 알파뱃을 저장해서 반환한다.
def x_crop(url):
    cropped = []
    img = Image.open(url)
    width,height = img.size
    cropby = x_cordinate(url)
    for i in range(len(cropby)-1):
        temp = img.crop((cropby[i],0,cropby[i+1],height))
#         temp.save("/Users/yunsu/Desktop/python_ocr/phonts/phont3/v_split/h_split/{}.jpg".format(i+12))
        cropped.append(temp)
    return cropped


# 이미지에 여러 줄로 글들이 구성되어 있을 때 줄들을 구분해서 각각 이미지화한다. 즉 각각의 줄을 이미지화해서 리스트로 반환한다.
def y_crop(url):
    cropped = []
    img = Image.open(url)
    width,height = img.size
    cropby = y_cordinate(url)
    for i in range(len(cropby)-1):
        temp = img.crop((0,cropby[i],width,cropby[i+1]))
#         temp.save("/Users/yunsu/Desktop/python_ocr/phonts/phont3/v_split/{}.jpg".format(i))
        cropped.append(temp)
    return cropped

#드디어 이미지 크롭!!
# url을 받아, y_crop을 통해 이미지에 있는 글로 이루어진 단락을 각각의 줄들로 분리한다. 
# x_cordinate_img 함수를 사용해, 각 줄에 대해 알파뱃들 사이를 채우고 있는 흰 여백의 x 축 좌표를 구한다.(함수이름에 신경써야한다.)
# crop한 알파뱃을 저장하고 싶은 위치를 설정한다. 여기서는 (/Users/yunsu/Destop/python_ocr/<alphabet>)
# temp.show()가 이미지를 보여주면, 사용자는 알파뱃을 대소문자를 구분해서 값을 입력하면, 입력받은 알파뱃을 폴더명이 없다면 생성해준다.
# 알파뱃 이미지를 폴더 내에 저장할 때는, 나중에 다른 알파뱃 이미지들과 섞였을 때 구분할 수 있도록, 알파뱃과 숫자값을 결합한 "A11"의 형식으로 저장한다.
# 숫자를 차곡차곡 지정하기 위해서 폴더내에 이미 존재했던 파일들을 search함수를 통해 가장 높은 숫자값을 구한후 그 값에 1을 더한 값을 숫자값으로 저장한다.
def crop_alphabet(url):
    import os
    lines = xycrop(url)
    for img in lines:
        width,height = img.size
        cropped = []
        cropby = x_cordinate_img(img)
        for i in range(len(cropby)-1):
            temp = img.crop((cropby[i],0,cropby[i+1],height))
            temp.show()
            alphabet = input("눈에 보이는 알파뱃을 대소문자 가려서 입력해주세요")
            directory = "/Users/yunsu/Desktop/python_ocr/alphabet/{}".format(alphabet)
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                num = search(directory)[-1]
                temp.save("/Users/yunsu/Desktop/python_ocr/alphabet/{alphabet_folder}/{alphabet}{number}.jpg".format(
                        alphabet_folder= alphabet,alphabet=alphabet,number=num+1))
            except:
                temp.save("/Users/yunsu/Desktop/python_ocr/alphabet/{alphabet_folder}/{alphabet}{number}.jpg".format(
                        alphabet_folder= alphabet,alphabet=alphabet,number=0))
            cropped.append(temp)
        return cropped
        


#=========================================================================================================================
def check_letter_pixels(array):
    count = 0
    width = len(array[0])
    height = len(array) 
    for x in range(height):
        for y in range(width):
            if array[x][y] == 1:
                count+=1
    return count
            
    
def check_left_side(array):
    count = 0
    width = len(array[0])
    height = len(array) 
    check = width % 2
    if check ==0:
        for x in range(height):
            for y in range(width//2):
                if array[x][y] == 1:
                    count+=1
    if check ==1:
        for x in range(height):
            for y in range((width-1)//2):
                if array[x][y] == 1:
                    count+=1        
            if array[x][(width-1)//2] ==1:
                count +=0.5
    a = check_letter_pixels(array)
    percent = count/a
    return percent



def compare_vertical(array):
    width = len(array[0])
    height = len(array)
    count = 0
    if width % 2 ==0:
        limit = width//2
        for x in range(height):
            for y in range(limit):
                if array[x][y] == 1 and array[x][width-1-y]==1:
                    count +=2
    if width % 2 !=0:
        limit =(width-1)//2
        for x in range(height):
            for y in range(limit):
                if array[x][y] ==1 and array[x][width-1-y]==1:
                    count +=2
            if array[x][limit] == 1:
                count +=1
    a = check_letter_pixels(array)
    percent = count/a
    return percent        

def compare_horizontal(array):
    width = len(array[0])
    height = len(array)
    count = 0
    if height % 2 ==0:
        limit = height//2
        for x in range(limit):
            for y in range(width):
                if array[x][y] == 1 and array[height-x-1][y]==1:
                    count +=2
    if width % 2 !=0:
        limit =(height-1)//2
        for x in range(limit):
            for y in range(width):
                if array[x][y] ==1 and array[height-x-1][y]==1:
                    count +=2
        for y in range(width):
            if array[limit][y] ==1:
                count +=1
    a = check_letter_pixels(array)
    percent = count/a
    return percent


#대각선의 개수까지 포함. 
def compare_diagonal_from_left_bottom(array):
    count = 0
    width = len(array[0])
    height = len(array)
    for x in range(height):
        for y in range(width):
            if array[x][y] ==1 and array[height-y-1][width-x-1]==1:
                count +=1
    
    a = check_letter_pixels(array)
    percent = count/a
    return percent

def compare_diagonal_from_left_top(array):
    count = 0
    width = len(array[0])
    height = len(array)
    for y in range(width):
        for x in range(height):
            if array[x][y] == 1 and array[y][x]==1:
                count +=1

    a = check_letter_pixels(array)
    percent = count/a
    return percent

def image_into_data_list(img_url,size):
    temp_arr = image_into_array(img_url,size)
    arr = make_square_matrix(temp_arr)
    a = check_left_side(arr)
    b = compare_vertical(arr)
    c = compare_horizontal(arr)
    d = compare_diagonal_from_left_bottom(arr)
    e = compare_diagonal_from_left_top(arr)
    return [a,b,c,d,e]

# def urlarr_into_dic(url_arr,size):
#     result = {}
#     for url in url_arr:
#         key = url.split("/")[-1].split(".")[0]
#         value = image_into_data_list(url,size)
#         result[key] = value
#     return result



def image_into_z_score(img_url,size):
    arr = image_into_array(img_url)
            
    mean = [0.51207,0.80240,0.73793,0.48870,0.49100]
    sigma = [0.06285,0.10405,0.13713,0.17777,0.17747]
    a = (check_left_side(arr)-mean[0])/sigma[0]
    b = (compare_vertical(arr)-mean[1])/sigma[1]
    c = (compare_horizontal(arr)-mean[2])/sigma[2]
    d = (compare_diagonal_from_left_bottom(arr)-mean[3])/sigma[3]
    e = (compare_diagonal_from_left_top(arr)-mean[4])/sigma[4]
    return [a,b,c,d,e]
## 첫번쨰 인자 오류남.


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


def infer(arr):
    result = []
    check = [[] for x in range(5)]
    for i in range(5):
        for x in range(26):
            if abs(z_score[x][i+1]-arr[i]) <= 0.5:
                check[i].append(x)
    for alphabet in check[0]:
        count = 0
        for i in range(5):
            if alphabet in check[i]:
                count+=1
            else:
                break
        if count ==5:
            result.append(alphabet)
    
    return z_score[result[0]][0] if len(result)==1 else check


def y_high(arr):
    height = len(arr)
    width = len(arr[0])
    for y in range(height):
        for x in range(width):
            if arr[y][x]==1:
                return y
def y_low(arr):
    height = len(arr)
    width = len(arr[0])
    for y in range(height)[::-1]:
        for x in range(width):
            if arr[y][x]==1:
                return y
            
def x_left(arr):
    height = len(arr)
    width = len(arr[0])
    for x in range(width):
        for y in range(height):
            if arr[y][x] ==1:
                return x
            
def x_right(arr):
    height = len(arr)
    width = len(arr[0])
    for x in range(width)[::-1]:
        for y in range(height):
            if arr[y][x] ==1:
                return x
            
#1 만약 가로 길이가 짝수이면 중간 좌표는 x.5이고 가로 길이가 홀수이면 중간 자표는 int이다.
def make_center(arr):
    y2 = y_high(arr)
    y1 = y_low(arr)
    x1 = x_left(arr)
    x2 = x_right(arr)
    return ((x1+x2)/2,(y1+y2)/2)

#2. 입력받은 arr를 알파뱃 중심을 기준으로 정사각행렬로 변환하기
#2.1 입력받은 arr에서 여백을 삭제해서 같은 정보를 담고 있는최소 사이즈로 만들기
#2.2 최소 사이즈 행렬에서 상하 좌우로 0만 담고있는 행렬을 추가해서 정 사각행렬로 만들기.

#2.1.1
def delete_col(arr,where='right',n=1):
    height = len(arr)
    width = len(arr[0])
    for __ in range(n):
        height = len(arr)
        width = len(arr[0])
        if where =='right':
            arr = np.delete(arr,width-1,1)
        elif where == 'left':
            arr = np.delete(arr,0,1)
    return arr
def delete_row(arr,where='high',n=1):
    height = len(arr)
    width = len(arr[0])
    for __ in range(n):
        height = len(arr)
        width = len(arr[0])
        if where =='high':
            arr = np.delete(arr,0,0)
        elif where == 'low':
            arr = np.delete(arr,height-1,0)
    return arr   
    
#2.2 row, col 추가 함수
def add_col(arr,where='right',n=1):
    for __ in range(n):
        height = len(arr)
        width = len(arr[0])
        if where =='right':
            arr = np.insert(arr,width,0,axis=1)
        elif where == 'left':
            arr = np.insert(arr,0,0,axis=1) 
    return arr

def add_row(arr,where='high',n=1):
    for __ in range(n):
        height = len(arr)
        width = len(arr[0])
        if where =='high':
            arr = np.insert(arr,0,0,axis=0)
        elif where == 'low':
            arr = np.insert(arr,height,0,axis=0) 
    return arr

# 2.1 최소 매트릭스 만들기.
def make_min_matrix(arr):
    height = len(arr)
    width = len(arr[0])
    rm_col_left = x_left(arr)
    rm_col_right = width-1 - x_right(arr)
    rm_row_high = y_high(arr)
    rm_row_low = height-1 - y_low(arr)
    
    arr = delete_col(arr,where='right',n=rm_col_right)
    arr = delete_col(arr,where='left',n=rm_col_left)
    arr = delete_row(arr,where='high',n=rm_row_high)
    arr = delete_row(arr,where='low',n=rm_row_low)
    return arr

## 최소 매트릭스로 정 사각 matrix만들어주기. ()
def make_square_matrix(arr):
    arr = make_min_matrix(arr)
    col = len(arr[0])
    row = len(arr)
    if col - row >= 1:
        m = col - row 
        if m %2 ==0:
            arr = add_row(arr,where='high',n=(m//2))
            arr = add_row(arr,where='low',n=(m//2))
        if m % 2 !=0:
            arr = add_row(arr,where='high',n=(m//2)+1)
            arr = add_row(arr,where='low',n=(m//2))
    if row - col >= 1:
        m = row - col
        if m %2 ==0:
            arr = add_col(arr,where='right',n=(m//2))
            arr = add_col(arr,where='left',n=(m//2))
        if m % 2 !=0:
            arr = add_col(arr,where='right',n=(m//2)+1)
            arr = add_col(arr,where='left',n=(m//2))
    return arr


def data_dict_to_excel(my_dict,file_name):
    import collections
    od = collections.OrderedDict(sorted(my_dict.items()))
    data = {}
    data['alphabet'] = []
    data['left_side_pixels'] = []
    data['verical_coincidence'] = []
    data['horizontal_coincidence'] = []
    data['from_bottom_dia_coincidence'] = []
    data['from_top_dia_coincidence'] = []

    for key,value in od.items():
        data['alphabet'] +=[key]
        data['left_side_pixels'] += [value[0]]
        data['verical_coincidence'] += [value[1]]
        data['horizontal_coincidence'] += [value[2]]
        data['from_bottom_dia_coincidence'] += [value[3]]
        data['from_top_dia_coincidence'] += [value[4]]
    import pandas as pd
    table = pd.DataFrame(data,columns=['alphabet','left_side_pixels','verical_coincidence','horizontal_coincidence',
                                     'from_bottom_dia_coincidence','from_top_dia_coincidence'])
    writer = pd.ExcelWriter('{}.xlsx'.format(file_name))
    table.to_excel(writer,'lowercase 1')
    writer.save()
    
def data_dict_to_table(my_dict):
    import collections
    od = collections.OrderedDict(sorted(my_dict.items()))
    data = {}
    data['alphabet'] = []
    data['left_side_pixels'] = []
    data['verical_coincidence'] = []
    data['horizontal_coincidence'] = []
    data['from_bottom_dia_coincidence'] = []
    data['from_top_dia_coincidence'] = []

    for key,value in od.items():
        data['alphabet'] +=[key]
        data['left_side_pixels'] += [value[0]]
        data['verical_coincidence'] += [value[1]]
        data['horizontal_coincidence'] += [value[2]]
        data['from_bottom_dia_coincidence'] += [value[3]]
        data['from_top_dia_coincidence'] += [value[4]]
    import pandas as pd
    table = pd.DataFrame(data,columns=['alphabet','left_side_pixels','verical_coincidence','horizontal_coincidence',
                                     'from_bottom_dia_coincidence','from_top_dia_coincidence'])
    return table

def img_url_arr_into_excel(url_arr,size,file_name):
    import pandas as pd
    import collections
    
    my_dict = make_percent_dictionary(url_arr,size)
    
    od = collections.OrderedDict(sorted(my_dict.items()))
    data = {}
    data['alphabet'] = []
    data['left_side_pixels'] = []
    data['vertical_coincidence'] = []
    data['horizontal_coincidence'] = []
    data['from_bottom_dia_coincidence'] = []
    data['from_top_dia_coincidence'] = []
    
    
    for key,value in od.items():
        data['alphabet'] +=[key]
        data['left_side_pixels'] += [value[0]]
        data['vertical_coincidence'] += [value[1]]
        data['horizontal_coincidence'] += [value[2]]
        data['from_bottom_dia_coincidence'] += [value[3]]
        data['from_top_dia_coincidence'] += [value[4]]
    table = pd.DataFrame(data,columns=['alphabet','left_side_pixels','verical_coincidence','horizontal_coincidence',
                                     'from_bottom_dia_coincidence','from_top_dia_coincidence'])
    writer = pd.ExcelWriter('{}.xlsx'.format(file_name))
    table.to_excel(writer,'lowercase 1')
    writer.save()
    
# 이미지에 여러 줄로 글들이 구성되어 있을 때 줄들을 구분해주는 흰 여백의 y 좌표를 list로 반환한다.
def y_cordinate(url):
    arr = image_into_array(url,(1000,1000))
    img = Image.open(url)
    width,height = img.size
    ycrop = [0]
    satisfied = 0
    for x in range(height):
        for y in range(width):
            if arr[x][y] == 1:
                satisfied =1
            if satisfied ==1 and 1 not in arr[x]:
                xcrop.append(x)
                satisfied = 0
    return ycrop



# 이미지 내의 한줄로 구성된 문자들이 있을 경우 문자들을 구분해주는 흰 여백의 x좌표를 list로 반환한다.
def x_cordinate(url):
    arr = image_into_array(url,(1000,1000))
    img = Image.open(url)
    xcrop = [0]
    satisfied = 0
    width,height = img.size
    for y in range(width):
        for x in range(height):
            if arr[x][y] == 1:
                satisfied = 1
            if satisfied ==1 and 1 not in [arr[x][y] for x in range(height)]:
                xcrop.append(y)
                satisfied = 0
    return xcrop

# 이미지 객체를 받아 한줄로 구성된 문자들이 있을 경우 문자들을 구분해주는 흰 여백의 x좌표를 list로 반환한다.
def x_cordinate_img(img):
    xcrop = [0]
    satisfied = 0
    width,height = img.size
    for y in range(width):
        for x in range(height):
            if arr[x][y] == 1:
                satisfied = 1
            if satisfied ==1 and 1 not in [arr[x][y] for x in range(height)]:
                xcrop.append(y)
                satisfied = 0
    return xcrop

## 파일 폴더를 받아서 그 폴더 하위에 있는 파일들의 파일명을 filenames에 저장한다. for 구문을 돌면서 filename을 파일명을 텍스트와 확장자로 구분한후,
## 텍스트(ex "A01")을 숫자 부분만 [1:]로 가져온후 int화 한후 배열로 정렬해서 반환한다.
def search(dirname):
    import os
    splitnames = []
    filenames = os.listdir(dirname)
    for filename in filenames:
        splitnames.append(int(os.path.splitext(filename)[1:]))
    return sorted(splitnames)
    
    
