import cv2
import numpy as np
from pynput.mouse import Button,Controller
import tkinter as tk
mouse=Controller()
root = tk.Tk()
sx= root.winfo_screenwidth()
sy= root.winfo_screenheight()
(comx,comy)=(320,240)
lowerBound=np.array([33,80,40])
uperBound=np.array([102,255,255])
com=cv2.VideoCapture(0)
com.set(3,comx)
com.set(4,comy)
kernalopen=np.ones((8,8))
kernelclose=np.ones((20,20))

currmou=0
while 1:
	ret,img=com.read()
        
	img=cv2.resize(img,(340,220))
	imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	mask=cv2.inRange(imgHSV,lowerBound,uperBound)
	maskopen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernalopen)
	maskclose=cv2.morphologyEx(maskopen,cv2.MORPH_OPEN,kernelclose)
	maskfinal=maskclose
	conts,h=cv2.findContours(maskfinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	cv2.drawContours(img,conts,-1,(255,0,0),3)
	if(len(conts)==2):
		if currmou==1:
		      mouse.release(Button.left)
		      currmou=0
		x1,y1,w1,h1=cv2.boundingRect(conts[0])
		x2,y2,w2,h2=cv2.boundingRect(conts[1])
		cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(0,255,0),2)
		cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(0,255,0),2)
		cx0=(x1+w1)//2
		cy0=(y1+h1)//2
		cx1=(x2+w2)//2
		cy1=(y2+h2)//2
		cx=(cx0+cx1)//2
		cy=(cy0+cy1)//2
		cv2.line(img,(cx0,cy0),(cx1,cy1),(255,0,0),2)
		cv2.circle(img,(cx,cy),2,(0,0,225),2)
		mouse.position=(sx-(cx*sx//comx),cy*sy//comy)
		while mouse.position!=(sx-(cx*sx//comx),cy*sy//comy):
			pass
	elif(len(conts)==1):
		x,y,w,h=cv2.boundingRect(conts[0])
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		cx=(x+w)//2
		cy=(y+h)//2
		cv2.circle(img,(cx,cy),(w+h)//4,(0,0,225),2)
		mouse.position=(sx-(cx*sx//comx),cy*sy//comy)
		while mouse.position!=(sx-(cx*sx//comx),cy*sy//comy):
			pass
		mouse.press(Button.left)
		currmou=1
	cv2.imshow("cam",img)
	cv2.waitKey(5)
