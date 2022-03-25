import cv2
import numpy as np

def Durand(hdr):

    ldr= np.zeros((hdr.shape[0],hdr.shape[1],hdr.shape[2]))
    intensity= (hdr[:,:,0]*1+hdr[:,:,1]*40+hdr[:,:,2]*20)/61
    log_i=np.log(intensity)
    log_low_pass=cv2.bilateralFilter(log_i,3,15,15)
    log_high_pass=log_i-log_low_pass
    delta=np.max(log_low_pass)-np.min(log_low_pass)
    gamma=2/delta
    recover=np.power(10,gamma*(log_low_pass)+log_high_pass)
    ldr[:,:,0] = (hdr[:,:,0]/intensity*1.0/np.power(10,np.max(gamma*log_low_pass)))*recover
    ldr[:,:,1] = (hdr[:,:,1]/intensity*1.0/np.power(10,np.max(gamma*log_low_pass)))*recover
    ldr[:,:,2] = (hdr[:,:,2]/intensity*1.0/np.power(10,np.max(gamma*log_low_pass)))*recover

    ldr=np.clip((ldr**0.5)*255,0,255)
    ldr=ldr.astype(np.uint8)
    return ldr
