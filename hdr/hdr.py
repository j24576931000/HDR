import cv2
from cv2 import imread
import numpy as np
import random
from scipy import sparse


def hdr(img_List):

    w=img_List[0].shape[0]
    h=img_List[0].shape[1]
    r_list=[]
    g_list=[]
    b_list=[]
    randomlist = []
    for i in range(50):
        a = random.randint(1,h*w)
        randomlist.append(a)
    print(randomlist)
    
    for i in range(0,8):
        for j in range(50):
            # print(List[i])
            r_list.append(img_List[i][randomlist[j]//h][randomlist[j]%h][2])
            # print(r_list)
            g_list.append(img_List[i][randomlist[j]//h][randomlist[j]%h][1])
            b_list.append(img_List[i][randomlist[j]//h][randomlist[j]%h][0])
    
    row = 50 * 8 + 1 + 254
    column = 256+ 50
    matrixA=sparse.csr_matrix((row,column)).toarray()
    matrixB=sparse.csr_matrix((row,1)).toarray()

    # for i in range(50*8):
    matrixA[len(r_list),128]=1
    for i in range(0,len(r_list)):
        #for j in range(50):
        j=r_list[i]+1     
        matrixA[i,j]=1
        

    for i in range(1,255):
        j=i
        matrixA[len(r_list)+i,j-1]=1
        matrixA[len(r_list)+i,j]=-2
        matrixA[len(r_list)+i,j+1]=1
    
    #print(matrixA[len(r_list)+254][253])

    k=1
    for i in range(0,len(img_List)):      
        for j in range(0,50):        
            matrixA[i*50+j,255+k]=-1
        k+=1


    ss = np.array([1/4,1/8,1/16,1/32,1/64,1/128,1/256,1/512,1/1024])
    for i in range(0,len(img_List)):
        for j in range(50):
            matrixB[i*50+j] = ss[i]
    #print(matrixB)
    matrixX=np.linalg.lstsq(matrixA, matrixB , rcond=None)[0][:256]
    print(matrixX)


    
    
        




       


    return 0









if __name__=='__main__':
    List=[]
    img=cv2.imread('image_alignment/result/My_Image1.jpg')
    List.append(img)
    img2=cv2.imread('image_alignment/result/My_Image2.jpg')
    List.append(img2)
    img3=cv2.imread('image_alignment/result/My_Image3.jpg')
    List.append(img3)
    img4=cv2.imread('image_alignment/result/My_Image4.jpg')
    List.append(img4)
    img5=cv2.imread('image_alignment/result/My_Image5.jpg')
    List.append(img5)
    img6=cv2.imread('image_alignment/result/My_Image6.jpg')
    List.append(img6)
    img7=cv2.imread('image_alignment/result/My_Image7.jpg')
    List.append(img7)
    img8=cv2.imread('image_alignment/result/My_Image8.jpg')
    List.append(img8)

    hdr(List)





