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
  
    irr_result=irradiance(img_List,matrixX_r,matrixX_g,matrixX_b)
    
    return irr_result


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
    w_list=[]
    matrixA[len(r_list),127]=1
    for i in range(0,len(r_list)):
        j=r_list[i]   
        if j<=127:
            matrixA[i,j]=1*j
            w_list.append(j)
        else:
            matrixA[i,j]=1*(255-j)
            w_list.append(255-j)


    k=0
    for i in range(0,sample_num):      
        for j in range(0,len(img_List)): 
            matrixA[i*len(img_List)+j,256+k]=-1*w_list[i*len(img_List)+j]
            
        k+=1
        
    

    ss = np.array([1/2,1/4,1/8,1/16,1/32,1/64,1/128,1/256,1/512,1/1024,1/2048])
    
    for i in range(0,sample_num):
        for j in range(len(img_List)):
            matrixB[i*len(img_List)+j] = np.log(ss[j])*w_list[i*len(img_List)+j]
    #print(matrixB)
    matrixX=np.linalg.lstsq(matrixA, matrixB , rcond=None)[0][:256]
    #print(matrixA)
    # print(matrixX)


    # fig=plt.figure()
    # ax=fig.add_subplot(111)
    # ax.plot(matrixX,'g')
    
    # plt.show()

    return matrixX

def irradiance(img_List,matrixX_r,matrixX_g,matrixX_b):
    ss = np.array([1/2,1/4,1/8,1/16,1/32,1/64,1/128,1/256,1/512,1/1024,1/2048])
    total_weight=np.zeros((img_List[0].shape[0],img_List[0].shape[1],img_List[0].shape[2]))
    weight=np.zeros((img_List[0].shape[0],img_List[0].shape[1],img_List[0].shape[2]))
    irr= np.zeros((img_List[0].shape[0],img_List[0].shape[1],img_List[0].shape[2]))
    irr=irr.astype(np.float32)
    
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

    irr=np.nan_to_num(irr)
    irr=np.exp(irr)

    print(np.max(irr))
    #print(irr)
    #np.save("test.npy",irr)
    cv2.imwrite("HDR.png",irr)
    
    return irr








