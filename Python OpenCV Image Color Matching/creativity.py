import os
import glob
import cv2
import cv
import numpy as np
from termcolor import colored
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
import Image


r = 0.2
color_distance_list = []
texture_distance_list = []
combined_distance_list = []
address_list = []
for ppm_infile in glob.glob( os.path.join("images", '*.ppm') ):
    #Loads each ppm images from the image folder.
    ppm_img = cv2.imread(ppm_infile)
    #Convert ppm image to gray scale.
    ppm_imgray = cv2.cvtColor(ppm_img,cv2.COLOR_BGR2GRAY)
    
    ##Color Histogram Section
    #Create ppm binary mask, a 8-bit image, where white denotes that region should be used for histogram calculations, and black means it should not.
    ppm_ret, ppm_thresh_mask = cv2.threshold(ppm_imgray,127,255,0)
    #Number of bins, since the histogram has 256 colors, it needs 256 bins. Bin is a multidimensional array.
    ppm_bins = np.arange(256).reshape(256,1)
    color = [ (255,0,0),(0,255,0),(0,0,255) ]
    #Iterate an enumerate tuple containing a count and the values obtained from iterating over the list color.
    for ch, col in enumerate(color):
        #Calculates a histogram for the 8-bit region marked in the mask using a set of arrays.
        ppm_hist = cv2.calcHist([ppm_img],[ch],ppm_thresh_mask,[256],[0,256])
        #Normalize the value to fall below 255 and fit in image height.
        cv2.normalize(ppm_hist,ppm_hist,0,255,cv2.NORM_MINMAX)

    ##Black and White Texture Histogram Section
    #Calculates the Laplacian of an image. The function calculates the Laplacian of the source image by adding up the second x and y derivatives calculated using the Sobel operator.
    ppm_gray_lap = cv2.Laplacian(ppm_imgray,cv2.CV_16S,ksize=3,scale=1,delta=0)
    #Converts input array elements to another 8-bit unsigned integer with optional linear transformation.
    ppm_dst = cv2.convertScaleAbs(ppm_gray_lap)
    #Create ppm binary mask, a 8-bit image, where white denotes that region should be used for histogram calculations, and black means it should not.
    ppm_ret, ppm_lap_thresh_mask = cv2.threshold(ppm_dst,127,255,0)
    #Calculates a histogram for the 8-bit region marked in the mask using a set of arrays.
    ppm_texture_hist = cv2.calcHist([ppm_dst],[0],ppm_lap_thresh_mask,[256],[0,255])
    #Normalize the value to fall below 255 and fit in image height.
    cv2.normalize(ppm_texture_hist,ppm_texture_hist,0,255,cv2.NORM_MINMAX)
    #Evenly round to the given number of decimals. For values exactly halfway between rounded decimal values, Numpy rounds to the nearest even value.

    sub_color_distance_list = []
    sub_texture_distance_list = []
    sub_address_list = []
    sub_combined_list = []
    for jpg_infile in glob.glob( os.path.join("images", '*.ppm') ):
        #Loads each jpg images from the image folder.
        jpg_img = cv2.imread(jpg_infile)
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

        ##Black and White Texture Histogram
        #Calculates the Laplacian of an image. The function calculates the Laplacian of the source image by adding up the second x and y derivatives calculated using the Sobel operator.
        jpg_gray_lap = cv2.Laplacian(jpg_imgray,cv2.CV_16S,ksize=3,scale=1,delta=0)
        #Converts input array elements to another 8-bit unsigned integer with optional linear transformation.
        jpg_dst = cv2.convertScaleAbs(jpg_gray_lap)
        #Create jpg binary mask, a 8-bit image, where white denotes that region should be used for histogram calculations, and black means it should not.
        jpg_ret, jpg_lap_thresh_mask = cv2.threshold(jpg_dst,127,255,0)
        #Calculates a histogram for the 8-bit region marked in the mask using a set of arrays.
        jpg_texture_hist = cv2.calcHist([jpg_dst],[0],jpg_lap_thresh_mask,[256],[0,255])
        #Normalize the value to fall below 255 and fit in image height.
        cv2.normalize(jpg_texture_hist,jpg_texture_hist,0,255,cv2.NORM_MINMAX)

        #Compare the correlation of two color histograms.
        color_counter = cv2.compareHist(ppm_hist, jpg_hist, cv.CV_COMP_CORREL)
        #Compare the correlation of two texture histograms.
        texture_counter = cv2.compareHist(ppm_texture_hist, jpg_texture_hist, cv.CV_COMP_CORREL)

        sub_color_distance_list.append(color_counter)
        sub_texture_distance_list.append(texture_counter)
        sub_address_list.append(jpg_infile)
        sub_combined_list.append(color_counter*(1-r) + texture_counter*r)
    color_distance_list.append(sub_color_distance_list)
    texture_distance_list.append(sub_texture_distance_list)
    address_list.append(sub_address_list)
    combined_distance_list.append(sub_combined_list)

# im = Image.open(address_list[5][0])
# plt.figimage(im, 0, 0)

# counter = 0
# for item in address_list[5]:
#     im = Image.open(item)
#     plt.figimage(im, 400*color_distance_list[5][counter], 300*texture_distance_list[5][counter])
#     counter = counter + 1

# plt.show()


im = Image.open("images/i06.ppm")
plt.figimage(im, 0, 0)

counter = 0
for item in address_list[05]:
    im = Image.open(item)
    plt.figimage(im, 600*(1-color_distance_list[05][counter]), 1800*(1-texture_distance_list[05][counter]))
    counter = counter + 1

plt.show()





