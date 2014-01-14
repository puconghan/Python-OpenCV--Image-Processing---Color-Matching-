import os
import glob
import cv2
from PIL import ImageTk,Image
import numpy as np
from termcolor import colored
import math

def isLeft(a, b, c):
	if ((b[0] - a[0])*(c[1] - a[1]) - (b[1] - a[1])*(c[0] - a[0])) > 0:
		return True
	else:
		return False

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

building_properties = []
building_relations = {}
building_distance = {}
reduced_relations = []
near_relations = []

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

#For each building countour, this for-loop assigns proper descriptions (shapes, sizes and location)
for h,cnt in enumerate(contours):
	building_name = ""
	building_shape = ""
	building_size_description = ""
	building_location_extrema_description = ""
	building_contour_center = []
	building_contour_area = 0
	building_contour_upper_left = []
	building_contour_lower_right = []

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
	xCenter = xValue / count
	yCenter = yValue / count

	building_contour_center = [xCenter, yCenter]

	x,y,w,h = cv2.boundingRect(cnt)

	building_contour_upper_left = [x, y]
	building_contour_lower_right = [x+w, y+h]

	#Get the name of the building by passing the variable to the hashtable label
	building_name = label[integer_value / count]
	

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
	
	#Compare with the coutours in the shape list and match shape description
	shape_name = shapes[0][1]
	shape_value = cv2.matchShapes(shapes[0][0], cnt, cv2.cv.CV_CONTOURS_MATCH_I1, 0)
	for item in shapes:
		if shape_value > cv2.matchShapes(item[0], cnt, cv2.cv.CV_CONTOURS_MATCH_I1, 0):
			shape_value = cv2.matchShapes(item[0], cnt, cv2.cv.CV_CONTOURS_MATCH_I1, 0)
			shape_name = item[1]
	building_shape = shape_name

	building_properties.append([building_name, building_contour_center, building_contour_area, building_contour_upper_left, building_contour_lower_right, building_shape, building_size_description, building_location_extrema_description])

# Importing Tkinter GUI library
from Tkinter import *

master = Tk()

# Callback function for mouse clicks
def callback(event):
	#[Testing] Print the mouse click x and y values
	print colored("clicked at: " + "(" + str(event.x) + ", " + str(event.y) + ")", "red")

	# The following code computes the descriptions for the locations.
	contour_fall = ""
	contour_name = ""
	descritions = []
	for h,cnt in enumerate(contours):
		#If the point is in any building contours, codes within this if-statement will print the building name.
		if cv2.pointPolygonTest(cnt,(event.x, event.y),True) >= 0:
			contour_fall = cnt
			count = 0
			integer_value = 0
			for demensions in cnt:
				for values in demensions:
					integer_value += integer_value_campus.getpixel((int(values[0]), int(values[1])))
					count += 1
					#Get the name of the building by passing the variable to the hashtable label.
					contour_name = label[integer_value / count]
			print colored(contour_name, 'blue')
	#If the point is not in any building contours, codes within this if-statement compute the location description of the point.
	if contour_fall == "":
		#Storing spatial relations of the point to all buildings. This is a temporary variable.
		spatial_relations = []
		#This for-loop goes over all buildings in the building_properties variable (including a list of building_name, building_contour_center, building_contour_area, building_contour_upper_left, building_contour_lower_right, building_shape, building_size_description, building_location_extrema_description). 
		for building in building_properties:
			#These if-and-else-statement checks and store building names and relations to the points to the spatial_relations list variable.
			if (isLeft(building[1], building[3], [event.x, event.y]) == False) and (isLeft(building[1], [building[4][0], building[3][1]], [event.x, event.y]) == True):
				if math.sqrt((event.y - building[4][1])*(event.y - building[4][1])) <= 10 * building[2] / 2500:
					spatial_relations.append(["south", building[0], math.sqrt((building[1][0] - event.x)*(building[1][0] - event.x) + (building[1][1] - event.y)*(building[1][1] - event.y)), "near"])
				else:
					spatial_relations.append(["south", building[0], math.sqrt((building[1][0] - event.x)*(building[1][0] - event.x) + (building[1][1] - event.y)*(building[1][1] - event.y)), "not near"])
			if (isLeft(building[1], building[3], [event.x, event.y]) == True) and (isLeft(building[1], [building[4][0], building[3][1]], [event.x, event.y]) == False):
				if math.sqrt((building[3][1] - event.y)*(building[3][1] - event.y)) <= 10 * building[2] / 2500:
					spatial_relations.append(["north", building[0], math.sqrt((building[1][0] - event.x)*(building[1][0] - event.x) + (building[1][1] - event.y)*(building[1][1] - event.y)), "near"])
				else:
					spatial_relations.append(["north", building[0], math.sqrt((building[1][0] - event.x)*(building[1][0] - event.x) + (building[1][1] - event.y)*(building[1][1] - event.y)), "not near"])
			if (isLeft(building[1], building[3], [event.x, event.y]) == True) and (isLeft(building[1], [building[4][0], building[3][1]], [event.x, event.y]) == True):
				if math.sqrt((event.x - building[4][0])*(event.x - building[4][0])) <= 10 * building[2] / 2500:
					spatial_relations.append(["east", building[0], math.sqrt((building[1][0] - event.x)*(building[1][0] - event.x) + (building[1][1] - event.y)*(building[1][1] - event.y)), "near"])
				else:
					spatial_relations.append(["east", building[0], math.sqrt((building[1][0] - event.x)*(building[1][0] - event.x) + (building[1][1] - event.y)*(building[1][1] - event.y)), "not near"])
			if (isLeft(building[1], building[3], [event.x, event.y]) == False) and (isLeft(building[1], [building[4][0], building[3][1]], [event.x, event.y]) == False):
				if math.sqrt((building[3][0] - event.x)*(building[3][0] - event.x)) <= 10 * building[2] / 2500:
					spatial_relations.append(["west", building[0], math.sqrt((building[1][0] - event.x)*(building[1][0] - event.x) + (building[1][1] - event.y)*(building[1][1] - event.y)), "near"])
				else:
					spatial_relations.append(["west", building[0], math.sqrt((building[1][0] - event.x)*(building[1][0] - event.x) + (building[1][1] - event.y)*(building[1][1] - event.y)), "not near"])
		#These temporary variables help to find the most immediate relation (nearest/ north/ south/ west/ east) of a point (with shortest distance to a building gesture).
		building_N = ""
		distance_N = math.sqrt(495*495+275*275)
		near_N = ""
		building_S = ""
		distance_S = math.sqrt(495*495+275*275)
		near_S = ""
		building_W = ""
		distance_W = math.sqrt(495*495+275*275)
		near_W = ""
		building_E = ""
		distance_E = math.sqrt(495*495+275*275)
		near_E = ""
		#This for-loop goes over the spatial_relations and stores the most immediate relation (nearest/ north/ south/ west/ east) of a point (with shortest distance to a building gesture) to appropriate temporary variables.
		for item in spatial_relations:
			if item[0] == "north":
				if distance_N >= item[2]:
					building_N = item[1]
					distance_N = item[2]
					near_N = item[3]
			if item[0] == "south":
				if distance_S >= item[2]:
					building_S = item[1]
					distance_S = item[2]
					near_S = item[3]
			if item[0] == "west":
				if distance_W >= item[2]:
					building_W = item[1]
					distance_W = item[2]
					near_W = item[3]
			if item[0] == "east":
				if distance_E >= item[2]:
					building_E = item[1]
					distance_E = item[2]
					near_E = item[3]

		#This temporary variable used to check all other points with same relation descriptions.
		point_stack = ""

		#These if-statements update and save the most immediate relation (nearest/ north/ south/ west/ east) of a point (with shortest distance to a building gesture) from temporary variables to descriptions list and point_stack string variable.
		if distance_N != math.sqrt(495*495+275*275):
			if near_N == "near":
				descritions.append("Point is near and is to the north of " + building_N)
				point_stack = point_stack + "near_north" + building_N
			else:
				descritions.append("Point is to the north of " + building_N)
				point_stack = point_stack + "north" + building_N
		if distance_S != math.sqrt(495*495+275*275):
			if near_S == "near":
				descritions.append("Point is near and is to the south of " + building_S)
				point_stack = point_stack + "near_south" + building_S
			else:
				descritions.append("Point is to the south of " + building_S)
				point_stack = point_stack + "south" + building_S
		if distance_W != math.sqrt(495*495+275*275):
			if near_W == "near":
				descritions.append("Point is near and is to the west of " + building_W)
				point_stack = point_stack + "near_west" + building_W
			else:
				descritions.append("Point is to the west of " + building_W)
				point_stack = point_stack + "west" + building_W
		if distance_E != math.sqrt(495*495+275*275):
			if near_E == "near":
				descritions.append("Point is near and is to the east of " + building_E)
				point_stack = point_stack + "near_east" + building_E
			else:
				descritions.append("Point is to the east of " + building_E)
				point_stack = point_stack + "east" + building_E
		#This for-loop prints all immediate relation (nearest/ north/ south/ west/ east) of a point (with shortest distance to a building gesture) from the descriptions list.
		for item in descritions:
			print colored(item, 'green')

		# The following code finds and draws all points sharing similar location descriptions.

		#Open the integer value campus image
		campus_region = cv2.imread("ass3-campus.pgm")

		#Improve running efficiency using the following loops. They go over all point within a region of interest 100 pixel * 100 pixel (mouse pixel in the middle)
		# x = event.x - 50
		# while x <= event.x + 50:
		# 	y = event.y - 50
		# 	while y <= event.y + 50:
		
		#The following while-loops go over all pixels in the image.
		x = 0
		while x <= integer_value_campus.size[0]:
			y = 0
			while y <= integer_value_campus.size[1]:
				#Similar to the previous portion, these loops and if-statement compute all relational descriptions of a point to all building contours.
				spatial_relations = []
				for building in building_properties:
					if (isLeft(building[1], building[3], [x, y]) == False) and (isLeft(building[1], [building[4][0], building[3][1]], [x, y]) == True):
						if math.sqrt((y - building[4][1])*(y - building[4][1])) <= 10 * building[2] / 2500:
							spatial_relations.append(["south", building[0], math.sqrt((building[1][0] - x)*(building[1][0] - x) + (building[1][1] - y)*(building[1][1] - y)), "near"])
						else:
							spatial_relations.append(["south", building[0], math.sqrt((building[1][0] - x)*(building[1][0] - x) + (building[1][1] - y)*(building[1][1] - y)), "not near"])
					if (isLeft(building[1], building[3], [x, y]) == True) and (isLeft(building[1], [building[4][0], building[3][1]], [x, y]) == False):
						if math.sqrt((building[3][1] - y)*(building[3][1] - y)) <= 10 * building[2] / 2500:
							spatial_relations.append(["north", building[0], math.sqrt((building[1][0] - x)*(building[1][0] - x) + (building[1][1] - y)*(building[1][1] - y)), "near"])
						else:
							spatial_relations.append(["north", building[0], math.sqrt((building[1][0] - x)*(building[1][0] - x) + (building[1][1] - y)*(building[1][1] - y)), "not near"])
					if (isLeft(building[1], building[3], [x, y]) == True) and (isLeft(building[1], [building[4][0], building[3][1]], [x, y]) == True):
						if math.sqrt((x - building[4][0])*(x - building[4][0])) <= 10 * building[2] / 2500:
							spatial_relations.append(["east", building[0], math.sqrt((building[1][0] - x)*(building[1][0] - x) + (building[1][1] - y)*(building[1][1] - y)), "near"])
						else:
							spatial_relations.append(["east", building[0], math.sqrt((building[1][0] - x)*(building[1][0] - x) + (building[1][1] - y)*(building[1][1] - y)), "not near"])
					if (isLeft(building[1], building[3], [x, y]) == False) and (isLeft(building[1], [building[4][0], building[3][1]], [x, y]) == False):
						if math.sqrt((building[3][0] - x)*(building[3][0] - x)) <= 10 * building[2] / 2500:
							spatial_relations.append(["west", building[0], math.sqrt((building[1][0] - x)*(building[1][0] - x) + (building[1][1] - y)*(building[1][1] - y)), "near"])
						else:
							spatial_relations.append(["west", building[0], math.sqrt((building[1][0] - x)*(building[1][0] - x) + (building[1][1] - y)*(building[1][1] - y)), "not near"])
				
				#These temporary variables help to find the most immediate relation (nearest/ north/ south/ west/ east) of a point (with shortest distance to a building gesture).
				building_N = ""
				distance_N = math.sqrt(495*495+275*275)
				near_N = ""
				building_S = ""
				distance_S = math.sqrt(495*495+275*275)
				near_S = ""
				building_W = ""
				distance_W = math.sqrt(495*495+275*275)
				near_W = ""
				building_E = ""
				distance_E = math.sqrt(495*495+275*275)
				near_E = ""
				
				#This for-loop goes over the spatial_relations and stores the most immediate relation (nearest/ north/ south/ west/ east) of a point (with shortest distance to a building gesture) to appropriate temporary variables.
				for item in spatial_relations:
					if item[0] == "north":
						if distance_N >= item[2]:
							building_N = item[1]
							distance_N = item[2]
							near_N = item[3]
					if item[0] == "south":
						if distance_S >= item[2]:
							building_S = item[1]
							distance_S = item[2]
							near_S = item[3]
					if item[0] == "west":
						if distance_W >= item[2]:
							building_W = item[1]
							distance_W = item[2]
							near_W = item[3]
					if item[0] == "east":
						if distance_E >= item[2]:
							building_E = item[1]
							distance_E = item[2]
							near_E = item[3]

				#This temporary variable used to check points with same relation descriptions.
				new_point_stack = ""

				#These if-statements update and save the most immediate relation (nearest/ north/ south/ west/ east) of a point (with shortest distance to a building gesture) from temporary variables to descriptions list and point_stack string variable.
				if distance_N != math.sqrt(495*495+275*275):
					if near_N == "near":
						new_point_stack = new_point_stack + "near_north" + building_N
					else:
						new_point_stack = new_point_stack + "north" + building_N
				if distance_S != math.sqrt(495*495+275*275):
					if near_S == "near":
						new_point_stack = new_point_stack + "near_south" + building_S
					else:
						new_point_stack = new_point_stack + "south" + building_S
				if distance_W != math.sqrt(495*495+275*275):
					if near_W == "near":
						new_point_stack = new_point_stack + "near_west" + building_W
					else:
						new_point_stack = new_point_stack + "west" + building_W
				if distance_E != math.sqrt(495*495+275*275):
					if near_E == "near":
						new_point_stack = new_point_stack + "near_east" + building_E
					else:
						new_point_stack = new_point_stack + "east" + building_E
				
				#This if-statement will check points with same relation descriptions to the mouse click point and draw red circles on a temporary campus image.
				if new_point_stack == point_stack:
					overlap = False
					for h,cnt in enumerate(contours):
						if cv2.pointPolygonTest(cnt,(x, y),True) >= 0:
							overlap = True
					if overlap == False:
						cv2.circle(campus_region,(x, y),1,[0,255,0],-1)
				y += 1
			x += 1
		#Save the modified image to image_with_points.png file.
		cv2.imwrite('image_with_points.png', campus_region)
	
	#Read the modified image and replace the label image of the GUI. As a result, the red circles will be displayed on the map.
	photo = PhotoImage(file='image_with_points.png')
	w.config(image=photo)
	w.photo = photo

def callback2(event):
	#[Testing] Print the mouse click x and y values
	print colored("clicked at: " + "(" + str(event.x) + ", " + str(event.y) + ")", "red")

	# The following code computes the descriptions for the locations.
	contour_fall = ""
	contour_name = ""
	descritions = []
	for h,cnt in enumerate(contours):
		#If the point is in any building contours, codes within this if-statement will print the building name.
		if cv2.pointPolygonTest(cnt,(event.x, event.y),True) >= 0:
			contour_fall = cnt
			count = 0
			integer_value = 0
			for demensions in cnt:
				for values in demensions:
					integer_value += integer_value_campus.getpixel((int(values[0]), int(values[1])))
					count += 1
					#Get the name of the building by passing the variable to the hashtable label.
					contour_name = label[integer_value / count]
			print colored(contour_name, 'blue')
	#If the point is not in any building contours, codes within this if-statement compute the location description of the point.
	if contour_fall == "":
		#Storing spatial relations of the point to all buildings. This is a temporary variable.
		spatial_relations = []
		#This for-loop goes over all buildings in the building_properties variable (including a list of building_name, building_contour_center, building_contour_area, building_contour_upper_left, building_contour_lower_right, building_shape, building_size_description, building_location_extrema_description). 
		for building in building_properties:
			#These if-and-else-statement checks and store building names and relations to the points to the spatial_relations list variable.
			if (isLeft(building[1], building[3], [event.x, event.y]) == False) and (isLeft(building[1], [building[4][0], building[3][1]], [event.x, event.y]) == True):
				if math.sqrt((event.y - building[4][1])*(event.y - building[4][1])) <= 10 * building[2] / 2500:
					spatial_relations.append(["south", building[0], math.sqrt((building[1][0] - event.x)*(building[1][0] - event.x) + (building[1][1] - event.y)*(building[1][1] - event.y)), "near"])
				else:
					spatial_relations.append(["south", building[0], math.sqrt((building[1][0] - event.x)*(building[1][0] - event.x) + (building[1][1] - event.y)*(building[1][1] - event.y)), "not near"])
			if (isLeft(building[1], building[3], [event.x, event.y]) == True) and (isLeft(building[1], [building[4][0], building[3][1]], [event.x, event.y]) == False):
				if math.sqrt((building[3][1] - event.y)*(building[3][1] - event.y)) <= 10 * building[2] / 2500:
					spatial_relations.append(["north", building[0], math.sqrt((building[1][0] - event.x)*(building[1][0] - event.x) + (building[1][1] - event.y)*(building[1][1] - event.y)), "near"])
				else:
					spatial_relations.append(["north", building[0], math.sqrt((building[1][0] - event.x)*(building[1][0] - event.x) + (building[1][1] - event.y)*(building[1][1] - event.y)), "not near"])
			if (isLeft(building[1], building[3], [event.x, event.y]) == True) and (isLeft(building[1], [building[4][0], building[3][1]], [event.x, event.y]) == True):
				if math.sqrt((event.x - building[4][0])*(event.x - building[4][0])) <= 10 * building[2] / 2500:
					spatial_relations.append(["east", building[0], math.sqrt((building[1][0] - event.x)*(building[1][0] - event.x) + (building[1][1] - event.y)*(building[1][1] - event.y)), "near"])
				else:
					spatial_relations.append(["east", building[0], math.sqrt((building[1][0] - event.x)*(building[1][0] - event.x) + (building[1][1] - event.y)*(building[1][1] - event.y)), "not near"])
			if (isLeft(building[1], building[3], [event.x, event.y]) == False) and (isLeft(building[1], [building[4][0], building[3][1]], [event.x, event.y]) == False):
				if math.sqrt((building[3][0] - event.x)*(building[3][0] - event.x)) <= 10 * building[2] / 2500:
					spatial_relations.append(["west", building[0], math.sqrt((building[1][0] - event.x)*(building[1][0] - event.x) + (building[1][1] - event.y)*(building[1][1] - event.y)), "near"])
				else:
					spatial_relations.append(["west", building[0], math.sqrt((building[1][0] - event.x)*(building[1][0] - event.x) + (building[1][1] - event.y)*(building[1][1] - event.y)), "not near"])
		#These temporary variables help to find the most immediate relation (nearest/ north/ south/ west/ east) of a point (with shortest distance to a building gesture).
		building_N = ""
		distance_N = math.sqrt(495*495+275*275)
		near_N = ""
		building_S = ""
		distance_S = math.sqrt(495*495+275*275)
		near_S = ""
		building_W = ""
		distance_W = math.sqrt(495*495+275*275)
		near_W = ""
		building_E = ""
		distance_E = math.sqrt(495*495+275*275)
		near_E = ""
		#This for-loop goes over the spatial_relations and stores the most immediate relation (nearest/ north/ south/ west/ east) of a point (with shortest distance to a building gesture) to appropriate temporary variables.
		for item in spatial_relations:
			if item[0] == "north":
				if distance_N >= item[2]:
					building_N = item[1]
					distance_N = item[2]
					near_N = item[3]
			if item[0] == "south":
				if distance_S >= item[2]:
					building_S = item[1]
					distance_S = item[2]
					near_S = item[3]
			if item[0] == "west":
				if distance_W >= item[2]:
					building_W = item[1]
					distance_W = item[2]
					near_W = item[3]
			if item[0] == "east":
				if distance_E >= item[2]:
					building_E = item[1]
					distance_E = item[2]
					near_E = item[3]

		#This temporary variable used to check all other points with same relation descriptions.
		point_stack = ""

		#These if-statements update and save the most immediate relation (nearest/ north/ south/ west/ east) of a point (with shortest distance to a building gesture) from temporary variables to descriptions list and point_stack string variable.
		if distance_N != math.sqrt(495*495+275*275):
			if near_N == "near":
				descritions.append("Point is near and is to the north of " + building_N)
				point_stack = point_stack + "near_north" + building_N
			else:
				descritions.append("Point is to the north of " + building_N)
				point_stack = point_stack + "north" + building_N
		if distance_S != math.sqrt(495*495+275*275):
			if near_S == "near":
				descritions.append("Point is near and is to the south of " + building_S)
				point_stack = point_stack + "near_south" + building_S
			else:
				descritions.append("Point is to the south of " + building_S)
				point_stack = point_stack + "south" + building_S
		if distance_W != math.sqrt(495*495+275*275):
			if near_W == "near":
				descritions.append("Point is near and is to the west of " + building_W)
				point_stack = point_stack + "near_west" + building_W
			else:
				descritions.append("Point is to the west of " + building_W)
				point_stack = point_stack + "west" + building_W
		if distance_E != math.sqrt(495*495+275*275):
			if near_E == "near":
				descritions.append("Point is near and is to the east of " + building_E)
				point_stack = point_stack + "near_east" + building_E
			else:
				descritions.append("Point is to the east of " + building_E)
				point_stack = point_stack + "east" + building_E
		#This for-loop prints all immediate relation (nearest/ north/ south/ west/ east) of a point (with shortest distance to a building gesture) from the descriptions list.
		for item in descritions:
			print colored(item, 'green')

		# The following code finds and draws all points sharing similar location descriptions.

		#Open the integer value campus image
		campus_region = cv2.imread("image_with_points.png")

		#Improve running efficiency using the following loops. They go over all point within a region of interest 100 pixel * 100 pixel (mouse pixel in the middle)
		# x = event.x - 50
		# while x <= event.x + 50:
		# 	y = event.y - 50
		# 	while y <= event.y + 50:
		
		#The following while-loops go over all pixels in the image.
		x = 0
		while x <= integer_value_campus.size[0]:
			y = 0
			while y <= integer_value_campus.size[1]:
				#Similar to the previous portion, these loops and if-statement compute all relational descriptions of a point to all building contours.
				spatial_relations = []
				for building in building_properties:
					if (isLeft(building[1], building[3], [x, y]) == False) and (isLeft(building[1], [building[4][0], building[3][1]], [x, y]) == True):
						if math.sqrt((y - building[4][1])*(y - building[4][1])) <= 10 * building[2] / 2500:
							spatial_relations.append(["south", building[0], math.sqrt((building[1][0] - x)*(building[1][0] - x) + (building[1][1] - y)*(building[1][1] - y)), "near"])
						else:
							spatial_relations.append(["south", building[0], math.sqrt((building[1][0] - x)*(building[1][0] - x) + (building[1][1] - y)*(building[1][1] - y)), "not near"])
					if (isLeft(building[1], building[3], [x, y]) == True) and (isLeft(building[1], [building[4][0], building[3][1]], [x, y]) == False):
						if math.sqrt((building[3][1] - y)*(building[3][1] - y)) <= 10 * building[2] / 2500:
							spatial_relations.append(["north", building[0], math.sqrt((building[1][0] - x)*(building[1][0] - x) + (building[1][1] - y)*(building[1][1] - y)), "near"])
						else:
							spatial_relations.append(["north", building[0], math.sqrt((building[1][0] - x)*(building[1][0] - x) + (building[1][1] - y)*(building[1][1] - y)), "not near"])
					if (isLeft(building[1], building[3], [x, y]) == True) and (isLeft(building[1], [building[4][0], building[3][1]], [x, y]) == True):
						if math.sqrt((x - building[4][0])*(x - building[4][0])) <= 10 * building[2] / 2500:
							spatial_relations.append(["east", building[0], math.sqrt((building[1][0] - x)*(building[1][0] - x) + (building[1][1] - y)*(building[1][1] - y)), "near"])
						else:
							spatial_relations.append(["east", building[0], math.sqrt((building[1][0] - x)*(building[1][0] - x) + (building[1][1] - y)*(building[1][1] - y)), "not near"])
					if (isLeft(building[1], building[3], [x, y]) == False) and (isLeft(building[1], [building[4][0], building[3][1]], [x, y]) == False):
						if math.sqrt((building[3][0] - x)*(building[3][0] - x)) <= 10 * building[2] / 2500:
							spatial_relations.append(["west", building[0], math.sqrt((building[1][0] - x)*(building[1][0] - x) + (building[1][1] - y)*(building[1][1] - y)), "near"])
						else:
							spatial_relations.append(["west", building[0], math.sqrt((building[1][0] - x)*(building[1][0] - x) + (building[1][1] - y)*(building[1][1] - y)), "not near"])
				
				#These temporary variables help to find the most immediate relation (nearest/ north/ south/ west/ east) of a point (with shortest distance to a building gesture).
				building_N = ""
				distance_N = math.sqrt(495*495+275*275)
				near_N = ""
				building_S = ""
				distance_S = math.sqrt(495*495+275*275)
				near_S = ""
				building_W = ""
				distance_W = math.sqrt(495*495+275*275)
				near_W = ""
				building_E = ""
				distance_E = math.sqrt(495*495+275*275)
				near_E = ""
				
				#This for-loop goes over the spatial_relations and stores the most immediate relation (nearest/ north/ south/ west/ east) of a point (with shortest distance to a building gesture) to appropriate temporary variables.
				for item in spatial_relations:
					if item[0] == "north":
						if distance_N >= item[2]:
							building_N = item[1]
							distance_N = item[2]
							near_N = item[3]
					if item[0] == "south":
						if distance_S >= item[2]:
							building_S = item[1]
							distance_S = item[2]
							near_S = item[3]
					if item[0] == "west":
						if distance_W >= item[2]:
							building_W = item[1]
							distance_W = item[2]
							near_W = item[3]
					if item[0] == "east":
						if distance_E >= item[2]:
							building_E = item[1]
							distance_E = item[2]
							near_E = item[3]

				#This temporary variable used to check points with same relation descriptions.
				new_point_stack = ""

				#These if-statements update and save the most immediate relation (nearest/ north/ south/ west/ east) of a point (with shortest distance to a building gesture) from temporary variables to descriptions list and point_stack string variable.
				if distance_N != math.sqrt(495*495+275*275):
					if near_N == "near":
						new_point_stack = new_point_stack + "near_north" + building_N
					else:
						new_point_stack = new_point_stack + "north" + building_N
				if distance_S != math.sqrt(495*495+275*275):
					if near_S == "near":
						new_point_stack = new_point_stack + "near_south" + building_S
					else:
						new_point_stack = new_point_stack + "south" + building_S
				if distance_W != math.sqrt(495*495+275*275):
					if near_W == "near":
						new_point_stack = new_point_stack + "near_west" + building_W
					else:
						new_point_stack = new_point_stack + "west" + building_W
				if distance_E != math.sqrt(495*495+275*275):
					if near_E == "near":
						new_point_stack = new_point_stack + "near_east" + building_E
					else:
						new_point_stack = new_point_stack + "east" + building_E
				
				#This if-statement will check points with same relation descriptions to the mouse click point and draw red circles on a temporary campus image.
				if new_point_stack == point_stack:
					overlap = False
					for h,cnt in enumerate(contours):
						if cv2.pointPolygonTest(cnt,(x, y),True) >= 0:
							overlap = True
					if overlap == False:
						cv2.circle(campus_region,(x, y),1,[0,0,255],-1)
				y += 1
			x += 1
		#Save the modified image to image_with_points.png file.
		cv2.imwrite('image_with_points.png', campus_region)
	
	#Read the modified image and replace the label image of the GUI. As a result, the red circles will be displayed on the map.
	photo = PhotoImage(file='image_with_points.png')
	w.config(image=photo)
	w.photo = photo

photo = PhotoImage(file="ass3-campus.pgm")
w = Label(None, image=photo)
w.photo = photo
w.bind("<Button-1>", callback)
w.bind("<Button-2>", callback2)
w.pack()

mainloop()