from threading import Thread

import cv2
import numpy as np
import self as self

cap = cv2.VideoCapture(0)
centrePoint = 317.5
width = 1000 #Default value is 500
height = 500 #Default value
radius = 0
maxRadius = 0
class CameraStart:
    def __init__(self):
        print("Initialising Camera")
        ret, img = cap.read()
        self.centre = 0
        self.radius = 0
        self.maxRadius = 0
        self.maxKey = 0

    def start(self):
        print("Starting Camera Thread")
        t = Thread(target=self.update,args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while True:
            ret, img = cap.read()
            edged = cv2.Canny(img, 50, 100)
            edged = cv2.dilate(img, None, iterations=1)
            edged = cv2.erode(img, None, iterations=1)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            low = np.array([0, 50, 50])
            high = np.array([10, 255, 255])
            mask1 = cv2.inRange(hsv, low, high)
            self.imgmoments = cv2.moments(mask1, True)
            lower_red = np.array([170, 50, 50])
            upper_red = np.array([180, 255, 255])
            redmask2 = cv2.inRange(hsv, lower_red, upper_red)
            redmask = mask1 + redmask2
            mask = cv2.morphologyEx(redmask, cv2.MORPH_OPEN, np.ones((5, 5)))
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((20, 20)))
            contour = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            max_cont = cv2.contourArea(contour[0])
            max_cont = max(contour, key=cv2.contourArea)
            for i in range(len(contour)):
                x, y, w, h = cv2.boundingRect(max_cont)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            croppedk = img[y:y + h, x:x + w]

            # cv2.imshow('Red_Mask:', mask)
            cv2.imshow('Original', img)
            cnt_r = 0
            for r in redmask:
                cnt_r = cnt_r + list(r).count(255)
            print ("Redness ", cnt_r)
            lower_green = np.array([50, 50, 50])
            upper_green = np.array([70, 255, 255])
            greenmask = cv2.inRange(hsv, lower_green, upper_green)
            # cv2.imshow('Green_Mask:', greenmask)
            cnt_g = 0
            for g in greenmask:
                cnt_g = cnt_g + list(g).count(255)
            print ("Greenness ", cnt_g)
            lower_yellow = np.array([20, 50, 50])
            upper_yellow = np.array([30, 255, 255])
            yellowmask = cv2.inRange(hsv, lower_yellow, upper_yellow)
            # cv2.imshow('Yellow_Mask:', yellowmask)
            cnt_y = 0
            for y in yellowmask:
                cnt_y = cnt_y + list(y).count(255)
            print ("Yellowness ", cnt_y)
            center = None
            if len(contour) > 0:
                c = max(contour, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                self.radius = radius
                self.imgmoments = cv2.moments(c)
                self.center = (
                    int(self.imgmoments["m10"] / self.imgmoments["m00"]),
                    int(self.imgmoments["m01"] / self.imgmoments["m00"]))
            if radius > 10:
                cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(img, self.center, 3, (0, 0, 255), -1)
                cv2.putText(img, "centroid", (self.center[0] + 10, self.center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                            (0, 0, 255), 1)
                cv2.putText(img, "(" + str(self.center[0]) + "," + str(self.center[1]) + ")",
                            (self.center[0] + 10, self.center[1] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            return self.maxRadius

    def returnMonments(self):
        return self.imgmoments

    def returnXPos(self):
        return self.centre

    def stopSteam(self):
        cap.release()



cam = CameraStart().start()
try:
    if __name__== '__main__':
        while True:
            cam.update()
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                print("Exiting Quality Checker ")
                break

except KeyboardInterrupt:
    print("Quality Checker interrupted")
finally:
    print("Exiting Quality Checker")
    #stop()

cap.release()
cv2.destroyAllWindows()
