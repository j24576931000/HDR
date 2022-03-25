import cv2
from cv2 import imread
import numpy as np
import random
from scipy import sparse
import matplotlib.pyplot as plt


def hdr(img_List):

    w=img_List[0].shape[0]
    h=img_List[0].shape[1]
    r_list=[]
    g_list=[]
    b_list=[]
    randomlist = []
    sample_num=50
    for i in range(sample_num):
        a = random.randint(1,h*w)
        randomlist.append(a)
    #print(randomlist)
    
    for i in range(0,sample_num):
        for j in range(0,len(img_List)):
            # print(List[i])
            r_list.append(img_List[j][randomlist[i]//h][randomlist[i]%h][2])
            # print(r_list)
            g_list.append(img_List[j][randomlist[i]//h][randomlist[i]%h][1])
            b_list.append(img_List[j][randomlist[i]//h][randomlist[i]%h][0])
    

    matrixX_r=g_function(sample_num,img_List,r_list)
    matrixX_g=g_function(sample_num,img_List,g_list)
    matrixX_b=g_function(sample_num,img_List,b_list)
    ss = np.array([1/4,1/8,1/16,1/32,1/64,1/128,1/256,1/512])
    total_weight=np.zeros((img_List[0].shape[0],img_List[0].shape[1],img_List[0].shape[2]))
    weight=np.zeros((img_List[0].shape[0],img_List[0].shape[1],img_List[0].shape[2]))
    irr= np.zeros((img_List[0].shape[0],img_List[0].shape[1],img_List[0].shape[2]))
    irr=irr.astype(np.float32)

    
    # for i in range (w):
    #     for j in range (h):
    #         for k in range (len(img_List)):
    #             if img_List[k][i][j][2]>127:
    #                 tmp=(255-img_List[k][i][j][2])*(matrixX[img_List[k][i][j][2]]-np.log(ss[k]))
    #                 irr[i][j][2]+=tmp
    #                 tmp_w=(255-img_List[k][i][j][2])
    #                 total_weight+=tmp_w
    #                 #print(k," = ",irr[i][j][2])
    #                 #print(k,"up= ",(255-img_List[k][i][j][2])*(matrixX[img_List[k][i][j][2]]-ss[k]))

    #             else:
    #                 tmp=((img_List[k][i][j][2]-0)*(matrixX[img_List[k][i][j][2]]-np.log(ss[k])))
    #                 irr[i][j][2]+=tmp
    #                 tmp_w=(img_List[k][i][j][2]-0)
    #                 total_weight+=tmp_w
    #                 #print(k," = ",irr[i][j][2])
    #                 #print(k,"up= ",(img_List[k][i][j][2]-0)*(matrixX[img_List[k][i][j][2]]-ss[k]))
    #     print(irr[i][j][2])
    #     print(total_weight)
    #     irr[i][j][2]=irr[i][j][2]/total_weight
    #     total_weight=0

    
    for k in range (len(img_List)):
        weight[:,:,2]=np.where((img_List[k])[:,:,2]<=127,(img_List[k][:,:,2]),(255-img_List[k][:,:,2]))        
        tmp=weight*(matrixX_r[img_List[k][:,:,2]]-np.log(ss[k]))
        irr+=tmp
        total_weight+=weight

    for k in range (len(img_List)):
        weight[:,:,1]=np.where((img_List[k])[:,:,1]<=127,(img_List[k][:,:,1]),(255-img_List[k][:,:,1]))        
        tmp=weight*(matrixX_g[img_List[k][:,:,1]]-np.log(ss[k]))
        irr+=tmp
        total_weight+=weight
    
    for k in range (len(img_List)):
        weight[:,:,0]=np.where((img_List[k])[:,:,0]<=127,(img_List[k][:,:,0]),(255-img_List[k][:,:,0]))        
        tmp=weight*(matrixX_b[img_List[k][:,:,0]]-np.log(ss[k]))
        irr+=tmp
        total_weight+=weight
        
    irr[:,:,0]=irr[:,:,0]/total_weight[:,:,0]
    irr[:,:,1]=irr[:,:,1]/total_weight[:,:,1]
    irr[:,:,2]=irr[:,:,2]/total_weight[:,:,2]

    
    irr=np.exp(irr)
    print(np.max(irr))
    #print(irr)
    np.save("test.npy",irr)
    cv2.imwrite("test.jpg",irr)
    return 0


def g_function(sample_num,img_List,r_list):


    row = sample_num * len(img_List) + 1 + 254
    column = 256+ sample_num

    matrixA=sparse.csr_matrix((row,column)).toarray()
    matrixB=sparse.csr_matrix((row,1)).toarray()
    #print(r_list)
    for i in range(1,255):
        j=i
        if i<=127:
            matrixA[len(r_list)+i,j-1]=1*(i-0)
            matrixA[len(r_list)+i,j]=-2*(i-0)
            matrixA[len(r_list)+i,j+1]=1*(i-0) 
        else:
            matrixA[len(r_list)+i,j-1]=1*(255-i)
            matrixA[len(r_list)+i,j]=-2*(255-i)
            matrixA[len(r_list)+i,j+1]=1*(255-i)
    k=0
    for i in range(0,sample_num):      
        for j in range(0,len(img_List)): 
            if matrixA[i*len(img_List)+j,256+k]!=0:
                print("error")
            else:
                matrixA[i*len(img_List)+j,256+k]=-1
            # print('i=',i*50+j)
            # print('j=',256+k)
        k+=1
        # print(r_list[i])
        # print('i=',i)
        # print('j=',j)
    matrixA[len(r_list),127]=1
    for i in range(0,len(r_list)):
        j=r_list[i]   
        if matrixA[i,j]!=0:
            print("error")
        else:
            matrixA[i,j]=1

    ss = np.array([1/4,1/8,1/16,1/32,1/64,1/128,1/256,1/512])
    
    for i in range(0,sample_num):
        for j in range(len(img_List)):
            matrixB[i*len(img_List)+j] = ss[j]
    print(matrixB)
    matrixX=np.linalg.lstsq(matrixA, matrixB , rcond=None)[0][:256]
    # print(matrixA)
    # print(matrixX)


    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(matrixX,'g')
    
    plt.show()

    return matrixX




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





