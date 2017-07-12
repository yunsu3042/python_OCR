# coding: utf-8
import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def relu(x):
    return np.maximum(x, 0)

def softmax(x):
    if x.ndim ==2:
        batch_size = x.shape[0]
        x = x - np.max(x, axis=1).reshape(batch_size, 1)
        
        return np.exp(x)/np.sum(np.exp(x), axis=1).reshape(batch_size, 1)
    x = x - np.max(x)
    return np.exp(x)/sum(np.exp(x))

def mean_squared_error(y,t):
    return 0.5 * np.sum((y - t)**2)

def cross_entropy_error(y,t):
    #y.shape[0]으로 배치사이즈를 가져올 때 1을 가져오기위해서. y.shape (10,) --> (1,10)
    output_size = y.shape[1]
    if y.ndim == 1:
        y = y.reshape(1, y.size)
        t = t.reshape(1, t.size)
    batch_size = y.shape[0]
    h = 1e-7
    
    #전제조건 : y는 one_hot_label이다. 따라서 if문의 조건식은 t와 y 모두 one_hot일경우 이다. --> t를 index 라벨로 바꾼다.
    if t.size != y.size:
        temp = np.zeros_like(y)
        for idx, row in enumerate(temp):
            row[t[idx]] = 1
        t = temp
    error = np.sum(-t * np.log(y + h) + (t - 1) * np.log(1 - y + h))
    mean_error = error / batch_size
    return mean_error

def softmax_loss(X, t):
    y = softmax(X)
    return cross_entropy_error(y, t)
    