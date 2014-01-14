##Image histogram is a graphical representation of the intensity distribution of an image. It quantifies the number of pixels for each intensity value considered.

import os
import glob
import cv2
import cv
import numpy as np
from termcolor import colored

for ppm_infile in glob.glob( os.path.join("images", '*.ppm') ):
    high_correlation = ""
    low_correlation = ""

    #Loads each ppm images from the image folder
    ppm_img = cv2.imread(ppm_infile)
    ppm_imgray = cv2.cvtColor(ppm_img,cv2.COLOR_BGR2GRAY)

    #Create binary images
    ppm_ret, ppm_thresh = cv2.threshold(ppm_imgray,127,255,0)

    #Find boundaries of objects from binary images
    ppm_contours, hierarchy = cv2.findContours(ppm_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #[Testing] Draw ppm_contours on the image
    #cv2.drawContours(gray,ppm_contours,-1,(255,0,0),3)

    #Build a numpy array with contours from all layers
    boundaries = ppm_contours[0]
    for layers in ppm_contours:
        if len(boundaries) != len(layers):
            boundaries = np.vstack((boundaries, layers))
    
    #Calculate the x,y, height and width of the contour bounding rectangle 
    x,y,w,h = cv2.boundingRect(boundaries)

    #[Testing] Draw bounding box of the region of interest
    #cv2.rectangle(ppm_img, (x,y), (x+w,y+h), (255,255,255))
    ppm_cropped_img = ppm_img[y:y+h, x:x+w] 

    #[Testing] Draw the croped image
    #cv2.imshow('colorhist',ppm_img)
    #cv2.imshow('colorhist',ppm_cropped_img)
    #cv2.waitKey(0)

    #Return number of bins (2-D array). Return 256 bins since we have 256 colors.
    bins = np.arange(256).reshape(256,1)
    color = [ (255,0,0),(0,255,0),(0,0,255) ]

    #Iterate an enumerate tuple containing a count and the values obtained from iterating over the list color
    for ch, col in enumerate(color):
        #Calculates a histogram of a set of arrays
        ppm_hist = cv2.calcHist([ppm_cropped_img],[ch],None,[256],[0,256])
        #Normalize the value to fall below 255 and fit in image height
        cv2.normalize(ppm_hist,ppm_hist,0,255,cv2.NORM_MINMAX)

    for jpg_infile in glob.glob( os.path.join("images", '*.jpg') ):
        #Loads each jpg images from the image folder
        jpg_img = cv2.imread(jpg_infile)
        jpg_imgray = cv2.cvtColor(jpg_img,cv2.COLOR_BGR2GRAY)
        jpg_ret, jpg_thresh = cv2.threshold(jpg_imgray,127,255,0)
        jpg_contours, jpg_hierarchy = cv2.findContours(jpg_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        boundaries = jpg_contours[0]
        for layers in jpg_contours:
            if len(boundaries) != len(layers):
                boundaries = np.vstack((boundaries, layers))
        x,y,w,h = cv2.boundingRect(boundaries)
        jpg_cropped_img = jpg_img[y:y+h, x:x+w]

        bins = np.arange(256).reshape(256,1)
        color = [ (255,0,0),(0,255,0),(0,0,255) ]
        for ch, col in enumerate(color):
            jpg_hist = cv2.calcHist([jpg_cropped_img],[ch],None,[256],[0,256])
            cv2.normalize(jpg_hist,jpg_hist,0,255,cv2.NORM_MINMAX)
            hist=np.int32(np.around(jpg_hist))
        counter = cv2.compareHist(ppm_hist, jpg_hist, cv.CV_COMP_CORREL)

        if high_correlation == "" and low_correlation == "":
            high_counter = counter
            low_counter = counter
            high_correlation = jpg_infile
            low_correlation = jpg_infile
        if counter >= high_counter:
            high_counter = counter
            high_correlation = jpg_infile
        if counter <= low_counter:
            low_counter = counter
            low_correlation = jpg_infile
    print colored("Reading PPM Image: " + ppm_infile, 'red')
    print colored("Most Similar JPG image: " + high_correlation + "     Correlation Value: " + str(high_counter), 'blue')
    print colored("Most Dissimilar JPG image: " + low_correlation + "  Correlation Value: " + str(low_counter), 'blue')
    print ""
