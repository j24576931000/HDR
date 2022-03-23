from image_alignment import alignment
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

    # for i in result_list:
    #     cv2.imwrite('image_alignment/result/My_Image'+i+'.jpg', result_list[i])
    cv2.imwrite('image_alignment/result/My_Image1.jpg', result_list[0])
    cv2.imwrite('image_alignment/result/My_Image2.jpg', result_list[1])
    cv2.imwrite('image_alignment/result/My_Image3.jpg', result_list[2])
    cv2.imwrite('image_alignment/result/My_Image4.jpg', result_list[3])
    cv2.imwrite('image_alignment/result/My_Image5.jpg', result_list[4])
    cv2.imwrite('image_alignment/result/My_Image6.jpg', result_list[5])
    cv2.imwrite('image_alignment/result/My_Image7.jpg', result_list[6])
    cv2.imwrite('image_alignment/result/My_Image8.jpg', result_list[7])
    cv2.imwrite('image_alignment/result/My_Image9.jpg', result_list[8])



    #tonemapping
    img=np.load('tone_mapping/irradiancemap.npy')   
    #cv2.imwrite('tone_mapping/result/origin.jpg',img)
    ldr=tone_mapping.Durand(img)
    cv2.imwrite('tone_mapping/result/final.jpg',ldr)
    # 按下任意鍵則關閉所有視窗
    cv2.waitKey(0)
    cv2.destroyAllWindows()

