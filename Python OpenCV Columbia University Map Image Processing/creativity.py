import os
import glob
import cv2
from PIL import ImageTk,Image
import numpy as np
from termcolor import colored
import math

#Function to determine whether point a is to the left of line through points b and c.
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

#Variables for storing temporary building properties
building_properties = []
building_relations = {}
building_distance = {}
#Variables for storing reduced spatial relations.
reduced_relations = []
#Variables for storing routes.
route = []
#Variables for storing start and destination variables.
start_and_destination = [[], []]

#Open the integer value campus image.
integer_value_campus = Image.open("ass3-labeled.pgm")
#Open the campus image.
campus = cv2.imread("ass3-campus.pgm")
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

	#Get the name of the building from the hash table
	building_name = label[integer_value / count]

	#Compute building location extrema descriptions.
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

	if building_location_extrema_description == "":
		building_location_extrema_description = "on campus"

	#Compute the contour area.
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

for building in building_properties:
	for building_sub in building_properties:
		if building[0] != building_sub[0]:
			if (isLeft(building[1], building[3], building_sub[1]) == False) and (isLeft(building[1], [building[4][0], building[3][1]], building_sub[1]) == True):
				building_relations[building[0], building_sub[0], "relation"] = "north"
				building_distance[building[0], building_sub[0], "relation"] = math.sqrt((building[1][0] - building_sub[1][0])*(building[1][0] - building_sub[1][0]) + (building[1][1] - building_sub[1][1])*(building[1][1] - building_sub[1][1]))
				if math.sqrt((building_sub[3][1] - building[4][1])*(building_sub[3][1] - building[4][1])) <= 6 * building[2] / 2500:
					building_relations[building[0], building_sub[0], "near"] = "near"
				else:
					building_relations[building[0], building_sub[0], "near"] = math.sqrt((building_sub[3][1] - building[4][1])*(building_sub[3][1] - building[4][1]))
			if (isLeft(building[1], building[3], building_sub[1]) == True) and (isLeft(building[1], [building[4][0], building[3][1]], building_sub[1]) == False):
				building_relations[building[0], building_sub[0], "relation"] = "south"
				building_distance[building[0], building_sub[0], "relation"] = math.sqrt((building[1][0] - building_sub[1][0])*(building[1][0] - building_sub[1][0]) + (building[1][1] - building_sub[1][1])*(building[1][1] - building_sub[1][1]))
				if math.sqrt((building[3][1] - building_sub[4][1])*(building[3][1] - building_sub[4][1])) <= 6 * building[2] / 2500:
					building_relations[building[0], building_sub[0], "near"] = "near"
				else:
					building_relations[building[0], building_sub[0], "near"] = math.sqrt((building_sub[3][1] - building[4][1])*(building_sub[3][1] - building[4][1]))
			if (isLeft(building[1], building[3], building_sub[1]) == True) and (isLeft(building[1], [building[4][0], building[3][1]], building_sub[1]) == True):
				building_relations[building[0], building_sub[0], "relation"] = "west"
				building_distance[building[0], building_sub[0], "relation"] = math.sqrt((building[1][0] - building_sub[1][0])*(building[1][0] - building_sub[1][0]) + (building[1][1] - building_sub[1][1])*(building[1][1] - building_sub[1][1]))
				if math.sqrt((building_sub[3][0] - building[4][0])*(building_sub[3][0] - building[4][0])) <= 6 * building[2] / 2500:
					building_relations[building[0], building_sub[0], "near"] = "near"
				else:
					building_relations[building[0], building_sub[0], "near"] = math.sqrt((building_sub[3][1] - building[4][1])*(building_sub[3][1] - building[4][1]))
			if (isLeft(building[1], building[3], building_sub[1]) == False) and (isLeft(building[1], [building[4][0], building[3][1]], building_sub[1]) == False):
				building_relations[building[0], building_sub[0], "relation"] = "east"
				building_distance[building[0], building_sub[0], "relation"] = math.sqrt((building[1][0] - building_sub[1][0])*(building[1][0] - building_sub[1][0]) + (building[1][1] - building_sub[1][1])*(building[1][1] - building_sub[1][1]))
				if math.sqrt((building[3][0] - building_sub[4][0])*(building[3][0] - building_sub[4][0])) <= 6 * building[2] / 2500:
					building_relations[building[0], building_sub[0], "near"] = "near"
				else:
					building_relations[building[0], building_sub[0], "near"] = math.sqrt((building_sub[3][1] - building[4][1])*(building_sub[3][1] - building[4][1]))

#Reduce the number of spatial relations.
a = 1
while a < 27 :
	b = 1
	target_building_N = ""
	distance_count_N = math.sqrt(495*495+275*275)
	testing_building_N = ""
	building_near_N = ""
	target_building_S = ""
	distance_count_S = math.sqrt(495*495+275*275)
	testing_building_S = ""
	building_near_S = ""
	target_building_W = ""
	distance_count_W = math.sqrt(495*495+275*275)
	testing_building_W = ""
	building_near_W = ""
	target_building_E = ""
	distance_count_E = math.sqrt(495*495+275*275)
	testing_building_E = ""
	building_near_E = ""
	while b < 27 :
		if label[a] != label[b]:
			if building_relations[label[a], label[b], "relation"] == "north":	
				if distance_count_N >= building_distance[label[a], label[b], "relation"]:
					distance_count_N = building_distance[label[a], label[b], "relation"]
					target_building_N = label[b]
					testing_building_N = label[a]
					if building_relations[label[a], label[b], "near"] == "near":
						building_near_N = "near"
			if building_relations[label[a], label[b], "relation"] == "south":	
				if distance_count_S >= building_distance[label[a], label[b], "relation"]:
					distance_count_S = building_distance[label[a], label[b], "relation"]
					target_building_S = label[b]
					testing_building_S = label[a]
					if building_relations[label[a], label[b], "near"] == "near":
						building_near_S = "near"
			if building_relations[label[a], label[b], "relation"] == "west":	
				if distance_count_W >= building_distance[label[a], label[b], "relation"]:
					distance_count_W = building_distance[label[a], label[b], "relation"]
					target_building_W = label[b]
					testing_building_W = label[a]
					if building_relations[label[a], label[b], "near"] == "near":
						building_near_W = "near"
			if building_relations[label[a], label[b], "relation"] == "east":	
				if distance_count_E >= building_distance[label[a], label[b], "relation"]:
					distance_count_E = building_distance[label[a], label[b], "relation"]
					target_building_E = label[b]
					testing_building_E = label[a]
					if building_relations[label[a], label[b], "near"] == "near":
						building_near_E = "near"
		b += 1
	a += 1

	#Further reduce the number of spatial relations.
	temp_list = []
	target_building = ""
	if distance_count_N != math.sqrt(495*495+275*275):
		if building_near_N == "near":
			temp_list.append(["south" , target_building_N, "near"])
		else:
			temp_list.append(["south" , target_building_N, "not near"])
		target_building = testing_building_N
	if distance_count_S != math.sqrt(495*495+275*275):
		if building_near_S == "near":
			temp_list.append(["north" , target_building_S, "near"])
		else:
			temp_list.append(["north" , target_building_S, "not near"])
		target_building = testing_building_S
	if distance_count_W != math.sqrt(495*495+275*275):
		if building_near_W == "near":
			temp_list.append(["east" , target_building_W, "near"])
		else:
			temp_list.append(["east" , target_building_W, "not near"])
		target_building = testing_building_W
	if distance_count_E != math.sqrt(495*495+275*275):
		if building_near_E == "near":
			temp_list.append(["west" , target_building_E, "near"])
		else:
			temp_list.append(["west" , target_building_E, "not near"])
		target_building = testing_building_E
	#Save reduced spatial relations into the reduced_relations list.
	if target_building != "":
		if not reduced_relations:
			reduced_relations.append([target_building, temp_list])
		else:
			existance = False
			for item in reduced_relations:
				if item[0] == target_building:
					existance = True
			if existance == False:
				reduced_relations.append([target_building, temp_list])

# [TESTING] Printing the reduced relations.
# for item in reduced_relations:
# 	print item
# 	print ""

# Importing Tkinter GUI library
from Tkinter import *

master = Tk()

# Callback function for mouse left clicks.
def callback(event):
	##Reset the image in a new click.
	#Open the integer value campus image
	campus_region = cv2.imread("ass3-campus.pgm")
	#Save the modified image to image_with_points.png file.
	cv2.imwrite('image_with_points.png', campus_region)

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
			for item in building_properties:
				if contour_name == item[0]:
					start_and_destination[0] = [item[1][0], item[1][1]]
					print colored("Start from: " + str(start_and_destination[0]), 'blue')

	#If the point is not in any building contours, codes within this if-statement compute the location description of the point.
	if contour_fall == "":
		start_and_destination[0] = [event.x, event.y]
		print colored("Start from: " + str(start_and_destination[0]), 'blue')
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
			print colored(item, 'blue')

		# The following code finds and draws all points sharing similar location descriptions.

		#Improve running efficiency using the following loops. They go over all point within a region of interest 100 pixel * 100 pixel (mouse pixel in the middle)
		x = event.x - 50
		while x <= event.x + 50:
			y = event.y - 50
			while y <= event.y + 50:
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
			print colored(contour_name, 'green')
			for item in building_properties:
				if contour_name == item[0]:
					start_and_destination[1] = [item[1][0], item[1][1]]
					print colored("End at: " + str(start_and_destination[1]), 'green')
	#If the point is not in any building contours, codes within this if-statement compute the location description of the point.
	if contour_fall == "":
		start_and_destination[1] = [event.x, event.y]
		print colored("End at: " + str(start_and_destination[1]), 'green')
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
		x = event.x - 50
		while x <= event.x + 50:
			y = event.y - 50
			while y <= event.y + 50:
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

def key(event):
    description_start = []
    description_end = []
    route = []
    if start_and_destination[0] == []:
    	print colored("Please select a start point from the campus map using a left click", "red")
    if start_and_destination[1] == []:
    	print colored("Please select a end point from the campus map using a right click", "red")
    else:
    	findRoute(start_and_destination[0], start_and_destination[1], description_start, description_end)

	#[Testing] Print all descriptions for the point.
	# for item in description_start:
	# 	print colored(item, 'red')
	# for item in description_end:
	# 	print colored(item, 'red')

	# [Testing] Print relations between the two points
	# if start_and_destination[1][0] >= start_and_destination[0][0] and start_and_destination[1][1] <= start_and_destination[0][1]:
	# 	print "end point to the upper right cornor"
	# if start_and_destination[1][0] >= start_and_destination[0][0] and start_and_destination[1][1] >= start_and_destination[0][1]:
	# 	print "end point to the lower right cornor"
	# if start_and_destination[1][0] <= start_and_destination[0][0] and start_and_destination[1][1] <= start_and_destination[0][1]:
	# 	print "end point to the upper left cornor"
	# if start_and_destination[1][0] <= start_and_destination[0][0] and start_and_destination[1][1] >= start_and_destination[0][1]:
	# 	print "end point to the lower left cornor"

	if description_start == description_end:
		print colored("Start point and destination point are in the same region or building gesture", "red")
	else:
		#[Testing] Print all descriptions for the point.
		# for item in description_start:
		# 	print colored(item, 'red')
		# for item in description_end:
		# 	print colored(item, 'red')
		if start_and_destination[1][0] >= start_and_destination[0][0] and start_and_destination[1][1] <= start_and_destination[0][1]:
			for item in description_start:
				if item[1] == "south":
					for building in building_properties:
						if building[0] == item[2]:
							extrema = building[7]
							size_description = building[6]
					route.append(["north", item[3], extrema, size_description, item[2]])
					findEachRoute(item[2], description_end[0][0], item[3], "upper_right", "south", route)
				if item[1] == "west":
					for building in building_properties:
						if building[0] == item[2]:
							extrema = building[7]
							size_description = building[6]
					route.append(["east", item[3], extrema, size_description, item[2]])
					findEachRoute(item[2], description_end[0][0], item[3], "upper_right", "west", route)
		if start_and_destination[1][0] >= start_and_destination[0][0] and start_and_destination[1][1] >= start_and_destination[0][1]:
			for item in description_start:
				if item[1] == "north":
					for building in building_properties:
						if building[0] == item[2]:
							extrema = building[7]
							size_description = building[6]
					route.append(["south", item[3], extrema, size_description, item[2]])
					findEachRoute(item[2], description_end[0][0], item[3], "lower_right", "north", route)
				if item[1] == "west":
					for building in building_properties:
						if building[0] == item[2]:
							extrema = building[7]
							size_description = building[6]
					route.append(["east", item[3], extrema, size_description, item[2]])
					findEachRoute(item[2], description_end[0][0], item[3], "lower_right", "west", route)
		if start_and_destination[1][0] <= start_and_destination[0][0] and start_and_destination[1][1] <= start_and_destination[0][1]:
			for item in description_start:
				if item[1] == "south":
					for building in building_properties:
						if building[0] == item[2]:
							extrema = building[7]
							size_description = building[6]
					route.append(["north", item[3], extrema, size_description, item[2]])
					findEachRoute(item[2], description_end[0][0], item[3], "upper_left", "south", route)
				if item[1] == "east":
					for building in building_properties:
						if building[0] == item[2]:
							extrema = building[7]
							size_description = building[6]
					route.append(["west", item[3], extrema, size_description, item[2]])
					findEachRoute(item[2], description_end[0][0], item[3], "upper_left", "east", route)
		if start_and_destination[1][0] <= start_and_destination[0][0] and start_and_destination[1][1] >= start_and_destination[0][1]:
			for item in description_start:
				if item[1] == "north":
					for building in building_properties:
						if building[0] == item[2]:
							extrema = building[7]
							size_description = building[6]
					route.append(["south", item[3], extrema, size_description, item[2]])
					findEachRoute(item[2], description_end[0][0], item[3], "lower_left", "north", route)
				if item[1] == "east":
					for building in building_properties:
						if building[0] == item[2]:
							extrema = building[7]
							size_description = building[6]
					route.append(["west", item[3], extrema, size_description, item[2]])
					findEachRoute(item[2], description_end[0][0], item[3], "lower_left", "east", route)

def findRoute(start, end, description_start, description_end):
	#If the start point fall into a building contour, this variable stores the name of the building.
	start_building_name = ""
	#If the end point fall into a building contour, this variable stores the name of the building.
	end_building_name = ""

	#This for-loop checks whether the start and end points fall into a building contour. If they are the name of the building will be stored to start_building_name and end_building_name variable accordingly.
	for h,cnt in enumerate(contours):
		#If the start point is in any building contours, store the name in the start_building_name variable.
		if cv2.pointPolygonTest(cnt,(start[0], start[1]),True) >= 0:
			count = 0
			integer_value = 0
			for demensions in cnt:
				for values in demensions:
					integer_value += integer_value_campus.getpixel((int(values[0]), int(values[1])))
					count += 1
					#Get the name of the building by passing the variable to the hashtable label.
					start_building_name = label[integer_value / count]
		#If the end point is in any building contours, store the name in the end_building_name variable.
		if cv2.pointPolygonTest(cnt,(end[0], end[1]),True) >= 0:
			count = 0
			integer_value = 0
			for demensions in cnt:
				for values in demensions:
					integer_value += integer_value_campus.getpixel((int(values[0]), int(values[1])))
					count += 1
					#Get the name of the building by passing the variable to the hashtable label.
					end_building_name = label[integer_value / count]

	# Following codes find spatial relations for the start point.
	spatial_relations = []
	#This for-loop goes over all buildings in the building_properties variable (including a list of building_name, building_contour_center, building_contour_area, building_contour_upper_left, building_contour_lower_right, building_shape, building_size_description, building_location_extrema_description). 
	for building in building_properties:
		if building[0] != start_building_name:
			#These if-and-else-statement checks and store building names and relations to the points to the spatial_relations list variable.
			if (isLeft(building[1], building[3], start) == False) and (isLeft(building[1], [building[4][0], building[3][1]], start) == True):
				if math.sqrt((start[1] - building[4][1])*(start[1] - building[4][1])) <= 10 * building[2] / 2500:
					spatial_relations.append(["south", building[0], math.sqrt((building[1][0] - start[0])*(building[1][0] - start[0]) + (building[1][1] - start[1])*(building[1][1] - start[1])), "near"])
				else:
					spatial_relations.append(["south", building[0], math.sqrt((building[1][0] - start[0])*(building[1][0] - start[0]) + (building[1][1] - start[1])*(building[1][1] - start[1])), "not near"])
			if (isLeft(building[1], building[3], start) == True) and (isLeft(building[1], [building[4][0], building[3][1]], start) == False):
				if math.sqrt((building[3][1] - start[1])*(building[3][1] - start[1])) <= 10 * building[2] / 2500:
					spatial_relations.append(["north", building[0], math.sqrt((building[1][0] - start[0])*(building[1][0] - start[0]) + (building[1][1] - start[1])*(building[1][1] - start[1])), "near"])
				else:
					spatial_relations.append(["north", building[0], math.sqrt((building[1][0] - start[0])*(building[1][0] - start[0]) + (building[1][1] - start[1])*(building[1][1] - start[1])), "not near"])
			if (isLeft(building[1], building[3], start) == True) and (isLeft(building[1], [building[4][0], building[3][1]], start) == True):
				if math.sqrt((start[0] - building[4][0])*(start[0] - building[4][0])) <= 10 * building[2] / 2500:
					spatial_relations.append(["east", building[0], math.sqrt((building[1][0] - start[0])*(building[1][0] - start[0]) + (building[1][1] - start[1])*(building[1][1] - start[1])), "near"])
				else:
					spatial_relations.append(["east", building[0], math.sqrt((building[1][0] - start[0])*(building[1][0] - start[0]) + (building[1][1] - start[1])*(building[1][1] - start[1])), "not near"])
			if (isLeft(building[1], building[3], start) == False) and (isLeft(building[1], [building[4][0], building[3][1]], start) == False):
				if math.sqrt((building[3][0] - start[0])*(building[3][0] - start[0])) <= 10 * building[2] / 2500:
					spatial_relations.append(["west", building[0], math.sqrt((building[1][0] - start[0])*(building[1][0] - start[0]) + (building[1][1] - start[1])*(building[1][1] - start[1])), "near"])
				else:
					spatial_relations.append(["west", building[0], math.sqrt((building[1][0] - start[0])*(building[1][0] - start[0]) + (building[1][1] - start[1])*(building[1][1] - start[1])), "not near"])
	
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

	#These if-statements update and save the most immediate relation (nearest/ north/ south/ west/ east) of a point (with shortest distance to a building gesture) from temporary variables to descriptions list and point_stack string variable.
	if distance_N != math.sqrt(495*495+275*275):
		if near_N == "near":
			description_start.append([start_building_name, "north", building_N, "near"])
		else:
			description_start.append([start_building_name, "north", building_N, "not near"])
	if distance_S != math.sqrt(495*495+275*275):
		if near_S == "near":
			description_start.append([start_building_name, "south", building_S, "near"])
		else:
			description_start.append([start_building_name, "south", building_S, "not near"])
	if distance_W != math.sqrt(495*495+275*275):
		if near_W == "near":
			description_start.append([start_building_name, "west", building_W, "near"])
		else:
			description_start.append([start_building_name, "west", building_W, "not near"])
	if distance_E != math.sqrt(495*495+275*275):
		if near_E == "near":
			description_start.append([start_building_name, "east", building_E, "near"])
		else:
			description_start.append([start_building_name, "east", building_E, "not near"])

	# Following codes find spatial relations for the end point.
	spatial_relations = []
	#This for-loop goes over all buildings in the building_properties variable (including a list of building_name, building_contour_center, building_contour_area, building_contour_upper_left, building_contour_lower_right, building_shape, building_size_description, building_location_extrema_description). 
	for building in building_properties:
		if building[0] != end_building_name:
			#These if-and-else-statement checks and store building names and relations to the points to the spatial_relations list variable.
			if (isLeft(building[1], building[3], end) == False) and (isLeft(building[1], [building[4][0], building[3][1]], end) == True):
				if math.sqrt((end[1] - building[4][1])*(end[1] - building[4][1])) <= 10 * building[2] / 2500:
					spatial_relations.append(["south", building[0], math.sqrt((building[1][0] - end[0])*(building[1][0] - end[0]) + (building[1][1] - end[1])*(building[1][1] - end[1])), "near"])
				else:
					spatial_relations.append(["south", building[0], math.sqrt((building[1][0] - end[0])*(building[1][0] - end[0]) + (building[1][1] - end[1])*(building[1][1] - end[1])), "not near"])
			if (isLeft(building[1], building[3], end) == True) and (isLeft(building[1], [building[4][0], building[3][1]], end) == False):
				if math.sqrt((building[3][1] - end[1])*(building[3][1] - end[1])) <= 10 * building[2] / 2500:
					spatial_relations.append(["north", building[0], math.sqrt((building[1][0] - end[0])*(building[1][0] - end[0]) + (building[1][1] - end[1])*(building[1][1] - end[1])), "near"])
				else:
					spatial_relations.append(["north", building[0], math.sqrt((building[1][0] - end[0])*(building[1][0] - end[0]) + (building[1][1] - end[1])*(building[1][1] - end[1])), "not near"])
			if (isLeft(building[1], building[3], end) == True) and (isLeft(building[1], [building[4][0], building[3][1]], end) == True):
				if math.sqrt((end[0] - building[4][0])*(end[0] - building[4][0])) <= 10 * building[2] / 2500:
					spatial_relations.append(["east", building[0], math.sqrt((building[1][0] - end[0])*(building[1][0] - end[0]) + (building[1][1] - end[1])*(building[1][1] - end[1])), "near"])
				else:
					spatial_relations.append(["east", building[0], math.sqrt((building[1][0] - end[0])*(building[1][0] - end[0]) + (building[1][1] - end[1])*(building[1][1] - end[1])), "not near"])
			if (isLeft(building[1], building[3], end) == False) and (isLeft(building[1], [building[4][0], building[3][1]], end) == False):
				if math.sqrt((building[3][0] - end[0])*(building[3][0] - end[0])) <= 10 * building[2] / 2500:
					spatial_relations.append(["west", building[0], math.sqrt((building[1][0] - end[0])*(building[1][0] - end[0]) + (building[1][1] - end[1])*(building[1][1] - end[1])), "near"])
				else:
					spatial_relations.append(["west", building[0], math.sqrt((building[1][0] - end[0])*(building[1][0] - end[0]) + (building[1][1] - end[1])*(building[1][1] - end[1])), "not near"])
	
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

	#These if-statements update and save the most immediate relation (nearest/ north/ south/ west/ east) of a point (with shortest distance to a building gesture) from temporary variables to descriptions list and point_stack string variable.
	if distance_N != math.sqrt(495*495+275*275):
		if near_N == "near":
			description_end.append([end_building_name, "north", building_N, "near"])
		else:
			description_end.append([end_building_name, "north", building_N, "not near"])
	if distance_S != math.sqrt(495*495+275*275):
		if near_S == "near":
			description_end.append([end_building_name, "south", building_S, "near"])
		else:
			description_end.append([end_building_name, "south", building_S, "not near"])
	if distance_W != math.sqrt(495*495+275*275):
		if near_W == "near":
			description_end.append([end_building_name, "west", building_W, "near"])
		else:
			description_end.append([end_building_name, "west", building_W, "not near"])
	if distance_E != math.sqrt(495*495+275*275):
		if near_E == "near":
			description_end.append([end_building_name, "east", building_E, "near"])
		else:
			description_end.append([end_building_name, "east", building_E, "not near"])

#Recursive function for finding and displaying routes.
def findEachRoute(start, end, short, cornor, orientation, route):
	if start != end:
		for item in reduced_relations:
			if item[0] == start:
				#This flag allow the function to pop unrelated routes.
				havetarget = False
				for related_item in item[1]:
					#If the building name exists in the list, it will not be considered again.
					existance = False
					for item in route:
						if item[4] == related_item[1]:
							existance = True
					if existance == False:
						if cornor == "upper_right":
							if related_item[0] == "north":
								for building in building_properties:
									if building[0] == related_item[1]:
										extrema = building[7]
										size_description = building[6]
								route.append(["north", related_item[2], extrema, size_description, related_item[1]])
								findEachRoute(related_item[1], end, related_item[2], cornor, "north", route)
								havetarget = True
							if related_item[0] == "east":
								for building in building_properties:
									if building[0] == related_item[1]:
										extrema = building[7]
										size_description = building[6]
								route.append(["east", related_item[2], extrema, size_description, related_item[1]])
								findEachRoute(related_item[1], end, related_item[2], cornor, "east", route)
								havetarget = True
						if cornor == "lower_right":
							if related_item[0] == "south":
								for building in building_properties:
									if building[0] == related_item[1]:
										extrema = building[7]
										size_description = building[6]
								route.append(["south", related_item[2], extrema, size_description, related_item[1]])
								findEachRoute(related_item[1], end, related_item[2], cornor, "south", route)
								havetarget = True
							if related_item[0] == "east":
								for building in building_properties:
									if building[0] == related_item[1]:
										extrema = building[7]
										size_description = building[6]
								route.append(["east", related_item[2], extrema, size_description, related_item[1]])
								findEachRoute(related_item[1], end, related_item[2], cornor, "east", route)
								havetarget = True
						if cornor == "upper_left":
							if related_item[0] == "north":
								for building in building_properties:
									if building[0] == related_item[1]:
										extrema = building[7]
										size_description = building[6]
								route.append(["north", related_item[2], extrema, size_description, related_item[1]])
								findEachRoute(related_item[1], end, related_item[2], cornor, "north", route)
								havetarget = True
							if related_item[0] == "west":
								for building in building_properties:
									if building[0] == related_item[1]:
										extrema = building[7]
										size_description = building[6]
								route.append(["west", related_item[2], extrema, size_description, related_item[1]])
								findEachRoute(related_item[1], end, related_item[2], cornor, "west", route)
								havetarget = True
						if cornor == "lower_left":
							if related_item[0] == "south":
								for building in building_properties:
									if building[0] == related_item[1]:
										extrema = building[7]
										size_description = building[6]
								route.append(["south", related_item[2], extrema, size_description, related_item[1]])
								findEachRoute(related_item[1], end, related_item[2], cornor, "south", route)
								havetarget = True
							if related_item[0] == "west":
								for building in building_properties:
									if building[0] == related_item[1]:
										extrema = building[7]
										size_description = building[6]
								route.append(["west", related_item[2], extrema, size_description, related_item[1]])
								findEachRoute(related_item[1], end, related_item[2], cornor, "west", route)
								havetarget = True
				#Pop unrelated routes if the flag is false (no routes are found).
				if havetarget == False:
					route.pop()
	else:
		#Recursively print the routes in the console.
		print colored("----------Suggested Routes----------", "yellow")
		for item in route:
			if item[1] == "near":
				print "Walk to the " + colored(item[0], "blue") + " toward the nearby " + colored(item[3], "green") + " " + colored(item[3], "green") + " building: " + colored(item[4], "red") + "."
			else:
				print "Walk to the " + colored(item[0], "blue") + " toward the " + colored(item[3], "green") + " " + colored(item[2], "green") + " building: " + colored(item[4], "red") + "."
			if item != route[len(route) - 1]:
				print "          |"
				print "          |"
				print "          V"
				print "And then from the building: " + colored(item[4], "red")

photo = PhotoImage(file="ass3-campus.pgm")
w = Label(None, image=photo)
w.photo = photo
w.bind("<Return>", key)
w.focus()
w.bind("<Button-1>", callback)
w.bind("<Button-2>", callback2)
w.pack()

mainloop()