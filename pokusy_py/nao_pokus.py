
from naoqi import ALProxy
import cv2
import numpy

ip = "10.10.48.252"
port = 9559

vdp=ALProxy("ALVideoDevice",ip,port)
cam=vdp.subscribeCamera("camtopaaa", 0, 2, 12, 30)
pic = vdp.getImageRemote(cam)

picc = (numpy.reshape(numpy.frombuffer(pic[6], dtype = '%iuint8' % pic[2]), (pic[1], pic[0], pic[2])))

yellow=cv2.inRange(picc, (22,100,100),(80,255,255)) #yellow
blue=cv2.inRange(picc, (160,45,45),(170,255,255)) #blue
red=cv2.inRange(picc, (0,45,45), (20,255,255)) #red

color_coords = []

for color in (yellow, 'yellow'), (blue, 'blue'),(red, 'red'):
	blur = cv2.medianBlur(color[0], 7)
	dist = cv2.distanceTransform(blur, cv2.cv.CV_DIST_L2,5)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(dist)
	normal = cv2.normalize(dist, alpha=0,beta=255,norm_type=cv2.cv.CV_MINMAX,dtype=cv2.cv.CV_8UC1)
	print "{}: x={} y={} r={}".format(color[1],max_loc[0],max_loc[1],max_val)
	if max_val > 0:
		color_coords.append((color[1], max_loc))
		cv2.imwrite("{}_normal.png".format(color[1]), normal)

color_coords.sort(key= lambda x: x[1][0])

print "zleva"

for color in color_coords:
	print color[0]

cv2.imwrite("blue.png", blue)
cv2.imwrite("red.png", red)
cv2.imwrite("yellow.png", yellow)
cv2.imwrite("orig.png", picc)
vdp.unsubscribe(cam)
