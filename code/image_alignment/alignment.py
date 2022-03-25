import cv2
import numpy as np
def BGRtoGray(image):
    RGB_image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    RGB_image = RGB_image.astype(np.int)
    n_RGB_image = (RGB_image[:,:,0]*54/256+RGB_image[:,:,1]*183/256+RGB_image[:,:,2]*19/256)
    return n_RGB_image

def MTB(image): 
    med = int(np.median(image))
    image[image>med]=255
    image[image<=med]=0
    return image

def Resize_Image(image):       
    image=cv2.resize(image,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_AREA)
    image=MTB(image) 
    return image

def Alignment(image,image2,last_shift):
    height=image.shape[0]
    width=image.shape[1]
    offset_x = [
        [1,0,-1],[1,0,0],[1,0,1]
    ]
    offset_y = [
        [0,1,-1],[0,1,0],[0,1,1]
    ]  
    num=0
    for i in offset_x:
        for j in offset_y:
            similarity=0
            shift = np.float32([i,j])
            dst=cv2.warpAffine(image,shift,(width,height))
            xor = cv2.bitwise_xor(dst,image2)      
            for k in range(0,height):
                for l in range(0,width):
                    if xor[k][l] == 0:                       
                        similarity=similarity+1    
            if num==0:           
                tmp_similarity=similarity
                best_shift=last_shift+shift
            else :
                if similarity>tmp_similarity:
                    tmp_similarity=similarity
                    best_shift=last_shift+shift
            num=num+1      
    return best_shift

def Recover(best_shift,image):
    height=image.shape[0]
    width=image.shape[1]
    best_shift[0][0]=1
    best_shift[1][0]=0
    best_shift[0][1]=0
    best_shift[1][1]=1
    best_shift[0][2]=best_shift[0][2]*2
    best_shift[1][2]=best_shift[1][2]*2
    dst=cv2.warpAffine(image,best_shift,(width,height))
    return dst
def alignment(base,data):
    Image_List=[]
    Image_List2=[]
    Gray_image=BGRtoGray(data)
    Gray_image2=BGRtoGray(base)

    #gray to mtb
    MTB_image=MTB(Gray_image)
    MTB_image2=MTB(Gray_image2)
    Image_List.append(MTB_image)
    Image_List2.append(MTB_image2)


    #resize image
    #0-1
    Image=Resize_Image(MTB_image)
    Image_List.append(Image)
    Image2=Resize_Image(MTB_image2)
    Image_List2.append(Image2)
    #1-2 2-3 3-4 4-5
    for i in range(0,4):
        Image=Resize_Image(Image)
        Image_List.append(Image)
        Image2=Resize_Image(Image2)
        Image_List2.append(Image2)


    #recover
    best_shift=0
    #5-4 4-3 3-2 2-1
    for i in range(0,4):
        best_shift=Alignment(Image_List[5-i],Image_List2[5-i],best_shift)
        Final=Recover(best_shift,Image_List[4-i])
    # 1-0
    best_shift=Alignment(Image_List[1],Image_List2[1],best_shift)
    Final=Recover(best_shift,data) 
    return Final

    




    