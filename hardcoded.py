import cv2
import numpy as np

image_path = "images/orig.png"

#picc = (numpy.reshape(numpy.frombuffer(pic[6], dtype = '%iuint8' % pic[2]), (pic[1], pic[0], pic[2])))
img = cv2.imread("images/orig.png")
rows, cols, ch = img.shape

pts1 = np.float32([[160,47],[115,321],[395,223],[417,406]])
pts2 = np.float32([[0,0],[0,rows],[cols,0],[cols,rows]])

M = cv2.getPerspectiveTransform(pts1,pts2)
dst = cv2.warpPerspective(img,M,(rows,cols))

dst = dst[50:200, 50:400]

#ty prahy 100,200 sou asi moc, 60,200 vychazi lip
#u tech kontur bude potreba nak voriznout ty zbytky ty tabule po
#ty transformaci
canny_output = cv2.Canny(dst, 40,200)
contours, hierarchy = cv2.findContours(canny_output,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(dst,contours,-1,(255,255,255),1)

img_name = image_path.split('/')[-1:][0].split('.')[0]
path_scgink = "seshat/SampleMathExps/{}.scgink".format(img_name)
with open(path_scgink, 'w') as ink_file:
	ink_file.write("SCG_INK\n")
	ink_file.write("{}\n".format(len(contours)))
	for contour in contours:
		ink_file.write("{}\n".format(len(contour)))
		for coord in contour:
			ink_file.write("{} {}\n".format(coord[0][0], coord[0][1]))



cv2.imshow("orig", img)
cv2.imshow("dst", dst)
cv2.waitKey()
