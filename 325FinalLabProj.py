#!/usr/bin/python

#Final Lab Project
#Melissa Van Baren
#Isaac Rai
#Daniel Wartella

print("Hello World")
#helpful: how to do object detection with opencv [live] on youtube by a siraj


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
  frame = imutils.resize(frame, width=1600)
  
  #Blurs frame to remove noise: size of the kernel is 11,11 and standard deviation
  blurred_frame = cv2.GaussianBlur(frame, (11,11), 0)
  
  #Convert frame to HSV
  hsv_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
  
  #Mask for the upper/lower color bounds
  mask = cv2.inRange(hsv_frame, lower_color, upper_color)
  

