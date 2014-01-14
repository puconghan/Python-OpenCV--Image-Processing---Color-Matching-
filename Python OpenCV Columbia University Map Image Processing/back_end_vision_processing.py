import os
import glob
import cv2
from PIL import Image
import numpy as np
from termcolor import colored
import math

#Create a hashtable, in Python it is called 'dictionaries' or 'associative arrays,' associates the building numbers with the building names.
label = {}
label[1]="Pupin"
label[2]="Schapiro CEPSR"
label[3]="Mudd, Engineering Terrace, Fairchild & Computer Science"
label[4]="Physical Fitness Center"
label[5]="Gymnasium & Uris"
label[6]="Schermerhorn"
label[7]="Chandler & Havemeyer"
label[8]="Computer Center"
label[9]="Avery"
label[10]="Fayerweather"
label[11]="Mathematics"
label[12]="Low Library"
label[13]="St. Paul's Chapel"
label[14]="Earl Hall"
label[15]="Lewisohn"
label[16]="Philosophy"
label[17]="Buell & Maison Francaise"
label[18]="Alma Mater"
label[19]="Dodge"
label[20]="Kent"
label[21]="College Walk"
label[22]="Journalism & Furnald"
label[23]="Hamilton, Hartley, Wallach & John Jay"
label[24]="Lion's Court"
label[25]="Lerner Hall"
label[26]="Butler Library"
label[27]="Carman"
#Create a list storing the contours of default shapes.
shapes = []
for shape_image in glob.glob( os.path.join("shapes", '*.png') ):
	shape = cv2.imread(shape_image)
	shape_gray = cv2.cvtColor(shape,cv2.COLOR_BGR2GRAY)
	ret_shape, thresh_shape = cv2.threshold(shape_gray,127,255,0)
	contours_shape, hierarchy_shape = cv2.findContours(thresh_shape,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	shapes.append([contours_shape[0], shape_image.replace("shapes/", "").replace(".png", "").replace("_", " ")])

#Open the integer value campus image
integer_value_campus = Image.open("ass3-labeled.pgm")
#Open the campus image
campus = cv2.imread("ass3-campus.pgm")

#[TESTING] Printing the size of the image (height, width, channel)
#print campus.shape

#Convert campus image to gray scale.
campus_gray = cv2.cvtColor(campus,cv2.COLOR_BGR2GRAY)
#Create binary images for the campus.
ret, thresh = cv2.threshold(campus_gray,127,255,0)
#Compute contours (boundaries) of buildings on campus.
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#[TESTING] Drawing building contours
#cv2.drawContours(campus,contours,-1,(0,255,0),3)

#For each building countour, this for-loop assigns proper descriptions (shapes, sizes and location)
for h,cnt in enumerate(contours):
	building_name = ""
	building_shape = ""
	building_size_description = ""
	building_location_extrema_description = ""
	building_contour_center = ""
	building_contour_area = 0
	building_contour_upper_left = 0
	building_contour_lower_right = 0
	
	#Get the integer value from the integer value campus image
	count = 0
	xValue = 0
	yValue = 0
	integer_value = 0
	for demensions in cnt:
		for values in demensions:
			integer_value += integer_value_campus.getpixel((int(values[0]), int(values[1])))
			xValue += values[0]
			yValue += values[1]
			count += 1
	#Compute the center of the contours.
	xCenter = xValue / count
	yCenter = yValue / count

	#Store the center of the contour into the building_contour_center variable.
	building_contour_center = "(" + str(xCenter) + ", " + str(yCenter) + ")"

	x,y,w,h = cv2.boundingRect(cnt)

	#[TESTING] Printing the bounding rectangle upper left and lower right
	# print "Upper left: " + "(" + str(x) + ", " + str(y) + ")"
	# print "Lower right: " + "(" + str(x+w) + ", " + str(y+h) + ")"

	building_contour_upper_left = "(" + str(x) + ", " + str(y) + ")"
	building_contour_lower_right = "(" + str(x+w) + ", " + str(y+h) + ")"

	#[TESTING] Printing the center
	# print "(" + str(xCenter) + ", " + str(yCenter) + ")"

	#Get the name of the building by passing the variable to the hashtable label
	building_name = label[integer_value / count]
	
	#[TESTING] Printing the name of the building
	# print colored(label[integer_value / count], 'blue')

	if 117.5 <= xCenter >= 157.5 and yCenter <= 40:
		building_location_extrema_description = "north most"
	if 117.5 <= xCenter >= 157.5 and yCenter >= 455:
		building_location_extrema_description = "south most"
	if xCenter <= 40 and 227.5 <= yCenter <= 267.5:
		building_location_extrema_description = "west most"
	if xCenter >= 235 and 227.5 <= yCenter <= 267.5:
		building_location_extrema_description = "east most"
	if xCenter <= 40 and yCenter <= 40:
		building_location_extrema_description = "north west most"
	if xCenter >= 235 and yCenter <= 40:
		building_location_extrema_description = "north east most"
	if xCenter <= 40 and yCenter >= 455:
		building_location_extrema_description = "south west most"
	if xCenter >= 235 and yCenter >= 455:
		building_location_extrema_description = "south east most"
	if math.sqrt((xCenter - 137.5)*(xCenter - 137.5) + (yCenter - 247.5)*(yCenter - 247.5)) <= 40:
		building_location_extrema_description = "most central"

	#[TESTING] Printing the building location extrema
	# if 117.5 <= xCenter >= 157.5 and yCenter <= 40:
	# 	print "north most"
	# if 117.5 <= xCenter >= 157.5 and yCenter >= 455:
	# 	print "south most"
	# if xCenter <= 40 and 227.5 <= yCenter <= 267.5:
	# 	print "west most"
	# if xCenter >= 235 and 227.5 <= yCenter <= 267.5:
	# 	print "east most"
	# if xCenter <= 40 and yCenter <= 40:
	# 	print "north west most"
	# if xCenter >= 235 and yCenter <= 40:
	# 	print "north east most"
	# if xCenter <= 40 and yCenter >= 455:
	# 	print "south west most"
	# if xCenter >= 235 and yCenter >= 455:
	# 	print "south east most"
	# if math.sqrt((xCenter - 137.5)*(xCenter - 137.5) + (yCenter - 247.5)*(yCenter - 247.5)) <= 40:
	# 	print "most central"

	#Compute the area of the contour
	building_contour_area = cv2.contourArea(cnt)

	#Compute the size of the countour area
	if cv2.contourArea(cnt) <= 500:
		building_size_description = "tiny size"
	if 500 < cv2.contourArea(cnt) <= 1200:
		building_size_description = "small size"
	if 1200 < cv2.contourArea(cnt) <= 2500:
		building_size_description = "average size"
	if cv2.contourArea(cnt) > 2500:
		building_size_description = "large size"

	#[TESTING] Printing sizes and descriptions of contour areas
	# print colored("Size of the area: " + str(cv2.contourArea(cnt)), 'green')
	# if cv2.contourArea(cnt) <= 500:
	# 	print colored("tiny size", 'green')
	# if 500 < cv2.contourArea(cnt) <= 1200:
	# 	print colored("small size", 'green')
	# if 1200 < cv2.contourArea(cnt) <= 2500:
	# 	print colored("average size", 'green')
	# if cv2.contourArea(cnt) > 2500:
	# 	print colored("large size", 'green')
	
	#Compare with the coutours in the shape list and match shape description
	shape_name = shapes[0][1]
	shape_value = cv2.matchShapes(shapes[0][0], cnt, cv2.cv.CV_CONTOURS_MATCH_I1, 0)
	for item in shapes:
		if shape_value > cv2.matchShapes(item[0], cnt, cv2.cv.CV_CONTOURS_MATCH_I1, 0):
			shape_value = cv2.matchShapes(item[0], cnt, cv2.cv.CV_CONTOURS_MATCH_I1, 0)
			shape_name = item[1]
	building_shape = shape_name
	#[TESTING] Printing the name of the shape
	# print shape_name
	# print ""

	print colored(building_name, 'red')
	print colored("Building contour center is: " + building_contour_center, 'green')
	print colored("Building contour area is: " + str(building_contour_area), 'green')
	print colored("Building contour upper left is: " + building_contour_upper_left, 'green')
	print colored("Building contour lower right is: " + building_contour_lower_right, 'green')
	print colored("Building shape is: " + building_shape, 'blue')
	print colored("Building size description: " + building_size_description, 'blue')
	if building_location_extrema_description is not "":
		print colored("Building shape description (extrema): " + building_location_extrema_description, 'blue')
	print ""
