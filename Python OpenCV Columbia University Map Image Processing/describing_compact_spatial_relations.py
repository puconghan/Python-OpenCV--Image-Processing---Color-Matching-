import os
import glob
import cv2
from PIL import Image
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

a = 1
while a < 27 :
	b = 1
	target_building_N = ""
	distance_count_N = math.sqrt(495*495+275*275)
	testing_building_N = ""
	target_building_S = ""
	distance_count_S = math.sqrt(495*495+275*275)
	testing_building_S = ""
	target_building_W = ""
	distance_count_W = math.sqrt(495*495+275*275)
	testing_building_W = ""
	target_building_E = ""
	distance_count_E = math.sqrt(495*495+275*275)
	testing_building_E = ""
	while b < 27 :
		if label[a] != label[b]:
			if building_relations[label[a], label[b], "relation"] == "north":	
				if distance_count_N >= building_distance[label[a], label[b], "relation"]:
					distance_count_N = building_distance[label[a], label[b], "relation"]
					target_building_N = label[b]
					testing_building_N = label[a]
			if building_relations[label[a], label[b], "relation"] == "south":	
				if distance_count_S >= building_distance[label[a], label[b], "relation"]:
					distance_count_S = building_distance[label[a], label[b], "relation"]
					target_building_S = label[b]
					testing_building_S = label[a]
			if building_relations[label[a], label[b], "relation"] == "west":	
				if distance_count_W >= building_distance[label[a], label[b], "relation"]:
					distance_count_W = building_distance[label[a], label[b], "relation"]
					target_building_W = label[b]
					testing_building_W = label[a]
			if building_relations[label[a], label[b], "relation"] == "east":	
				if distance_count_E >= building_distance[label[a], label[b], "relation"]:
					distance_count_E = building_distance[label[a], label[b], "relation"]
					target_building_E = label[b]
					testing_building_E = label[a]
			# print label[a] + " is to the " + building_relations[label[a], label[b], "relation"] + " of " + label[b]
			if building_relations[label[a], label[b], "near"] == "near":
				# print colored(label[a] + " is " + building_relations[label[a], label[b], "near"] + " to the " + label[b], 'red')
				near_relations.append([label[a], label[b]])
		b += 1
	a += 1
	if distance_count_N != math.sqrt(495*495+275*275):
		reduced_relations.append([testing_building_N, "north" , target_building_N])
	if distance_count_S != math.sqrt(495*495+275*275):
		reduced_relations.append([testing_building_S, "south" , target_building_S])
	if distance_count_W != math.sqrt(495*495+275*275):
		reduced_relations.append([testing_building_W, "west" , target_building_W])
	if distance_count_E != math.sqrt(495*495+275*275):
		reduced_relations.append([testing_building_E, "east" , target_building_E])

print colored("Reduced Relations", 'red')
for item in reduced_relations:
	print item
print colored("Reduced Nearest Relations", 'blue')
for item in near_relations:
	print item






