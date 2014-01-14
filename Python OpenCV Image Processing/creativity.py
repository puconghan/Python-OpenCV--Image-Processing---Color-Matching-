import os
import glob
import Image
import cv2
import numpy as np
import math
from termcolor import colored
import ImageDraw

counterX = 320
counterY = 213
accelerator = 1
freezedFlag = False

sequence_list = ["sequence_1", "sequence_2", "sequence_3", "sequence_4", "sequence_5_failed", "sequence_6_failed", "sequence_7", "sequence_8", "sequence_9", "sequence_10_failed", "sequence_11", "sequence_12"]
targeted_result_list = ["320213print", "322216print", "321213print", "319213print", "320211print", "324213print", "320213print", "319212print", "320211print", "320210printprint", "318215print", "320213print"]
listcounter = 0

for folder in sequence_list:
	print "\n"
	print colored("Reading Folder: " + folder, 'green')
	counterX = 320
	counterY = 213
	accelerator = 1
	freezedFlag = False
	boundaries = np.empty
	for infile in glob.glob( os.path.join("sequences_of_hand_gesture_images/" + folder, '*.jpg') ):
		number_print = ""
		print colored("Reading Image: " + infile, 'red')
		im = cv2.imread(infile)
		imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

		##Create binary images
		ret, thresh = cv2.threshold(imgray,127,255,0)

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

		## Center of gesture falls into the orange center of the screen
		if (math.sqrt((320 - xCenter)*(320 - xCenter) + (213 - yCenter)*(213 - yCenter)) <= 53.25):
			##Build a numpy array with contours from all layers
			boundaries = contours[0]
			for layers in contours:
				if len(boundaries) != len(layers):
					boundaries = np.vstack((boundaries, layers))
			
			##Draw bounding Box
			#hull = cv2.convexHull(boundaries)
			x,y,w,h = cv2.boundingRect(boundaries)
			boundingRect = w*h


			##Distance from the center of bounding box to the center of coutour
			distanceToCenter = math.sqrt(((x+w/2) - xCenter)*((x+w/2) - xCenter) + ((y+h/2) - yCenter)*((y+h/2) - yCenter))

			##Find convex hull and convexity defects for boundaries of objects
			hull = cv2.convexHull(boundaries,returnPoints = False)
			defects = cv2.convexityDefects(boundaries,hull)

			defectPointCount = 0
			largestX = 0
			largestY = 0
			for i in range(defects.shape[0]):
			    s,e,f,d = defects[i,0]

			    if d >= 1000:
				    start = tuple(boundaries[s][0])
				    end = tuple(boundaries[e][0])
				    far = tuple(boundaries[f][0])
				    if math.sqrt((end[0] - far[0])*(end[0] - far[0])) > largestX:
				    	largestX = math.sqrt((end[0] - far[0])*(end[0] - far[0]))
				    if math.sqrt((end[1] - far[1])*(end[1] - far[1])) > largestY:
				    	largestY = math.sqrt((end[1] - far[1])*(end[1] - far[1]))
				    cv2.line(im,start,end,[255,0,0],2)
				    cv2.circle(im,far,4,[255,0,255],-1)
				    if d >= 10000:
				    	defectPointCount += 1
			## If statement for capturing open palm gesture in the center
			if defectPointCount >= 5 and boundingRect >= 45000:
				print colored("Location of Counter", "blue")
				print colored("Counter X:" + str(counterX), "red")
				print colored("Counter Y:" + str(counterY), "red")
				number_print = number_print + "print"
			## If statement for capturing thumb up gesture in the center
			elif defectPointCount <= 5 and 19000 <= boundingRect < 35000:
				accelerator += 1
				print "Accelerator is increased to: " + str(accelerator)
			## If statement for capturing fist gesture in the center
			elif defectPointCount <= 5 and 10000 <= boundingRect < 19000:
				if freezedFlag != True:
					print "Reset X -> 320 and Y -> 213"
					counterX = 320
					counterY = 213
				else:
					print "Counter Freezed"
			## If statement for capturing horizontal palm gesture in the center
			elif defectPointCount <= 5 and boundingRect < 10000:
				print "Counter Freezed. No further movements are allowed"
				freezedFlag = True
			else:
				print "Opps I don't understand this gesture"
		
		## Center of gesture falls into four green eccentric circle sections.
		elif (53.25 < math.sqrt((320 - xCenter)*(320 - xCenter) + (213 - yCenter)*(213 - yCenter)) <= 106.5):
			if xCenter < 320 and yCenter < 213:
				if math.sqrt((320 - xCenter)*(320 - xCenter)) > math.sqrt((213 - yCenter)*(213 - yCenter)):
					if freezedFlag != True:
						print "Left (X - " + str(accelerator) + ")"
						counterX -= accelerator
					else:
						print "Counter Freezed"
				else:
					if freezedFlag != True:
						print "Up (Y - " + str(accelerator) + ")"
						counterY -= accelerator
					else:
						print "Counter Freezed"
			elif xCenter > 320 and yCenter < 213:
				if math.sqrt((320 - xCenter)*(320 - xCenter)) > math.sqrt((213 - yCenter)*(213 - yCenter)):
					if freezedFlag != True:
						print "Right (X + " + str(accelerator) + ")"
						counterX += accelerator
					else:
						print "Counter Freezed"
				else:
					if freezedFlag != True:
						print "Up (Y - " + str(accelerator) + ")"
						counterY -= accelerator
					else:
						print "Counter Freezed"
			elif xCenter < 320 and yCenter > 213:
				if math.sqrt((320 - xCenter)*(320 - xCenter)) > math.sqrt((213 - yCenter)*(213 - yCenter)):
					if freezedFlag != True:
						print "Left (X - " + str(accelerator) + ")"
						counterX -= accelerator
					else:
						print "Counter Freezed"
				else:
					if freezedFlag != True:
						print "Down (Y + " + str(accelerator) + ")"
						counterY += accelerator
					else:
						print "Counter Freezed"
			elif xCenter > 320 and yCenter > 213:
				if math.sqrt((320 - xCenter)*(320 - xCenter)) > math.sqrt((213 - yCenter)*(213 - yCenter)):
					if freezedFlag != True:
						print "Right (X + " + str(accelerator) + ")"
						counterX += accelerator
					else:
						print "Counter Freezed"
				else:
					if freezedFlag != True:
						print "Down (Y + " + str(accelerator) + ")"
						counterY += accelerator
					else:
						print "Counter Freezed"
			else:
				print "Can't recognize this gesture"

		## Center of gesture falls into the four blue square areas outside the circle.
		elif (math.sqrt((320 - xCenter)*(320 - xCenter) + (213 - yCenter)*(213 - yCenter)) > 106.5):
			if xCenter < 320 and yCenter < 213:
				if freezedFlag != True:
					print "Left and Up (X - "+ str(accelerator) + " and Y - " + str(accelerator) + ")"
					counterX -= accelerator
					counterY -= accelerator
				else:
					print "Counter Freezed"
			elif xCenter > 320 and yCenter < 213:
				if freezedFlag != True:
					print "Right and Up (X + "+ str(accelerator) + " and Y - " + str(accelerator) + ")"
					counterX += accelerator
					counterY -= accelerator
				else:
					print "Counter Freezed"
			elif xCenter < 320 and yCenter > 213:
				if freezedFlag != True:
					print "Left and Down (X - "+ str(accelerator) + " and Y + " + str(accelerator) + ")"
					counterX -= accelerator
					counterY += accelerator
				else:
					print "Counter Freezed"
			elif xCenter > 320 and yCenter > 213:
				if freezedFlag != True:
					print "Right and Down (X + "+ str(accelerator) + " and Y + " + str(accelerator) + ")"
					counterX += accelerator
					counterY += accelerator
				else:
					print "Counter Freezed"
			else:
				print "Can't recognize this gesture"
		else:
				print "Can't recognize this gesture"
	result_text = str(counterX) + str(counterY) + number_print
	if result_text == targeted_result_list[listcounter]:
		print "The Sequence of Actions is Successfully Processed"
	else:
		print "The Sequence of Actions is Failed"
		print colored("Current Location of Counter is: ", "blue")
		print colored("Counter X:" + str(counterX), "red")
		print colored("Counter Y:" + str(counterY), "red")
	listcounter += 1
	result_text = ""