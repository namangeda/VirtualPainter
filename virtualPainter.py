from cv2 import cv2
import numpy as np



livecap = cv2.VideoCapture(0)

"""   
     a markel with blue holder sholud be used as pen
     
     you can choose marker with any holder color but for that than you may find
     these values from detectColorWebCam.py
     then fill those values in min ans max lists
     listed below                                          
                                                                """


min = [60, 148, 51]      #these are min hue, sat and val values for blue color            
max = [116, 255, 255]    #these are max hue, sat and val values for blue color 
frameWidth = 600
frameHeight = 400
livecap.set(3, 400)      
livecap.set(4, 600)
livecap.set(10, 100)        #brightness 100

points = []
def stackImages(scale,imgArray):       # function to stack images including gray images and to scale them down
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver



def getContour(img):
    
    contours,hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cntr in contours:
        area = cv2.contourArea(cntr)
        if area > 300:
            cv2.drawContours(imgContour, cntr, -1, (0,255,0), 1)
            perimeter = cv2.arcLength(cntr, True)
            approx = cv2.approxPolyDP(cntr, 0.01*perimeter, True)
            x,y,w,h = cv2.boundingRect(approx)
            points.append([x+w//2, y])
            cv2.circle(imgContour, (x+w//2, y), 10, (255, 0, 0), cv2.FILLED)



while True:
    success, img = livecap.read()
    imgContour = img.copy()
    
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([75, 117, 102])
    upper = np.array([115, 255, 255])
    mask = cv2.inRange(imgHSV,lower,upper)
    imgResult = cv2.bitwise_and(img,img,mask=mask)
    imgCanny = cv2.Canny(imgResult, 50, 50)
    getContour(imgCanny)
    print(len(points))
    for p in points:
        cv2.circle(imgContour, (p[0], p[1]), 10, (255, 0, 0), cv2.FILLED)
    imgstack = stackImages(0.7, ([img, imgHSV, imgResult],
                                  [imgCanny, imgContour, mask]))
    cv2.imshow("stacked images", imgstack)    
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
