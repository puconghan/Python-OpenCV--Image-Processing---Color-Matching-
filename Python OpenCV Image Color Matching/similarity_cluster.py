##Image histogram is a graphical representation of the intensity distribution of an image. It quantifies the number of pixels for each intensity value considered.
import os
import glob
import cv2
import cv
import numpy as np
from termcolor import colored

r = 0.2

for ppm_infile in glob.glob( os.path.join("images", '*.ppm') ):
    high_color_correlation = ""
    low_color_correlation = ""
    high_texture_correlation = ""
    low_texture_correlation = ""
    high_combined_correlation = ""
    low_combined_correlation = ""
    #Loads each ppm images from the image folder.
    ppm_img = cv2.imread(ppm_infile)
    #For drawing the histogram.
    ppm_h = np.zeros((300,256,3))
    #Convert ppm image to gray scale.
    ppm_imgray = cv2.cvtColor(ppm_img,cv2.COLOR_BGR2GRAY)
    
    ##Color Histogram Section
    #Create ppm binary mask, a 8-bit image, where white denotes that region should be used for histogram calculations, and black means it should not.
    ppm_ret, ppm_thresh_mask = cv2.threshold(ppm_imgray,127,255,0)
    #Save 8 bit mask images
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
    #Save color histograms
    cv2.imwrite("histograms/ppm/" + ppm_infile.replace("images/", "").replace(".ppm", ".jpg"), ppm_h)

    ##Black and White Texture Histogram Section
    #For drawing the histogram.
    ppm_h = np.zeros((300,256,3))
    #Calculates the Laplacian of an image. The function calculates the Laplacian of the source image by adding up the second x and y derivatives calculated using the Sobel operator.
    ppm_gray_lap = cv2.Laplacian(ppm_imgray,cv2.CV_16S,ksize=3,scale=1,delta=0)
    #Converts input array elements to another 8-bit unsigned integer with optional linear transformation.
    ppm_dst = cv2.convertScaleAbs(ppm_gray_lap)
    #Save paplacian ppm images.
    cv2.imwrite("laplacian/ppm/" + ppm_infile.replace("images/", "").replace(".ppm", ".jpg"), ppm_dst)
    #Create ppm binary mask, a 8-bit image, where white denotes that region should be used for histogram calculations, and black means it should not.
    ppm_ret, ppm_lap_thresh_mask = cv2.threshold(ppm_dst,127,255,0)
    #Save 8 bit mask images.
    cv2.imwrite("8bitmask/ppm/" + ppm_infile.replace("images/", "").replace(".ppm", ".jpg"), ppm_lap_thresh_mask)
    #Calculates a histogram for the 8-bit region marked in the mask using a set of arrays.
    ppm_texture_hist = cv2.calcHist([ppm_dst],[0],ppm_lap_thresh_mask,[256],[0,255])
    #Normalize the value to fall below 255 and fit in image height.
    cv2.normalize(ppm_texture_hist,ppm_texture_hist,0,255,cv2.NORM_MINMAX)
    #Evenly round to the given number of decimals. For values exactly halfway between rounded decimal values, Numpy rounds to the nearest even value.
    round_ppm_texture_hist = np.int32(np.around(ppm_texture_hist))
    for x,fliped_ppm_texture_hist in enumerate(round_ppm_texture_hist):
        cv2.line(ppm_h,(x,0),(x,fliped_ppm_texture_hist),(255,255,255))
    fliped_ppm_texture_hist = np.flipud(ppm_h)
    #Save texture histograms
    cv2.imwrite("one_dimensional_histograms/ppm/" + ppm_infile.replace("images/", "").replace(".ppm", ".jpg"), fliped_ppm_texture_hist)

    for jpg_infile in glob.glob( os.path.join("images", '*.jpg') ):
        #Loads each jpg images from the image folder.
        jpg_img = cv2.imread(jpg_infile)
        #For drawing the histogram.
        jpg_h = np.zeros((300,256,3))
        #Convert jpg image to gray scale.
        jpg_imgray = cv2.cvtColor(jpg_img,cv2.COLOR_BGR2GRAY)
        
        ##Color Histogram Section
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
        #Save color histograms
        cv2.imwrite("histograms/jpg/" + jpg_infile.replace("images/", "").replace(".ppm", ".jpg"), jpg_h)

        ##Black and White Texture Histogram
        #For drawing the histogram.
        jpg_h = np.zeros((300,256,3))
        #Calculates the Laplacian of an image. The function calculates the Laplacian of the source image by adding up the second x and y derivatives calculated using the Sobel operator.
        jpg_gray_lap = cv2.Laplacian(jpg_imgray,cv2.CV_16S,ksize=3,scale=1,delta=0)
        #Converts input array elements to another 8-bit unsigned integer with optional linear transformation.
        jpg_dst = cv2.convertScaleAbs(jpg_gray_lap)
        #Save paplacian jpg images.
        cv2.imwrite("laplacian/jpg/" + jpg_infile.replace("images/", "").replace(".ppm", ".jpg"), jpg_dst)
        #Create jpg binary mask, a 8-bit image, where white denotes that region should be used for histogram calculations, and black means it should not.
        jpg_ret, jpg_lap_thresh_mask = cv2.threshold(jpg_dst,127,255,0)
        #Save 8 bit mask images.
        cv2.imwrite("8bitmask/jpg/" + jpg_infile.replace("images/", "").replace(".ppm", ".jpg"), jpg_lap_thresh_mask)
        #Calculates a histogram for the 8-bit region marked in the mask using a set of arrays.
        jpg_texture_hist = cv2.calcHist([jpg_dst],[0],jpg_lap_thresh_mask,[256],[0,255])
        #Normalize the value to fall below 255 and fit in image height.
        cv2.normalize(jpg_texture_hist,jpg_texture_hist,0,255,cv2.NORM_MINMAX)
        #Evenly round to the given number of decimals. For values exactly halfway between rounded decimal values, Numpy rounds to the nearest even value.
        round_jpg_texture_hist = np.int32(np.around(jpg_texture_hist))
        for x,fliped_jpg_texture_hist in enumerate(round_jpg_texture_hist):
            cv2.line(jpg_h,(x,0),(x,fliped_jpg_texture_hist),(255,255,255))
        #Flip the image vertically.
        fliped_jpg_texture_hist = np.flipud(jpg_h)
        #Save one dimensional histogram
        cv2.imwrite("one_dimensional_histograms/jpg/" + jpg_infile.replace("images/", "").replace(".ppm", ".jpg"), fliped_jpg_texture_hist)


        #Compare the correlation of two color histograms.
        color_counter = cv2.compareHist(ppm_hist, jpg_hist, cv.CV_COMP_CORREL)
        #Initialization of the result interpretation.
        if high_color_correlation == "" and low_color_correlation == "":
            high_color_counter = color_counter
            low_color_counter = color_counter
            high_color_correlation = jpg_infile
            low_color_correlation = jpg_infile
        #Find the most similar jpg image.
        if color_counter >= high_color_counter:
            high_color_counter = color_counter
            high_color_correlation = jpg_infile
        #Find the most dissimilar jpg image.
        if color_counter <= low_color_counter:
            low_color_counter = color_counter
            low_color_correlation = jpg_infile

        #Compare the correlation of two texture histograms.
        texture_counter = cv2.compareHist(ppm_texture_hist, jpg_texture_hist, cv.CV_COMP_CORREL)
        #Initialization of the result interpretation.
        if high_texture_correlation == "" and low_texture_correlation == "":
            high_texture_counter = texture_counter
            low_texture_counter = texture_counter
            high_texture_correlation = jpg_infile
            low_texture_correlation = jpg_infile
        #Find the most similar jpg image.
        if texture_counter >= high_texture_counter:
            high_texture_counter = texture_counter
            high_texture_correlation = jpg_infile
        #Find the most dissimilar jpg image.
        if texture_counter <= low_texture_counter:
            low_texture_counter = texture_counter
            low_texture_correlation = jpg_infile

        if high_combined_correlation == "" and low_combined_correlation == "":
            high_counter = texture_counter*r + color_counter*(1-r)
            low_counter = texture_counter*r + color_counter*(1-r)
            high_correlation = jpg_infile
            low_correlation = jpg_infile
        if (texture_counter*r + color_counter*(1-r)) >= high_counter:
            high_counter = texture_counter*r + color_counter*(1-r)
            high_combined_correlation = jpg_infile
        if (texture_counter*r + color_counter*(1-r)) <= low_counter:
            low_counter = texture_counter*r + color_counter*(1-r)
            low_combined_correlation = jpg_infile


    #Print the result using colored text supported by the termcolor library of terminal.
    print colored("Reading PPM Image: " + ppm_infile, 'red')
    print colored("Color Histogram Matching", 'green')
    print colored("Most Similar JPG image: " + high_color_correlation + "     Correlation Value: " + str(high_color_counter), 'blue')
    print colored("Most Dissimilar JPG image: " + low_color_correlation + "  Correlation Value: " + str(low_color_counter), 'blue')
    print colored("Texture Histogram Matching", 'green')
    print colored("Most Similar JPG image: " + high_texture_correlation + "     Correlation Value: " + str(high_texture_counter), 'blue')
    print colored("Most Dissimilar JPG image: " + low_texture_correlation + "  Correlation Value: " + str(low_texture_counter), 'blue')
    print colored("Combined Matching", 'green')
    print colored("Most Similar JPG image: " + high_combined_correlation + "     Correlation Value: " + str(high_counter), 'blue')
    print colored("Most Dissimilar JPG image: " + low_combined_correlation + "  Correlation Value: " + str(low_counter), 'blue')
    print ""
    # img1 = cv2.imread(ppm_infile)
    # img2 = cv2.imread(high_color_correlation)
    # img3 = cv2.imread(low_color_correlation)

    # #Setup the result folders.
    # if not os.path.exists("color_matching_results/" + ppm_infile.replace("images/", "").replace(".ppm", "/")):
    #     os.makedirs("color_matching_results/" + ppm_infile.replace("images/", "").replace(".ppm", "/"))

    # #Write result images to targeted folders.
    # cv2.imwrite("color_matching_results/" + ppm_infile.replace("images/", "").replace(".ppm", "/") + ppm_infile.replace("images/", ""), img1)
    # cv2.imwrite("color_matching_results/" + ppm_infile.replace("images/", "").replace(".ppm", "/") + high_color_correlation.replace("images/", ""), img2)
    # cv2.imwrite("color_matching_results/" + ppm_infile.replace("images/", "").replace(".ppm", "/") + low_color_correlation.replace("images/", ""), img3)