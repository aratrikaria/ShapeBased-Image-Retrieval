import ImageFilter
import tkFileDialog
import sqlite3 as lite
from Tkinter import *
root=Tk()
flag=0
c=0
def uploadfile() :
    global a
    a=tkFileDialog.askopenfilename()
  
def contour() :
    import Image
    global a
    global ext
    ext=".jpg"
    print a
    a1=a.split("/")
    print a1
    #imageFile = a
    im1 = Image.open(a)
    def filterContour(im):
    
        im1 = im.filter(ImageFilter.CONTOUR)
    
        im1.save("CONTOURfunc" + ext)

    filterContour(im1)

def findedges() :
    import Image
    global ext
    global a
    ext=".jpg"
    #imageFile = a
    im1 = Image.open(a)
    def filterFindEdges(im):
    
        im1 = im.filter(ImageFilter.FIND_EDGES)
    
        im1.save("EDGESfunc" + ext)

    filterFindEdges(im1)

def edgematch() :
    from PIL import Image
    import ImageFilter
    xyz=1
    i1=0
    im1 = Image.open(a)
    original = im1
    db = {}
    while(xyz==1):
        i1+=1
        print i1
        global ext
        ext=".png"
        con = lite.connect('iem.sql')
        cur = con.cursor()
        res = cur.execute('select data from frames')
        imgs = []

        for row in res:
            imgs.append(row[0]+'.png')
        for imgg in imgs:
            print imgg
            count=0
            while count < 4:
                try:
                    im = Image.open(imgg)
                except IOError:
                    print "failed to identify", file
                else:
                    if im.info.has_key("description"):
                        print "image description:", im.info["description"]
                import numpy
                data = numpy.asarray(im)
                data1 = numpy.asarray(im1)
                c=0
                s=0
                p=1
                print data1[0,0]
                print len(data1[0,0])
                print data[0,0]
                print len(data)
    ##            if(data[0,0][1]!=data1[0,0][1]):
    ##                print "ok"
                data2=[]
                diff=[]
                y=[]
                try:
                    for i in range(0,len(data)):
                        for j in range(0,len(data)):
                            for k in range(0,3):
                                s+=1
                                if(data[i,j][k]!=data1[i,j][k]):
                                    c+=1
                                    if (data[i,j][0]>=data1[i,j][0]):
                                        r1=data[i,j][0]
                                        r2=data1[i,j][0]
                                    else:
                                        r1=data1[i,j][0]
                                        r2=data[i,j][0]
                                    if (data[i,j][1]>=data1[i,j][1]):
                                        g1=data[i,j][1]
                                        g2=data1[i,j][1]
                                    else:
                                        g1=data1[i,j][1]
                                        g2=data[i,j][1]
                                    if (data[i,j][2]>=data1[i,j][2]):
                                        b1=data[i,j][2]
                                        b2=data1[i,j][2]
                                    else:
                                        b1=data1[i,j][2]
                                        b2=data[i,j][2]
                                    diff.append((r1-r2)+(g1-g2)+(b1-b2))   
                                    data2.append(str([i,j]))                                
                                    break
                                
                    print "unmatched: ",c/3
                    print s
                    p=c*100/3
                    print p
                    print "percentage unmatched", p/s

                    if(p==0):
                        print "similar Images"
                        xyz=2
                        db[imgg]=p/s
                        flag=1
                        break
                        
                        
                    else:
                        db[imgg]=p/s
                        for h in range(0,10):
                          #  print diff[h]
                            y.append(diff[h])
                        x=[1,2,3,4,5,6,7,8,9,10]
                        im1 = im1.rotate(90);

                        plt.xlabel("pixel number")
                        plt.ylabel("difference")
                        plt.plot(x,y)
                
                        plt.show()
                    
                except:
                    pass
                count+=1 
    print db
    if(flag==0):
        print "NO search results found"
    import cv
    for i in db.keys():
        im = cv.LoadImage(i)
        name = i+' '+str(db[i])
        if db[i] == 0:
            cv.ShowImage(name,im)
    cv.WaitKey(0)
    

    

Button(root,text="Upload",command=uploadfile).grid(row=1,column=0)
Button(root,text="Find Contour",command=contour).grid(row=1,column=2)
Button(root,text="Find Edges",command=findedges).grid(row=1,column=4)
Button(root,text="Match Images",command=edgematch).grid(row=2,column=2)
root.mainloop()
