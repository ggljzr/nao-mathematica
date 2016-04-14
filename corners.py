
import cv2
import numpy as np
import sys


image_path = "images/image2.png"

argc = len(sys.argv)

if argc > 1:
	image_path = str(sys.argv[1])

img = cv2.imread(image_path)

#nejdriv prevedu na grayscale a vykreslim
#kontury podel hran (canny)
#tyhle kontury budou pro detekci primek a rohu
#a je lepsi je udelat silnejsi (2px)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,60,200,apertureSize = 3)
contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(edges,contours,-1,(255,255,255),2)

#udelam detekci primek
lines = cv2.HoughLines(edges,1,np.pi/180,250)

#primky vykreslim do cernobilyho vobrazku bilou
#bez vykresleni tech primek ma ta detekce rohu
#pak docela problemy
for rho,theta in lines[0]:
	a = np.cos(theta)
	b = np.sin(theta)
	x0 = a*rho
	y0 = b*rho
	x1 = int(x0 + 1000*(-b))
	y1 = int(y0 + 1000*(a))
	x2 = int(x0 - 1000*(-b))
	y2 = int(y0 - 1000*(a))

	cv2.line(gray,(x1,y1),(x2,y2),(255,255,255),2)
	#ty cary ani rohy pak do toho img nevykreslovat
	#by zbytecne kazily ten priklad
	#cv2.line(img, (x1, y1), (x2, y2), (0,0,255),2)

#v cernobilym vobrazku udelam detekci rohu
#hledat rohy rovnou v tim edges (udelat akorat canny)
#a nehledat primky by se mozna taky dalo
#ale tohle vychazi pro to orig2.png lepsi
corners = cv2.goodFeaturesToTrack(gray,30,0.01,10)
corners = np.int0(corners)

#najdu ctyri rohy podle kterejch vobrazek vyrovnam
top_left = min(corners, key = lambda p: p[0][0] + p[0][1])
print top_left

bottom_right = max(corners, key = lambda p: p[0][0] + p[0][1])
print bottom_right

top_right = max(corners, key = lambda p: p[0][0] - p[0][1])
print top_right

bottom_left = min(corners, key = lambda p: p[0][0] - p[0][1])
print bottom_left

#vyrovnam vobrazek ze ctyri body kde byly detekovany rohy
#budou v rozich vobrazku
rows, cols, ch = img.shape

pts1 = np.float32([top_left,bottom_left,top_right,bottom_right])
pts2 = np.float32([[0,0],[0,rows],[cols,0],[cols,rows]])

M = cv2.getPerspectiveTransform(pts1,pts2)
dst = cv2.warpPerspective(img,M,(rows,cols))

#trosku voriznuti
dst = dst[50:400, 50:400]

#ve vyrovnamym vobrazku vobtahnu kontury (napsanej priklad)
#ty prahy 100,200 sou asi moc, 60,200 vychazi lip
#u tech kontur bude potreba nak voriznout ty zbytky ty tabule po
#ty transformaci
canny_output = cv2.Canny(dst, 60,200)
contours, hierarchy = cv2.findContours(canny_output,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(dst,contours,-1,(255,255,255),1)

#vysype nalezeny kontury do souboru aby to vodpovidalo
#tomu scgink formatu
#tohle dobry v tom smyslu, ze ten format seshat sezere
#jinak ale to vyhodi nesmysly, jednak protoze tam
#sou ty = bez druhy strany a jednak sou to proste kontury
#a ne ty tahy jakoby
img_name = image_path.split('/')[-1:][0].split('.')[0]
path_scgink = "seshat/SampleMathExps/{}.scgink".format(img_name)
with open(path_scgink, 'w') as ink_file:
	ink_file.write("SCG_INK\n")
	ink_file.write("{}\n".format(len(contours)))
	for contour in contours:
		ink_file.write("{}\n".format(len(contour)))
		for coord in contour:
			ink_file.write("{} {}\n".format(coord[0][0], coord[0][1]))

#zakreselni bodu jen pro nazornost
for i in corners:
	x,y = i.ravel()
	cv2.circle(img,(x,y),4,80,-1)

for i in top_left, top_right, bottom_left, bottom_right:
	x,y = i.ravel()
	cv2.circle(img,(x,y),4,255,-1)



#jo a taky se mu nelibi kdyz to nevolam z ty slozky seshat ale z ty vo jednu vejs
#asi kvuli nakejm cestam nebo neco takovyho

cv2.imshow('dst', dst) #dst je uz vyrovnanej vobrazek, sou v nem teda este vykreselny primky a rohy
cv2.imshow('img', img) #puvodni vobrazek kde sou doplneny primky a rohy
cv2.waitKey()

