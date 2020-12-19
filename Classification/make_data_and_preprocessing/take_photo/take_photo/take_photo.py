import cv2
import numpy as np
import time
import os
def main():
    dir = "D:/DO AN CDT/code_test/cachua_resize2/train/loai5/"
    cap = cv2.VideoCapture(1)
    i=0
    while(cap.isOpened()):
        _,frame = cap.read()
        img = frame[100:400,200:500,:]
        cv2.imshow("Video",img)
        key = cv2.waitKey(1)
        if(key == ord('s')):
            idx = len(os.listdir(dir))
            file_name = "imgmoi_"+str(idx)+".jpg"
            cv2.imwrite(dir+file_name,img)
            print("Saving!")
        if(key == 27):#ESC key : 27
            break
    cap.release()
    cv2.destroyAllWindows()
    return 1

if __name__ == '__main__':
    main()