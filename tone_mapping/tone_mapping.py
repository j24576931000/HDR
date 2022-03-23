import cv2
import numpy as np

def Durand(hdr):

    ldr= np.zeros((hdr.shape[0],hdr.shape[1],hdr.shape[2]))
    # intensity_array= np.zeros((hdr.shape[0],hdr.shape[1],hdr.shape[2]))
    # intensity_array[:,:,0]=intensity_array[:,:,1]=intensity_array[:,:,2]= (hdr[:,:,0]*1+hdr[:,:,1]*40+hdr[:,:,2]*20)/61
    intensity= (hdr[:,:,0]*1+hdr[:,:,1]*40+hdr[:,:,2]*20)/61
    #cv2.imwrite('tone_mapping/result/intensity.jpg',intensity)
    log_i=np.log(intensity)
    
    log_low_pass=cv2.bilateralFilter(log_i,3,15,15)
    #cv2.imwrite('tone_mapping/result/low_pass_image.jpg',np.power(10,log_low_pass))

    log_high_pass=log_i-log_low_pass
    #cv2.imwrite('tone_mapping/result/high_pass_image.jpg',np.power(10,log_high_pass))

    delta=np.max(log_low_pass)-np.min(log_low_pass)
    gamma=2/delta
    recover=np.power(10,gamma*(log_low_pass)+log_high_pass)
    
    
    #cv2.imwrite('tone_mapping/result/recover.jpg',recover)

    # ldr[:,:,0] = (hdr[:,:,0]/intensity)*recover
    # ldr[:,:,1] = (hdr[:,:,1]/intensity)*recover
    # ldr[:,:,2] = (hdr[:,:,2]/intensity)*recover

    ldr[:,:,0] = (hdr[:,:,0]/intensity*1.0/np.power(10,np.max(gamma*log_low_pass)))*recover
    ldr[:,:,1] = (hdr[:,:,1]/intensity*1.0/np.power(10,np.max(gamma*log_low_pass)))*recover
    ldr[:,:,2] = (hdr[:,:,2]/intensity*1.0/np.power(10,np.max(gamma*log_low_pass)))*recover

    ldr=np.clip((ldr**0.5)*255,0,255)
    ldr=ldr.astype(np.uint8)
    return ldr

# if __name__=='__main__':
#     img=np.load('irradiancemap.npy')   
#     cv2.imwrite('origin.jpg',img)
#     ldr=Durand(img)
#     cv2.imwrite('final.jpg',ldr)
#     # 按下任意鍵則關閉所有視窗
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
