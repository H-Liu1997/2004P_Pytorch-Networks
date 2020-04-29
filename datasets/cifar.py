import os
import numpy as np 
import torch 
import cv2
from random import randint
import torchvision.transforms as transforms


def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict


class CIFARData(torch.utils.data.Dataset):
    def __init__(self, img_path, dtype='train', label_path=None, aug=None):
        self.data_full = unpickle(img_path)
        self.data = np.array(self.data_full[b'data'])
        self.label = np.array(self.data_full[b'labels'])
        self.dtype = dtype
        self.aug = aug
        
    def __getitem__(self,index):
        data_final = self.data[index].reshape(32,32,3) 
        if self.aug is not None:
            data_final = self.aug(data_final)
        if self.dtype == 'test':
            return data_final
        else:
            label_final = torch.from_numpy(np.array(self.label[index]))
            return data_final,label_final

    def __len__(self):
        return self.label.shape[0]