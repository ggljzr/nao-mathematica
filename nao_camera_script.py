import naoqi
import cv2
import numpy
from naoqi import ALProxy
vdp = ALProxy("ALVideoDevice", "10.10.48.108", 9559)

cam = vdp.subscribeCamera("camera", 0, 2, 11, 15)
pic = vdp.getImageRemote(cam)
picc = (numpy.reshape(numpy.frombuffer(pic[6], dtype = '%iuint8' % pic[2]), (pic[1],   pic[0], pic[2])))

cv2.imwrite("/tmp/test.jpg", picc)

vdp.unsubscribe(cam)
