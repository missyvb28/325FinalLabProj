#!/usr/bin/python

#Final Lab Project
#Melissa Van Baren
#Isaac Rai
#Daniel Wartella

from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
 
#upper/lower bounds
#lower_color= (29, 86, 6)
#upper_color = (64, 255, 255)
upper_color = (174, 223, 255)
lower_color = (125, 106, 91)
 
#argument parse
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
args = vars(ap.parse_args())
 
if not args.get("video", False):
  vs = VideoStream(src=0).start()
else:
  vs = cv2.VideoCapture(args["video"])
 
#Keep looking until quiting
while True:
  #Grabs the current frame that is being used
  frame = vs.read()
  
  #If the frame is not successfuly read, break from the loop
  if frame is None:
    break
  
  #Resizes frame to desired width
  frame = imutils.resize(frame, width=600)
  
  #Blurs frame to remove noise: size of the kernel is 11,11 and standard deviation
  blurred_frame = cv2.GaussianBlur(frame, (11,11), 0)
  
  #Convert frame to HSV
  hsv_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
  
  #Mask for the upper/lower color bounds
  mask = cv2.inRange(hsv_frame, lower_color, upper_color)
  
  #Erosion
  mask = cv2.erode(mask, None, iterations=2)
  
  #Dilation
  mask = cv2.dilate(mask, None, iterations=2)
 
  #array of contours
  #takes in masked image, takes out child contours, removes redundant points, and compresses the contours
  contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  
  #Validates OpenCV giving contours
  if imutils.is_cv2():
    contours = contours[0]
  else:
    contours = contours[1]
 
  #if statement to find an existing contour
  if len(contours) > 0:
    #Calculates the centroid of the max contour
    centroid = max(contours, key=cv2.contourArea)
    
    #Finds the x, y, and radius of the max contour
    ((x, y), radius) = cv2.minEnclosingCircle(centroid)
    
    #Output x and y coordinates
    #print(int(x), int(y))
    
 	#Process to draw rectangle around tracked object
    if radius > 5:
      #Draws a yellow rectangle around tracked object
      cv2.rectangle(frame, (int(x)-int(radius), int(y)-int(radius)),(int(x)+int(radius), int(y)+int(radius)), (0, 255, 255), 6)
      #Outputs text "ACTIVE"
      cv2.putText(frame, 'TRACKING SYSTEM: ACTIVE', (10,650), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
    else:
        #Outputs text "INACTIVE" since the radius of the contour is too small to read
      cv2.putText(frame, 'TRACKING SYSTEM: INACTIVE', (10,650), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
  else:
    #Outpus text "INACTIVE" since no contours are read
    cv2.putText(frame, 'TRACKING SYSTEM: INACTIVE', (10,650), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
 
  #Shows the current frame to the screen
  cv2.imshow("Live Video", frame)
 
  #Shows the HSV frame
  #cv2.imshow("HSV", mask)
 
  #If q is pressed, the video stream stops
  if cv2.waitKey(1) == ord("q"):
    break
 
if not args.get("video", False):
  vs.stop()
else:
  vs.release()
 
cv2.destroyAllWindows()
