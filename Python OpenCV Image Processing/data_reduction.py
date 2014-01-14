import os
import glob
import Image
import cv2
import numpy as np
import math
from termcolor import colored
import ImageDraw

boundaries = np.empty
for infile in glob.glob( os.path.join("gestures", '*.jpg') ):
	print colored("Reading Image: " + infile, 'red')
	im = cv2.imread(infile)
	imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

	##Create binary images
	ret, thresh = cv2.threshold(imgray,127,255,0)

	##Save binary images
	binaryImage = Image.fromarray(thresh)
	binaryImage.save("binary_image_" + infile)

	##Find boundaries of objects from binary images
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(im,contours,-1,(0,255,0),3)

	##Average the contours and calculate the center
	count = 0;
	xValue = 0;
	yValue = 0;
	for layers in contours:
		for demensions in layers:
			for values in demensions:
				xValue += values[0]
				yValue += values[1]
				count += 1
	xCenter = xValue / count
	yCenter = yValue / count
	cv2.circle(im,(xCenter, yCenter),5,(0,0,255),3)

	##Save image with contours, defects and centers
	IplImage = Image.fromarray(im)
	IplImage.save("boundary_center_" + infile)

	##Build a numpy array with contours from all layers
	boundaries = contours[0]
	for layers in contours:
		if len(boundaries) != len(layers):
			boundaries = np.vstack((boundaries, layers))
	
	##Draw bounding Box
	#hull = cv2.convexHull(boundaries)
	x,y,w,h = cv2.boundingRect(boundaries)
	cv2.rectangle(im,(x,y),(x+w,y+h),(127,127,0),2)
	boundingRect = w*h
	cv2.circle(im,(x+w/2, y+h/2),4,[127,127,0],2)


	##Distance from the center of bounding box to the center of coutour
	distanceToCenter = math.sqrt(((x+w/2) - xCenter)*((x+w/2) - xCenter) + ((y+h/2) - yCenter)*((y+h/2) - yCenter))
	
	##[TEST]Print the distance between two centers
	print distanceToCenter

	##Find convex hull and convexity defects for boundaries of objects
	hull = cv2.convexHull(boundaries,returnPoints = False)
	defects = cv2.convexityDefects(boundaries,hull)

	defectPointCount = 0
	for i in range(defects.shape[0]):
	    s,e,f,d = defects[i,0]
	    if d >= 1000:
		    start = tuple(boundaries[s][0])
		    end = tuple(boundaries[e][0])
		    far = tuple(boundaries[f][0])
		    cv2.line(im,start,end,[255,0,0],2)
		    cv2.circle(im,far,4,[255,0,255],-1)
		    if d >= 10000:
		    	defectPointCount += 1
	
	##[TEST]Print the number of defect points
	print "Number of Defect Points: " + str(defectPointCount)
		    ##[TEST]Print the distance from defect point to the contour and the size of the bounding rectangle
	if infile == "gestures/fist_center.jpg":
		print "Size of Bounding Rectangle: " + str(boundingRect)
	if infile == "gestures/horizontal.jpg":
		print "Size of Bounding Rectangle: " + str(boundingRect)
	if infile == "gestures/open_palm.jpg":
		print "Size of Bounding Rectangle: " + str(boundingRect)
	if infile == "gestures/thumb_up.jpg":
		print "Size of Bounding Rectangle: " + str(boundingRect)
		    # 	print "Size of Bounding Rectangle: " + str(boundingRect)
		    # if infile == "gestures/fist_left_bottom.jpg":
		    # 	print "Size of Bounding Rectangle: " + str(boundingRect)
		    # if infile == "gestures/fist_left_up.jpg":
		    # 	print "Size of Bounding Rectangle: " + str(boundingRect)
		    # if infile == "gestures/fist_right_bottom.jpg":
		    # 	print "Size of Bounding Rectangle: " + str(boundingRect)
		    # if infile == "gestures/fist_right_up.jpg":
		    # 	print "Size of Bounding Rectangle: " + str(boundingRect)
		    # if infile == "gestures/open_palm.jpg":
		    # 	print "Size of Bounding Rectangle: " + str(boundingRect)
	
	##[TESTING RESULT]Print the analyzing results
	if defectPointCount >= 5 and boundingRect >= 45000:
		print colored("[RESULT] Hand Gesture is more like a --> Open Palm", "blue")
	elif defectPointCount <= 5 and 19000 <= boundingRect < 35000:
		print colored("[RESULT] Hand Gesture is more like a --> Thumb Up", "blue")
	elif defectPointCount <= 5 and 10000 <= boundingRect < 19000:
		print colored("[Result] Hand Gesture is more like a --> Fist", "blue")
	elif defectPointCount <= 5 and boundingRect < 10000:
		print colored("[Result] Hand Gesture is more like a --> Horizontal Palm", "blue")
	else:
		print "Opps I don't understand this gesture"

	##Save image with contour, defects, two centers and bounding box
	IplImage = Image.fromarray(im)
	IplImage.save("analyzed_" + infile)