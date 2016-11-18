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
