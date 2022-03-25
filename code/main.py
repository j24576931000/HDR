from image_alignment import alignment
from hdr import hdr
from tone_mapping import tone_mapping
import cv2
import numpy as np
import os


if __name__=='__main__':
    #read data
    img_list=[]
    result_list=[]
    for filename in os.listdir(r"./" + 'data'):
        img_list.append(filename)
        print(filename)

    #alignment
    base_img = cv2.imread(os.path.join('data',img_list[0]))
    print(len(img_list))
    result_list.append(base_img)
    
    for i in range(1,len(img_list)):
        data_img = cv2.imread(os.path.join('data',img_list[i]))#讀取圖片
        result=alignment.alignment(base_img,data_img)  
        result_list.append(result)
        print(i)

    print("HDR...")
    img=hdr.hdr(result_list)
    print("HDR")
    #tonemapping
    print("tonemapping...")
    ldr=tone_mapping.Durand(img)
    print("tonemapping finish")
    cv2.imwrite('tone_mapping/result/final.png',ldr)
    # 按下任意鍵則關閉所有視窗
    cv2.waitKey(0)
    cv2.destroyAllWindows()

