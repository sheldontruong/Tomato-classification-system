import cv2
import numpy as np
import os
import h5py
import argparse

def shuffle_data(x_train,y_train):
    idex = np.random.permutation(len(x_train))
    return x_train[idex],y_train[idex]

def main(args):
    os.chdir(args.workingdir)
    #link folder : cachua_resize2
    #              |_____________train
    #                            |____loai1
    #                            |____loai2
    #                            |____loai3
    #                            |____loai4
    #                            |____loai5
    #                            |____loai6
    #              |_____________test
    #                            |____(the same with train)
    train_dir = "cachua_resize2/train/"
    test_dir = "cachua_resize2/test/"
    
    train_classes = os.listdir(train_dir)
    x_train = []
    y_train = []
    i = 0
    for t_class in train_classes:
        y_now = np.zeros((6,))
        t_list = os.listdir(train_dir+t_class)
        y_now[int(t_class[4])-1] = 1
        for img_name in t_list:
            print(t_class,img_name)
            img = cv2.imread(train_dir+t_class+"/"+img_name)
            img = cv2.resize(img,(100,100)) #resize
            img = img/255 #normalization
            x_train.append(img)
            y_train.append(y_now)
            print("img"+str(i))
            i+=1
    x = np.asarray(x_train) #data, shape (num_image,100,100,3)
    y = np.asarray(y_train) #label,shape (num_image,6)
    print(len(x))
    x_train,y_train = shuffle_data(x,y)
    with h5py.File(args.output,'w') as F:
        F.create_dataset('x_train',data = x_train)
        F.create_dataset('y_train',data = y_train)
    return 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--workingdir",default=".",help="current working directory")
    parser.add_argument("--output",default="train_data_100.h5",help)
    main()

