import cv2
import numpy as np
import os

os.chdir("D:/DO AN CDT/code_test")
my_dir = "cachua_resize2/take_photo/loai4/"

name_list = os.listdir(my_dir)
for i,name in enumerate(name_list):
    img = cv2.imread(my_dir + name)
    h,w = img.shape[:2]
    r45_M = cv2.getRotationMatrix2D((h/2,w/2),45,1)
    r45_img = cv2.warpAffine(img, r45_M, (h, w))
    rn45_M = cv2.getRotationMatrix2D((h/2,w/2),-45,1)
    rn45_img = cv2.warpAffine(img, rn45_M, (h, w))
    scale_img = cv2.resize(img[50:310,50:320,:],(300,300))
    cv2.imwrite(my_dir+ "imgr45_%3d.jpg"%(i),r45_img)
    cv2.imwrite(my_dir+ "imgrn45_%3d.jpg"%(i),rn45_img)
    cv2.imwrite(my_dir+ "imgsc_%3d.jpg"%(i),scale_img)
    #cv2.imwrite(my_dir+ "imgr45_"+name[7:10]+".jpg",r45_img)
    #cv2.imwrite(my_dir+ "imgrn45_"+name[7:10]+".jpg",rn45_img)
    #cv2.imwrite(my_dir+ "imgsc_"+name[7:10]+".jpg",scale_img)