import cv2
import numpy as np

#videofile = 'https://iframe.videodelivery.net/2ab2150459f14de4222459d5cf6d7a20'

def getFirstFrame(videofile):
    
    vidcap = cv2.VideoCapture(videofile)
    success, image = vidcap.read()
    if success:
        cv2.imwrite("video/first_frame.jpg", image)
        print('Saved first frame')
    else:
        print('Failed to save first frame')

getFirstFrame(videofile)
