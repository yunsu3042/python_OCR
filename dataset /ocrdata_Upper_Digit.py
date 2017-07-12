# coding: utf-8
import numpy as np
import string
import os, sys
from PIL import Image
import pickle

def _change_one_hot_label(X):
    T = np.zeros((X.size, 26), dtype=np.uint8)
    for idx, row in enumerate(T):
        row[X[idx]] = 1
    return T

def infer(X):
    result = ""
    book = list(string.ascii_uppercase)
    for x in X:
        idx = np.argmax(x, axis=0)
        
        result += book[idx]
    return result

def load_dataset(flatten=False, one_hot_label=False):
    file_path = "/Users/yunsu/Downloads/English/Fnt"
    save_file = os.path.dirname(os.getcwd()) + "/dataset" + "/Upper_Digit_only_ocr.pk1"

    if os.path.exists(save_file):
        print("loadind data pickles")
        with open(save_file, 'rb') as f:
            dataset = pickle.load(f)
        print("done")
        return (dataset['x_train'],dataset['t_train']), (dataset['x_test'], dataset['t_test'])
        
    x_train = []
    t_train = []
    folders = []
    lables = list(string.ascii_uppercase)
    for i in range(1, 10):
        folders.append(file_path + "/Sample" + "00{}".format(i))
    for i in range(10, 37):
        folders.append(file_path + "/Sample" + "0{}".format(i))
    for ap_idx, folder in enumerate(folders):
        files = os.listdir(folder)
        for idx, file in enumerate(files):
            file_dir = folder + "/" + file
            img = Image.open(file_dir)
            img.thumbnail((28, 28))
            if flatten == True:
                col = np.array(img, dtype=np.uint8).reshape(-1,)
            else:
                col = np.array(img, dtype=np.uint8).reshape(1,28,28)
            x_train.append(col)
            t_train.append(ap_idx)
            
    x_train = np.array(x_train, dtype=np.uint8)
    t_train = np.array(t_train, dtype=np.uint8)
    p = np.random.permutation(len(x_train))
    x_train = x_train[p]
    t_train = t_train[p]
    div = int(len(x_train) * 0.8)
    x_train, x_test = x_train[0:div], x_train[div:]
    t_train, t_test = t_train[0:div], t_train[div:]
    
    if one_hot_label == True:
        t_train = _change_one_hot_label(t_train)
        t_test = _change_one_hot_label(t_test)
    dataset = {}
    dataset['x_train'] = x_train
    dataset['t_train'] = t_train
    dataset['x_test'] = x_test
    dataset['t_test'] = t_test
    print("making data pickles")
    with open(save_file, 'wb') as f:
        pickle.dump(dataset, f, -1)
    print("done")
    return (dataset['x_train'],dataset['t_train']), (dataset['x_test'], dataset['t_test'])
