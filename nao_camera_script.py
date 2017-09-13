import naoqi
import cv2
import numpy
import sys
from naoqi import ALProxy
vdp = ALProxy("ALVideoDevice", "10.10.48.252", 9559)

cam = vdp.subscribeCamera("camera", 0, 2, 11, 15)
pic = vdp.getImageRemote(cam)
picc = (numpy.reshape(numpy.frombuffer(pic[6], dtype = '%iuint8' % pic[2]), (pic[1],   pic[0], pic[2])))

img_name = 'test.png'

if len(sys.argv) > 1:
	img_name = sys.argv[1]

cv2.imshow(img_name, picc)
cv2.imwrite(img_name, picc)

cv2.waitKey()

vdp.unsubscribe(cam)
