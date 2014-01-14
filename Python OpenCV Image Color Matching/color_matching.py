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
    #Loads each ppm images from the image folder.
    ppm_img = cv2.imread(ppm_infile)
    #For drawing the histogram.
    ppm_h = np.zeros((300,256,3))
    #Convert ppm image to gray scale.
    ppm_imgray = cv2.cvtColor(ppm_img,cv2.COLOR_BGR2GRAY)
    #Create ppm binary mask, a 8-bit image, where white denotes that region should be used for histogram calculations, and black means it should not.
    ppm_ret, ppm_thresh_mask = cv2.threshold(ppm_imgray,127,255,0)
    #Return number of bins (2-D array). Return 256 bins since we have 256 colors.

    cv2.imwrite("8bitmask/" + ppm_infile.replace("images/", "").replace(".ppm", ".jpg"), ppm_thresh_mask)

    #Number of bins, since the histogram has 256 colors, it needs 256 bins. Bin is a multidimensional array.
    ppm_bins = np.arange(256).reshape(256,1)
    color = [ (255,0,0),(0,255,0),(0,0,255) ]
    #Iterate an enumerate tuple containing a count and the values obtained from iterating over the list color.
    for ch, col in enumerate(color):
        #Calculates a histogram for the 8-bit region marked in the mask using a set of arrays.
        ppm_hist = cv2.calcHist([ppm_img],[ch],ppm_thresh_mask,[256],[0,256])
        #Normalize the value to fall below 255 and fit in image height.
        cv2.normalize(ppm_hist,ppm_hist,0,255,cv2.NORM_MINMAX)
        #Evenly round to the given number of decimals. For values exactly halfway between rounded decimal values, Numpy rounds to the nearest even value.
        round_ppm_hist = np.int32(np.around(ppm_hist))
        #Stack bins and hist for drawing the polylines.
        ppm_pts = np.column_stack((ppm_bins,round_ppm_hist))
        #Draw polylines to represent the histogram.
        cv2.polylines(ppm_h,[ppm_pts],False,col)

    #Flip the image vertically.
    ppm_h=np.flipud(ppm_h)

    cv2.imwrite("histograms/ppm/" + ppm_infile.replace("images/", "").replace(".ppm", ".jpg"), ppm_h)

    for jpg_infile in glob.glob( os.path.join("images", '*.jpg') ):
        #Loads each jpg images from the image folder.
        jpg_img = cv2.imread(jpg_infile)
        #For drawing the histogram.
        jpg_h = np.zeros((300,256,3))
        #Convert jpg image to gray scale.
        jpg_imgray = cv2.cvtColor(jpg_img,cv2.COLOR_BGR2GRAY)
        #Create jpg binary mask, a 8-bit image, where white denotes that region should be used for histogram calculations, and black means it should not.
        jpg_ret, jpg_thresh_mask = cv2.threshold(jpg_imgray,127,255,0)
        #Return number of bins (2-D array). Return 256 bins since we have 256 colors.
        jpg_bins = np.arange(256).reshape(256,1)
        color = [ (255,0,0),(0,255,0),(0,0,255) ]
        #Iterate an enumerate tuple containing a count and the values obtained from iterating over the list color.
        for ch, col in enumerate(color):
            #Calculates a histogram for the 8-bit region marked in the mask using a set of arrays.
            jpg_hist = cv2.calcHist([jpg_img],[ch],jpg_thresh_mask,[256],[0,256])
            #Normalize the value to fall below 255 and fit in image height.
            cv2.normalize(jpg_hist,jpg_hist,0,255,cv2.NORM_MINMAX)
            #Evenly round to the given number of decimals. For values exactly halfway between rounded decimal values, Numpy rounds to the nearest even value.
            round_jpg_hist = np.int32(np.around(jpg_hist))
            #Stack bins and hist for drawing the polylines.
            jpg_pts = np.column_stack((jpg_bins,round_jpg_hist))
            #Draw polylines to represent the histogram.
            cv2.polylines(jpg_h,[jpg_pts],False,col)

        #Flip the image vertically.
        jpg_h=np.flipud(jpg_h)

        cv2.imwrite("histograms/jpg/" + jpg_infile.replace("images/", "").replace(".ppm", ".jpg"), jpg_h)

        #Compare the correlation of two histograms and return a numerical parameter that express how well two histograms match with each other.
        counter = cv2.compareHist(ppm_hist, jpg_hist, cv.CV_COMP_CORREL)

        #Initialization of the result interpretation.
        if high_correlation == "" and low_correlation == "":
            high_counter = counter
            low_counter = counter
            high_correlation = jpg_infile
            low_correlation = jpg_infile
        #Find the most similar jpg image.
        if counter >= high_counter:
            high_counter = counter
            high_correlation = jpg_infile
        #Find the most dissimilar jpg image.
        if counter <= low_counter:
            low_counter = counter
            low_correlation = jpg_infile
    #Print the result using colored text supported by the termcolor library of terminal.
    print colored("Reading PPM Image: " + ppm_infile, 'red')
    print colored("Most Similar JPG image: " + high_correlation + "     Correlation Value: " + str(high_counter), 'blue')
    print colored("Most Dissimilar JPG image: " + low_correlation + "  Correlation Value: " + str(low_counter), 'blue')
    print ""
    img1 = cv2.imread(ppm_infile)
    img2 = cv2.imread(high_correlation)
    img3 = cv2.imread(low_correlation)

    #Setup the result folders.
    if not os.path.exists("color_matching_results/" + ppm_infile.replace("images/", "").replace(".ppm", "/")):
        os.makedirs("color_matching_results/" + ppm_infile.replace("images/", "").replace(".ppm", "/"))

    #Write result images to targeted folders.
    cv2.imwrite("color_matching_results/" + ppm_infile.replace("images/", "").replace(".ppm", "/") + ppm_infile.replace("images/", ""), img1)
    cv2.imwrite("color_matching_results/" + ppm_infile.replace("images/", "").replace(".ppm", "/") + high_correlation.replace("images/", ""), img2)
    cv2.imwrite("color_matching_results/" + ppm_infile.replace("images/", "").replace(".ppm", "/") + low_correlation.replace("images/", ""), img3)