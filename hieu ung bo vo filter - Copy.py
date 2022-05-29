import numpy as np
import cv2
import random
import glob
import os
from PIL import Image, ImageOps
ngang=1000
doc=600

#Tạo ra mask dựa vào cái points đa giác đã đánh dấu
def applyPTS(pts):
    mask = np.zeros((doc,ngang), np.uint8)
    cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)
    mask=np.stack([mask] * 3, axis=2)
    return mask

#Apply cur vào ảnh pre dựa vào mask
def putMask(cur,pre,mask):
    dst = np.copy(pre)
    np.putmask(dst,mask,cur)
    return dst

#chuyển đổi định dạng của PIL sang NP
def PILtoCV(img):
    img = np.array(img)
    #img=img[::,::,::-1]
    return img
#Chuyển ngược lại
def CVtoPIL(img):
    img = Image.fromarray(img, 'RGB')
    return img
#Mở file bằng cv2
def openAsCV(filename):
    image=cv2.imread(filename)
    image=cv2.resize(image,(ngang,doc))
    return image
#mở file bằng PIL
def openAsPIL(filename):
    image=Image.open(filename)
    image=image.resize((ngang,doc))
    return image
#Xoay góc box ảnh 180 
def applyBox(image,box):
    image=CVtoPIL(image)
    sub_image = image.crop(box).rotate(180)
    image.paste(sub_image, box[0:2])
    image=PILtoCV(image)
    return image
def main(): 
    prev_image=np.zeros((doc,ngang,3), dtype=np.uint8)
    img=[]
    path=(__file__)
    path=path.replace("hieu ung bo vo filter - Copy.py","")
    filenames = glob.glob(path+"*.png")
    for filename in filenames:
        img.append(openAsCV(filename))
    for image in img:
        rand=4#random.randint(1,4)    
        #1 Trai qua phai tren xuong duoi
        #2 Trai qua phai duoi len tren
        #3 Phai qua trai tren xuong duoi
        #4 Phai qua trai duoi len tren
        #mirror=CVtoPIL(image)
        for i in range(100):
            #Xác định vị trí tâm xoay hiện tại
            curDoc=round(doc*i/100)
            curNgang=round(ngang*i/100)
            #Tạo box, pts dựa vào chiều            
            if(rand==1):   
                pts = np.array([[0,curDoc],[curNgang,0],[0,0]])
                box=(0,0,curNgang,curDoc)
            if(rand==2):
                pts = np.array([[0,doc-curDoc],[curNgang,doc],[0,doc]])
                box=(0,doc-curDoc,curNgang,doc)
            if(rand==3):
                pts = np.array([[ngang,curDoc],[ngang-curNgang,0],[ngang,0]])
                box=(ngang-curNgang,0,ngang,curDoc)
            if(rand==4):
                pts = np.array([[ngang,doc-curDoc],[ngang-curNgang,doc],[ngang,doc]])
                box=(ngang-curNgang,doc-curDoc,ngang,doc)
            #tạo mask
            mask=applyPTS(pts)
            #xoay ảnh 90 độ dựa vào box
            temp=applyBox(prev_image,box)
            #đặt image vào ảnh trước theo mask
            dst=putMask(image,temp,mask)
            cv2.imshow("croped.png", dst)
            cv2.waitKey(10)    
        for i in range(100):
            #Xác định vị trí tâm xoay hiện tại            
            curDoc=round(doc*i/100)
            curNgang=round(ngang*i/100)
            #Tạo box, pts dựa vào chiều
            if(rand==1):
                pts = np.array([[ngang,curDoc],[curNgang,doc],[ngang,doc]])
                box=(curNgang,curDoc,ngang,doc)
            if(rand==2):
                pts = np.array([[ngang,doc-curDoc],[curNgang,0],[ngang,0]])
                box=(curNgang,0,ngang,doc-curDoc)
            if(rand==3):
                pts = np.array([[0,curDoc],[ngang-curNgang,doc],[0,doc]])
                box=(0,curDoc,ngang-curNgang,doc)
            if(rand==4):
                pts = np.array([[0,doc-curDoc],[ngang-curNgang,0],[0,0]])
                box=(0,0,ngang-curNgang,doc-curDoc)
            
            mask=applyPTS(pts)
            temp=applyBox(prev_image,box)
            dst=putMask(temp,image,mask)
            cv2.imshow("croped.png", dst)
            cv2.waitKey(10)
        prev_image=image
main()