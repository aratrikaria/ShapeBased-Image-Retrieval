import ImageFilter
import tkFileDialog
import sqlite3 as lite
from Tkinter import *
root=Tk()

def uploadfile() :
    global a
    a=tkFileDialog.askopenfilename()


def convexhull():
    
    import cv2
    import numpy as np
    import Image
    global ext
    global a
    ext=".jpg"
        
    def thresh_callback(thresh):
        edges = cv2.Canny(blur,thresh,thresh*2)
        drawing = np.zeros(img.shape,np.uint8)     # Image to draw the contours
        contours,hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            hull = cv2.convexHull(cnt)
            cv2.drawContours(drawing,[cnt],0,(0,255,0),2)   # draw contours in green color
            cv2.drawContours(drawing,[hull],0,(0,0,255),2)  # draw contours in red color
            cv2.imshow('output',drawing)
            cv2.imshow('input',img)
            cv2.imwrite('sad.jpg',drawing)

    img = cv2.imread(a)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)

    cv2.namedWindow('input')

    thresh = 100
    max_thresh = 255

    cv2.createTrackbar('canny thresh:','input',thresh,max_thresh,thresh_callback)

    thresh_callback(0)

    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()

def harris():
    import cv
    import math
    global a
    imcolor = cv.LoadImage('leaf1.jpg')
    image = cv.LoadImage('leaf1.jpg',cv.CV_LOAD_IMAGE_GRAYSCALE)
    cornerMap = cv.CreateMat(image.height, image.width, cv.CV_32FC1)
    # OpenCV corner detection
    cv.CornerHarris(image,cornerMap,3)

    pts = []
    print "one"
    for y in range(0, image.height):
     for x in range(0, image.width):
      harris = cv.Get2D(cornerMap, y, x) # get the x,y value
      
      # check the corner detector response
      if harris[0] > 10e-06:
    ##   print x
    ##   print y
       # draw a small circle on the original image
       cv.Circle(imcolor,(x,y),2,cv.RGB(155, 0, 25))
       pts.append((x,y))


    ang = []
    for i in range(1,len(pts)-2):
        x1 = float(pts[i-1][0])
        y1 = float(pts[i-1][1])
        x2 = float(pts[i][0])
        y2 = float(pts[i][1])
        try:
            s1 = (y2-y1)/(x2-x1)
        except:
            pass
        
        x1 = float(pts[i][0])
        y1 = float(pts[i][1])
        x2 = float(pts[i+1][0])
        y2 = float(pts[i+1][1])
        try:
            s2 = (y2-y1)/(x2-x1)        
        except:
            pass
        
        ang.append(abs(math.atan(s2-s1)))


    imcolor = cv.LoadImage(a)
    image = cv.LoadImage(a,cv.CV_LOAD_IMAGE_GRAYSCALE)
    cornerMap = cv.CreateMat(image.height, image.width, cv.CV_32FC1)
    # OpenCV corner detection
    cv.CornerHarris(image,cornerMap,3)

    pts = []
    print "one"
    for y in range(0, image.height):
     for x in range(0, image.width):
      harris = cv.Get2D(cornerMap, y, x) # get the x,y value
      
      # check the corner detector response
      if harris[0] > 10e-06:
    ##   print x
    ##   print y
       # draw a small circle on the original image
       cv.Circle(imcolor,(x,y),2,cv.RGB(155, 0, 25))
       pts.append((x,y))


    ang1 = []
    for i in range(1,len(pts)-2):
        x1 = float(pts[i-1][0])
        y1 = float(pts[i-1][1])
        x2 = float(pts[i][0])
        y2 = float(pts[i][1])
        try:
            s1 = (y2-y1)/(x2-x1)
        except:
            pass
        
        x1 = float(pts[i][0])
        y1 = float(pts[i][1])
        x2 = float(pts[i+1][0])
        y2 = float(pts[i+1][1])
        try:
            s2 = (y2-y1)/(x2-x1)        
        except:
            pass
        
        ang1.append(abs(math.atan(s2-s1)))

    ind = min(len(ang),len(ang1))
    print ind

    val = 0
    for i in range(0,ind):
        val += ang[i] - ang1[i]

    print val
    if val <=0:
        print 'images are similar...'
        exit()
    else:
        print "Different Images"
        exit()

   

Button(root,text="Upload ",command=uploadfile).grid(row=1,column=2)
Button(root,text="Find Convex Hull",command=convexhull).grid(row=2,column=2)
Button(root,text="Find Key Point",command=harris).grid(row=3,column=2)
root.mainloop()
