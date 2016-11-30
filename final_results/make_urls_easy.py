alphabet_arr = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
url_arr = ["/Users/yunsu/Desktop/python_ocr/lowercase/{}.jpg".format(x) for x in alphabet_arr]

url_arr[0].split("/")[-1].split(".")[0]
