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

sequence_list = ["sequence_1", "sequence_2", "sequence_3", "sequence_4", "sequence_5_failed", "sequence_6_failed", "sequence_7", "sequence_8", "sequence_9", "sequence_10_failed"]
targeted_result_list = ["320213print", "322216print", "321213print", "320213print", "320211print", "324213print", "320213print", "319212print", "320211print", "320210printprint"]
listcounter = 0

for folder in sequence_list:
	print "\n"
	print colored("Reading Folder: " + folder, 'green')
	counterX = 320
	counterY = 213
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
			for i in range(defects.shape[0]):
				s,e,f,d = defects[i,0]
				if d >= 10000:
					defectPointCount += 1

			if defectPointCount >= 5 and boundingRect >= 45000:
				print colored("Location of Counter", "blue")
				print colored("Counter X:" + str(counterX), "red")
				print colored("Counter Y:" + str(counterY), "red")
				number_print = number_print + "print"
			elif defectPointCount <= 5 and boundingRect <= 35000:
				print "Reset X -> 320 and Y -> 213"
				counterX = 320
				counterY = 213
			else:
				print "Opps I don't understand this gesture"
		elif (53.25 < math.sqrt((320 - xCenter)*(320 - xCenter) + (213 - yCenter)*(213 - yCenter)) <= 106.5):
			if xCenter < 320 and yCenter < 213:
				if math.sqrt((320 - xCenter)*(320 - xCenter)) > math.sqrt((213 - yCenter)*(213 - yCenter)):
					print "Left (X - 1)"
					counterX -= 1
				else:
					print "Up (Y - 1)"
					counterY -= 1
			elif xCenter > 320 and yCenter < 213:
				if math.sqrt((320 - xCenter)*(320 - xCenter)) > math.sqrt((213 - yCenter)*(213 - yCenter)):
					print "Right (X + 1)"
					counterX += 1
				else:
					print "Up (Y - 1)"
					counterY -= 1
			elif xCenter < 320 and yCenter > 213:
				if math.sqrt((320 - xCenter)*(320 - xCenter)) > math.sqrt((213 - yCenter)*(213 - yCenter)):
					print "Left (X - 1)"
					counterX -= 1
				else:
					print "Down (Y + 1)"
					counterY += 1
			elif xCenter > 320 and yCenter > 213:
				if math.sqrt((320 - xCenter)*(320 - xCenter)) > math.sqrt((213 - yCenter)*(213 - yCenter)):
					print "Right (X + 1)"
					counterX += 1
				else:
					print "Down (Y + 1)"
					counterY += 1
		elif (math.sqrt((320 - xCenter)*(320 - xCenter) + (213 - yCenter)*(213 - yCenter)) > 106.5):
			if xCenter < 320 and yCenter < 213:
				print "Left and Up (X - 1 and Y - 1)"
				counterX -= 1
				counterY -= 1
			if xCenter > 320 and yCenter < 213:
				print "Right and Up (X + 1 and Y - 1)"
				counterX += 1
				counterY -= 1
			if xCenter < 320 and yCenter > 213:
				print "Left and Down (X - 1 and Y + 1)"
				counterX -= 1
				counterY += 1
			if xCenter > 320 and yCenter > 213:
				print "Right and Down (X + 1 and Y + 1)"
				counterX += 1
				counterY += 1
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