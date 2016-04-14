
from naoqi import ALProxy
import cv2
import numpy

ip = "10.10.48.252"
port = 9559

vdp=ALProxy("ALVideoDevice",ip,port)
cam=vdp.subscribeCamera("camtooppaaa", 0, 2, 0, 30)
pic = vdp.getImageRemote(cam)

picc = (numpy.reshape(numpy.frombuffer(pic[6], dtype = '%iuint8' % pic[2]), (pic[1], pic[0], pic[2])))

ret,thresh = cv2.threshold(picc,127,255,0)
canny_output = cv2.Canny(picc, 100,200)
contours, hierarchy = cv2.findContours(canny_output,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(picc,contours,-1,(255,255,255),1)


print contours[0]

cv2.imwrite("image.png",picc)
cv2.imwrite("contours.png", canny_output)


vdp.unsubscribe(cam)
