# coding: utf-8
import numpy as np
import sys, os
import pickle
sys.path.append(os.pardir)
from common.functions import *
from common.layers import *


"""정확도 99% 이상의 고정밀 합성곱 신경망
   네트워크 구성은 아래와 같음
   conv - batchnorm - relu - conv - batchnorm - relu - pool -
   conv - batchnorm - relu - conv - batchnorm - relu - pool -
   conv - batchnorm - relu - conv - batchnorm - relu - pool -
   affine - batchnorm - relu - affine - batchnorm - softmax"""

class DeepConvNet:
    def __init__(self, input_dim=(1,28,28), file_path=None,
                conv_params1={'filter_num':32, 'filter_size':3, 'pad':1, 'stride':1},
                conv_params2={'filter_num':32, 'filter_size':3, 'pad':1, 'stride':1},
                conv_params3={'filter_num':64, 'filter_size':3, 'pad':1, 'stride':1},
                conv_params4={'filter_num':64, 'filter_size':3, 'pad':2, 'stride':1},
                conv_params5={'filter_num':128, 'filter_size':3, 'pad':1, 'stride':1},
                conv_params6={'filter_num':128, 'filter_size':3, 'pad':1, 'stride':1},
                hidden_size=100, output_size=26):
        BN_init = [1, 1, 1, 1, 1, 1, 1, 1]

        if file_path:
            print("loading param pickles")
            with open(file_path, 'rb') as f:
                self.params = pickle.load(f)
            print("done")
        else:
            pre_node_num = np.ones(8, dtype=np.uint16)
            pre_channel_num = input_dim[0]
            for idx, conv_params in enumerate([conv_params1, conv_params2, conv_params3, 
                                               conv_params4, conv_params5, conv_params6]):
                pre_node_num[idx] = pre_channel_num * conv_params['filter_size'] ** 2
                pre_channel_num = conv_params['filter_num']
            pre_node_num[6] = conv_params6['filter_num'] * 4 * 4
            pre_node_num[7] = hidden_size
            print(pre_node_num)
            weight_init_std = np.sqrt(2/pre_node_num)

            self.params = {}
            channel_num = input_dim[0]
            for idx, conv_params in enumerate([conv_params1, conv_params2, conv_params3, 
                                               conv_params4, conv_params5, conv_params6]):
                self.params['W' + str(idx + 1)] = weight_init_std[idx] * np.random.randn(
                    conv_params['filter_num'], channel_num, conv_params['filter_size'], conv_params['filter_size'])
                self.params['b' + str(idx + 1)] = np.zeros(conv_params['filter_num'])
                channel_num = conv_params['filter_num']
            self.params['W7'] = weight_init_std[6] * np.random.randn(pre_node_num[6], hidden_size)
            self.params['b7'] = np.zeros(hidden_size)
            self.params['W8'] = weight_init_std[7] * np.random.randn(pre_node_num[7], output_size)
            self.params['b8'] = np.zeros(output_size)
            
            for idx in range(8):
                self.params['G' + str(idx + 1)] = 1.0
                self.params['B' + str(idx + 1)] = 0.0
        
        self.layers = []
        self.layers.append(Convolution(self.params['W1'], self.params['b1'], 
                           conv_params1['stride'], conv_params1['pad']))
        self.layers.append(BatchNormalization(gamma=self.params['G1'], beta=self.params['B1']))
        self.layers.append(Relu())
        self.layers.append(Convolution(self.params['W2'], self.params['b2'], 
                           conv_params2['stride'], conv_params2['pad']))
        self.layers.append(BatchNormalization(gamma=self.params['G2'], beta=self.params['B2']))
        self.layers.append(Relu())
        self.layers.append(Pooling(pool_h=2, pool_w=2, stride=2))
        self.layers.append(Convolution(self.params['W3'], self.params['b3'], 
                           conv_params3['stride'], conv_params3['pad']))
        self.layers.append(BatchNormalization(gamma=self.params['G3'], beta=self.params['B3']))
        self.layers.append(Relu())
        self.layers.append(Convolution(self.params['W4'], self.params['b4'],
                           conv_params4['stride'], conv_params4['pad']))
        self.layers.append(BatchNormalization(gamma=self.params['G4'], beta=self.params['B4']))
        self.layers.append(Relu())
        self.layers.append(Pooling(pool_h=2, pool_w=2, stride=2))
        self.layers.append(Convolution(self.params['W5'], self.params['b5'],
                           conv_params5['stride'], conv_params5['pad']))
        self.layers.append(BatchNormalization(gamma=self.params['G5'], beta=self.params['B5']))
        self.layers.append(Relu())
        self.layers.append(Convolution(self.params['W6'], self.params['b6'],
                           conv_params6['stride'], conv_params6['pad']))
        self.layers.append(BatchNormalization(gamma=self.params['G6'], beta=self.params['B6']))
        self.layers.append(Relu())
        self.layers.append(Pooling(pool_h=2, pool_w=2, stride=2))
        self.layers.append(Affine(self.params['W7'], self.params['b7']))
        self.layers.append(BatchNormalization(gamma=self.params['G7'], beta=self.params['B7']))
        self.layers.append(Relu())
        self.layers.append(Affine(self.params['W8'], self.params['b8']))
        self.layers.append(BatchNormalization(gamma=self.params['G8'], beta=self.params['B8']))

        self.last_layer = SoftmaxWithLoss()
        
    def predict(self, x, train_flg=False):
        for layer in self.layers:
            if isinstance(layer, DropOut):
                x = layer.forward(x, train_flg)
            else:
                x = layer.forward(x)
        return x
    
    def loss(self, x, t):
        y = self.predict(x, train_flg=True)
        return self.last_layer.forward(y, t)
    
    def accuracy(self, x, t, batch_size=100):
        acc = 0.0
        
        if t.ndim != 1:
            t = np.argmax(t, axis=1)
        y = self.predict(x)
        y = np.argmax(y, axis=1)
        acc = np.sum(y==t)/x.shape[0]
        return acc
    
    def gradient(self, x, t):
        self.loss(x, t)
        grads = {}
        dout = 1
        dout = self.last_layer.backward(dout)
        
        tmp_layers = self.layers.copy()
        tmp_layers.reverse()
        for layer in tmp_layers:
            dout = layer.backward(dout)

        for idx, layer_idx in enumerate([1, 4, 8, 11, 15, 18, 22, 25]):
            grads['G' + str(idx + 1)] = self.layers[layer_idx].dgamma
            grads['B' + str(idx + 1)] = self.layers[layer_idx].dbeta
            
        for idx, layer_idx in enumerate([0, 3, 7, 10, 14, 17, 21, 24]):
            grads['W' + str(idx + 1)] = self.layers[layer_idx].dW
            grads['b' + str(idx + 1)] = self.layers[layer_idx].db
            
        return grads
    
    def save_params(self, file_name="params.pkl"):
        params = {}
        for key, val in self.params.items():
            params[key] = val
        with open(file_name, 'wb') as f:
            pickle.dump(params, f)

    def load_params(self, file_name="params.pkl"):
        with open(file_name, 'rb') as f:
            params = pickle.load(f)
        for key, val in params.items():
            self.params[key] = val

        for i, layer_idx in enumerate((0, 3, 7, 10, 14, 17, 21, 24)):
            self.layers[layer_idx].W = self.params['W' + str(i+1)]
            self.layers[layer_idx].b = self.params['b' + str(i+1)]
            
            