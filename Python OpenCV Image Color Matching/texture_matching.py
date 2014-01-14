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
    #Convert ppm images to gray scale images.
    ppm_imgray = cv2.cvtColor(ppm_img,cv2.COLOR_BGR2GRAY)
    #Save gray scale ppm images.
    cv2.imwrite("grayscale/ppm/" + ppm_infile.replace("images/", "").replace(".ppm", ".jpg"), ppm_imgray)

    #Calculates the Laplacian of an image. The function calculates the Laplacian of the source image by adding up the second x and y derivatives calculated using the Sobel operator.
    ppm_gray_lap = cv2.Laplacian(ppm_imgray,cv2.CV_16S,ksize=3,scale=1,delta=0)
    #Converts input array elements to another 8-bit unsigned integer with optional linear transformation.
    ppm_dst = cv2.convertScaleAbs(ppm_gray_lap)
    #Save paplacian ppm images.
    cv2.imwrite("laplacian/ppm/" + ppm_infile.replace("images/", "").replace(".ppm", ".jpg"), ppm_dst)

    #Create ppm binary mask, a 8-bit image, where white denotes that region should be used for histogram calculations, and black means it should not.
    ppm_ret, ppm_thresh_mask = cv2.threshold(ppm_dst,127,255,0)
    #Save 8 bit mask images.
    cv2.imwrite("8bitmask/ppm/" + ppm_infile.replace("images/", "").replace(".ppm", ".jpg"), ppm_thresh_mask)

    #Calculates a histogram for the 8-bit region marked in the mask using a set of arrays.
    ppm_hist = cv2.calcHist([ppm_dst],[0],ppm_thresh_mask,[256],[0,255])
    #Normalize the value to fall below 255 and fit in image height.
    cv2.normalize(ppm_hist,ppm_hist,0,255,cv2.NORM_MINMAX)
    #Evenly round to the given number of decimals. For values exactly halfway between rounded decimal values, Numpy rounds to the nearest even value.
    round_ppm_hist = np.int32(np.around(ppm_hist))
    for x,fliped_ppm in enumerate(round_ppm_hist):
        cv2.line(ppm_h,(x,0),(x,fliped_ppm),(255,255,255))
    fliped_ppm = np.flipud(ppm_h)

    cv2.imwrite("one_dimensional_histograms/ppm/" + ppm_infile.replace("images/", "").replace(".ppm", ".jpg"), fliped_ppm)

    for jpg_infile in glob.glob( os.path.join("images", '*.jpg') ):
        #Loads each jpg images from the image folder.
        jpg_img = cv2.imread(jpg_infile)
        #For drawing the histogram.
        jpg_h = np.zeros((300,256,3))
        #Convert jpg image to gray scale.
        jpg_imgray = cv2.cvtColor(jpg_img,cv2.COLOR_BGR2GRAY)
        #Save gray scale jpg images.
        cv2.imwrite("grayscale/jpg/" + jpg_infile.replace("images/", "").replace(".ppm", ".jpg"), jpg_imgray)
        
        #Calculates the Laplacian of an image. The function calculates the Laplacian of the source image by adding up the second x and y derivatives calculated using the Sobel operator.
        jpg_gray_lap = cv2.Laplacian(jpg_imgray,cv2.CV_16S,ksize=3,scale=1,delta=0)
        #Converts input array elements to another 8-bit unsigned integer with optional linear transformation.
        jpg_dst = cv2.convertScaleAbs(jpg_gray_lap)
        #Save paplacian jpg images.
        cv2.imwrite("laplacian/jpg/" + jpg_infile.replace("images/", "").replace(".ppm", ".jpg"), jpg_dst)

        #Create jpg binary mask, a 8-bit image, where white denotes that region should be used for histogram calculations, and black means it should not.
        jpg_ret, jpg_thresh_mask = cv2.threshold(jpg_dst,127,255,0)
        #Save 8 bit mask images.
        cv2.imwrite("8bitmask/jpg/" + jpg_infile.replace("images/", "").replace(".ppm", ".jpg"), jpg_thresh_mask)

        #Calculates a histogram for the 8-bit region marked in the mask using a set of arrays.
        jpg_hist = cv2.calcHist([jpg_dst],[0],jpg_thresh_mask,[256],[0,255])
        #Normalize the value to fall below 255 and fit in image height.
        cv2.normalize(jpg_hist,jpg_hist,0,255,cv2.NORM_MINMAX)
        #Evenly round to the given number of decimals. For values exactly halfway between rounded decimal values, Numpy rounds to the nearest even value.
        round_jpg_hist = np.int32(np.around(jpg_hist))
        for x,fliped_jpg in enumerate(round_jpg_hist):
            cv2.line(jpg_h,(x,0),(x,fliped_jpg),(255,255,255))
        #Flip the image vertically.
        fliped_jpg = np.flipud(jpg_h)

        #Save one dimensional histogram
        cv2.imwrite("one_dimensional_histograms/jpg/" + jpg_infile.replace("images/", "").replace(".ppm", ".jpg"), fliped_jpg)

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
    if not os.path.exists("texture_matching_results/" + ppm_infile.replace("images/", "").replace(".ppm", "/")):
        os.makedirs("texture_matching_results/" + ppm_infile.replace("images/", "").replace(".ppm", "/"))

    #Write result images to targeted folders.
    cv2.imwrite("texture_matching_results/" + ppm_infile.replace("images/", "").replace(".ppm", "/") + ppm_infile.replace("images/", ""), img1)
    cv2.imwrite("texture_matching_results/" + ppm_infile.replace("images/", "").replace(".ppm", "/") + high_correlation.replace("images/", ""), img2)
    cv2.imwrite("texture_matching_results/" + ppm_infile.replace("images/", "").replace(".ppm", "/") + low_correlation.replace("images/", ""), img3)
        