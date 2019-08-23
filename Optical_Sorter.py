import cv2
import numpy as np
import serial
import time


ser = serial.Serial('COM9',9600,timeout=0.5)

time.sleep(2)

# capturing video through webcam
cap = cv2.VideoCapture(1)

font = cv2.FONT_HERSHEY_COMPLEX

while (1):
    _, img = cap.read()
    img = cv2.flip(img, 1)
    f = 0
    rect = img[50:350, 150:480]

    cv2.rectangle(img, (150,50), (480,350), (0,0,255),0)
    # converting frame(img i.e BGR) to HSV (hue-saturation-value)
    hsv = cv2.cvtColor(rect, cv2.COLOR_BGR2HSV)

    # defining the Range of Blue color
    blue_lower = np.array([99, 115, 160], np.uint8)
    blue_upper = np.array([110, 255, 255], np.uint8)

    # defining the Range of yellow color
    yellow_lower = np.array([22, 60, 160], np.uint8)
    yellow_upper = np.array([31, 255, 255], np.uint8)

    green_lower = np.array([46, 36, 128], np.uint8)
    green_upper = np.array([72, 255, 255], np.uint8)

   # finding the range of red,blue and yellow color in the image
   # red = cv2.inRange(hsv, red_lower, red_upper)
    blue = cv2.inRange(hsv, blue_lower, blue_upper)
    yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
    green = cv2.inRange(hsv, green_lower, green_upper)

    # Morphological transformation, Dilation
    kernal = np.ones((5, 5), "uint8")



    blue = cv2.dilate(blue, kernal)
    res1 = cv2.bitwise_and(rect, rect, mask=blue)

    yellow = cv2.dilate(yellow, kernal)
    res2 = cv2.bitwise_and(rect, rect, mask=yellow)

    green = cv2.dilate(green, kernal)
    res3 = cv2.bitwise_and(rect, rect, mask=green)


    # Tracking the Blue Color
    contours, hierarchy = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours): #ASK
        area = cv2.contourArea(contour)
        if (area > 10000):
            x, y, w, h = cv2.boundingRect(contour)
            #rect = cv2.rectangle(rect, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(rect, "Blue color", (x-50, y+200), cv2.FONT_HERSHEY_SIMPLEX, 1.50, (255, 0, 0))
            print(area)


    # Tracking the yellow Color
    contours, hierarchy = cv2.findContours(yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 12000):
            x, y, w, h = cv2.boundingRect(contour)
            #rect = cv2.rectangle(rect, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(rect, "yellow  color", (x-50, y+200), cv2.FONT_HERSHEY_SIMPLEX, 1.50, (0, 0, 255))
            print(area)

    # Tracking the green Color
    contours, hierarchy = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 12000):
            x, y, w, h = cv2.boundingRect(contour)
           # rect = cv2.rectangle(rect, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(rect, "Green  color", (x-50, y+200), cv2.FONT_HERSHEY_SIMPLEX, 1.50, (0, 0, 255))
            print(area)


    contours, _ = cv2.findContours(yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) >= 12000:
            approx = cv2.approxPolyDP(cnt, 0.025 * cv2.arcLength(cnt, True), True)
            cv2.drawContours(img, [approx], 0, (0), 5)
            x = approx.ravel()[0]
            y = approx.ravel()[1]
            if len(approx) > 0 and len(approx) < 7:
                cv2.putText(rect, "Rectangle", (x-20, y), font, 1, (255,0,0))
                ser.write(str(5))
                print("yellow rec 75")
                f = 1 
            elif len(approx)  >=7:
                cv2.putText(rect, "Circle", (x-20, y), font, 1, (255,0,0))
                ser.write(str(4))
                print("yellow circle 60")
                f = 1 
            
                
                
    
    contours, _ = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) >= 10000:
            approx = cv2.approxPolyDP(cnt, 0.025 * cv2.arcLength(cnt, True), True)
            cv2.drawContours(img, [approx], 0, (0), 5)
            x = approx.ravel()[0]
            y = approx.ravel()[1]
            if len(approx) > 0 and len(approx) < 7:
                cv2.putText(rect, "RectBangle", (x-20, y), font, 1, (255,0,0))
                ser.write(str(2))
                print("blue rec 30")
                f = 2
            
            elif len(approx)>= 7:
                cv2.putText(rect, "Circle", (x-20, y), font, 1, (255,0,0))
                ser.write(str(1))
                print("blue circle 15")
                f = 2
                
               

    contours, _ = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) >= 12000:
            approx = cv2.approxPolyDP(cnt, 0.025 * cv2.arcLength(cnt, True), True)
            cv2.drawContours(img, [approx], 0, (0), 5)
            x = approx.ravel()[0]
            y = approx.ravel()[1]
            
            if len(approx) > 0 and len(approx) < 6:
                cv2.putText(rect, "Rectangle", (x-20, y), font, 1, (255,0,0))
                print("green rectangle 45")
                ser.write(str(3))
                f=3
            elif len(approx) >= 6:
                cv2.putText(rect, "Circle", (x-20, y), font, 1, (255,0,0))
                print("green circle 90")
                ser.write(str(6))
                f=3
    if f>0 :
      time.sleep(2.5)
      f=0
    
    

    
    cv2.imshow('Original', img)
   # cv2.imshow('RECT', rect)
    k = cv2.waitKey(5)
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()