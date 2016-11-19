def check_letter_pixels(zero_one_array):
    count = 0
    width = len(zero_one_array[0])
    height = len(zero_one_array) 
    for x in range(height):
        for y in range(width):
            if zero_one_array[x][y] == 1:
                count+=1
    return count
            
    
def check_left_side(array):
    count = 0
    width = len(array[0])
    height = len(array)
    for x in range(height):
        for y in range((width+1)//2):
            if array[x][y] == 1: 
                count +=1
    return count

def compare_vertical(array):
    width = len(array[0])
    height = len(array)
    count = 0
    if width % 2 ==0:
        limit = width//2
        for x in range(height):
            for y in range(limit):
                if array[x][y] == 1 and array[x][width-1-y]==1:
                    count +=1
    if width % 2 !=0:
        limit =(width+1)//2
        for x in range(height):
            for y in range(limit):
                if array[x][y] ==1 and array[x][width-1-y]==1:
                    count +=1
    return count
        

def compare_horizontal(array):
    width = len(array[0])
    height = len(array)
    count = 0
    if height % 2 ==0:
        limit = height//2
        for x in range(limit):
            for y in range(width):
                if array[x][y] == 1 and array[height-x-1][y]==1:
                    count +=1
    if width % 2 !=0:
        limit =(height+1)//2
        for x in range(limit):
            for y in range(width):
                if array[x][y] ==1 and array[height-x-1][y]==1:
                    count +=1
    return count

#대각선의 개수까지 포함. 
def compare_diagonal_from_left_bottom(array):
    count = 0
    width = len(array[0])
    height = len(array)
    for x in range(height):
        for y in range(width-x):
            if array[x][y] ==1 and array[height-y-1][width-x-1]==1:
                count +=1
    return count

def compare_diagonal_from_left_top(array):
    count = 0
    width = len(array[0])
    height = len(array)
    for y in range(width):
        for x in range(height-y):
            if array[x][y] == 1 and array[y][x]==1:
                count +=1
    return count


def image_into_tuples(img_url,size):
    np.set_printoptions(threshold=np.inf)
    img = Image.open(img_url).convert("RGB")
    img.thumbnail(size)
    width,height = img.size
    img_arr = np.array(img).reshape(height,width,3)
    zero_or_one_arr = np.zeros((height,width),dtype=np.uint8)
    # 이미지 배열을 흑백화 하는 과정 img = PIL.Image.open("foo.jpg").convert("L")로도 가능하지만 나중에 커스터마이징을 위해 짰음.
    for x in range(0,height):
        for y in range(0,width):
            a = img_arr[x,y,0]
            b = img_arr[x,y,1]
            c = img_arr[x,y,2]
            det = a*0.2989 + b*0.5870 + c*0.1140
            if det >140:
                color = 0
            else:
                color = 1
            zero_or_one_arr[x,y] = color
    a = check_left_side(zero_or_one_arr)
    b = compare_horizontal(zero_or_one_arr)
    c = compare_vertical(zero_or_one_arr)
    d = compare_diagonal_from_left_bottom(zero_or_one_arr)
    e = compare_diagonal_from_left_top(zero_or_one_arr)
    return (a,b,c,d,e)

def urlarr_into_dic(url_arr,size):
    result = {}
    for url in url_arr:
        key = url.split("/")[-1].split(".")[0]
        value = image_into_tuples(url,size)
        result[key] = value
    return result

def urlarr_into_percent_dic(url_arr,size):
    result = {}
    val_tuple =()
    for url in url_arr:
        key = url.split("/")[-1].split(".")[0]
        values = image_into_tuples(url,size)
        arr = image_into_zero_one_array(url,size)
        for x,value in enumerate(values):
            val_tuple += (value/check_letter_pixels(arr),)
        result[key] = val_tuple
    return result
