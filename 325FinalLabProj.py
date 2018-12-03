#Final Lab Project
#Melissa Van Baren
#Isaac Rai
#Daniel Wartella

print("Hello World")
#helpful: how to do object detection with opencv [live] on youtube by a siraj

#import statements
import numpy as np
import cv2
import imutils
import argparse
from imutils.video import VideoStream

#video port
cap = cv2.VideoCapture(0)

#RGB values
# dark orange [16,100,68.6]
# light orange [18,75.1,96.1]
DarkOrng = np.array(min_org, cv2.COLOR_RGB2HSV)
LightOrng = cv2.cvtColor(max_org, cv2.COLOR_RGB2HSV)

while True:
	ret, frame = cap.read()
	#name of window and making window
	#cv2.imshow('frame',frame)
	
	#get the current frame from the camera
	frame = vs.read()

	#handling the video stream
	if args.get("Video", False):
		frame = frame[1] #if there's no video feed
	else:
		frame = frame #if there is video feed

	#if the frame isn't successfully read, then quit
	if frame is None:
		break

	#resize the frame
	frame.imutils.resize(frame, width=600)

	#blur the frame, smooth out color variations
	blurred_frame = cv2.GaussianBlur(frame, (11,11), 0)

	#convert frame to HSV (Hue Saturation Value)
	hsv_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

	#mask the frame to find the puck w/in the upper/lower color bounds
	mask = cv2.inRange(hsv, DarkOrng, LightOrng)

	#erode everything else
	mask = cv2.erode(mask, None, iterations=2)

	#dilation
	mask = cv2.dilate(mask, None, iterations=2)

	contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	#validates OpenCV giving us contours
	if imutils.is_cv2():
		contours = contours[0]
	else:
		contours = contours[1]

	#center of the object
	center = None

	#find an existing contour
	if len(contours) > 0:
		centroid = max(contours, key = cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(centroid)
		moment = cv2.moments(centroid)

		#find the coordinates of the center
		center = (int(moment["m10"] / moment["m00"]), int(moment["m01"] / moment["m00"]))

	#draw a rectangle around the object being tracked
	if radius > 10:
		#draw yellow rectangle
		cv2.rectangle(frame, (int(x), int(y)), int(radius), (0,0,255), thickness = 3)
		#draw a purple line following the object
		cv2.circle(frame, center, 5, (204, 0, 102), -1)

	#display current frame on screen
	cv2.imshow("frame", frame)

	#to quit window, press q
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
