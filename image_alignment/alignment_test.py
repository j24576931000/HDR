#from turtle import width
import cv2
#from cv2 import AlignMTB
import numpy as np
img_list=[]
img = cv2.imread('test2.jpg')#讀取圖片
img_list.append(img)
img2 = cv2.imread('test1.jpg')#讀取圖片
img_list.append(img)



def BGRtoGray(image):
    RGB_image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    for i in range(RGB_image.shape[0]):
        for j in range(RGB_image.shape[1]):
            RGB_image[i][j]=((RGB_image[i][j][0]*54+RGB_image[i][j][1]*183+19*RGB_image[i][j][2])/256)
    return RGB_image


def MTB(image): 
    med = int(np.median(image))
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if(image[i][j][0]>med):
                image[i][j]=255
            else :
                image[i][j]=0
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
                    if xor[k][l][0] == 0:                       
                        similarity=similarity+1    
            if num==0:           
                tmp_similarity=similarity
                best_shift=last_shift+shift
                print(tmp_similarity)
            else :
                if similarity>tmp_similarity:
                    tmp_similarity=similarity
                    best_shift=last_shift+shift
                    print(tmp_similarity)
            num=num+1      
    return best_shift

def Recover(best_shift,image):
    height=image.shape[0]
    width=image.shape[1]
    # print('shape',best_shift.shape)
    print('shape',best_shift[0])
    print('shape',best_shift[1])
    best_shift[0][0]=1
    best_shift[1][0]=0

    best_shift[0][1]=0
    best_shift[1][1]=1

    best_shift[0][2]=best_shift[0][2]*2
    best_shift[1][2]=best_shift[1][2]*2
    dst=cv2.warpAffine(image,best_shift,(width,height))
    print('shape',best_shift[0])
    print('shape',best_shift[1])

    return dst



# def mouse_click(event,x,y,flags,para):
#     if event==cv2.EVENT_LBUTTONDOWN:
#         print(x,y)
#         print('img',img[y,x])
#         print('color',color[y,x])
#         #print('gray',gray[y,x])
#         print(((color[y,x][0]*54+color[y,x][1]*183+19*color[y,x][2])/256))


if __name__=='__main__':

    Image_List=[]
    Image_List2=[]
    Gray_image=BGRtoGray(img)
    Gray_image2=BGRtoGray(img2)
    MTB_image=MTB(Gray_image)
    MTB_image2=MTB(Gray_image2)

    Image_List.append(MTB_image)
    Image_List2.append(MTB_image2)

    #0-1
    Image=Resize_Image(MTB_image)
    Image_List.append(Image)
    Image2=Resize_Image(MTB_image2)
    Image_List2.append(Image2)
    for i in range(0,4):
        Image=Resize_Image(Image)
        Image_List.append(Image)
        Image2=Resize_Image(Image2)
        Image_List2.append(Image2)
    best_shift=0
    for i in range(0,4):
        best_shift=Alignment(Image_List[5-i],Image_List2[5-i],best_shift)
        Final=Recover(best_shift,Image_List[4-i])
    # #5-4
    # best_shift=Alignment(Image_List[5],Image_List2[5],0)
    # Final=Recover(best_shift,Image_List[4])
    # #4-3
    # best_shift=Alignment(Image_List[4],Image_List2[4],best_shift)
    # Final=Recover(best_shift,Image_List[3])

    # #3-2
    # best_shift=Alignment(Image_List[3],Image_List2[3],best_shift)
    # Final=Recover(best_shift,Image_List[2])
    # #2-1
    # best_shift=Alignment(Image_List[2],Image_List2[2],best_shift)
    # Final=Recover(best_shift,Image_List[1])
    # #1-0
    best_shift=Alignment(Image_List[1],Image_List2[1],best_shift)
    Final=Recover(best_shift,img)



    
    # for i in range(Image.shape[0]):
    #     for j in range(Image.shape[1]):
    #         print(Image[i][j])

    # print('image2:  ',Image2.shape)
    # for i in range(MTB_image2.shape[0]):
    #     for j in range(MTB_image2.shape[1]):
    #         print(MTB_image2[i][j])
    # cv2.namedWindow("My Image")
    #cv2.setMouseCallback("My Image",mouse_click)
    cv2.imshow('My Image', img2)
    cv2.imshow('My Image_F', Final)
    

    # 按下任意鍵則關閉所有視窗
    cv2.waitKey(0)
    cv2.destroyAllWindows()




    