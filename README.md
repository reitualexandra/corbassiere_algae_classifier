# Corbassiere Algae Classifier

This repository is a (minimal) sample classifier software for glacier algae, applied on the Corbassiere glacier in the European Alps. The scripts are using training data from https://github.com/jmcook1186/IceSurfClassifiers . The scripts use the minimum distance classification algorithm, and are adapted to work with Sentinel-2, Landsat-7 and Landsat-8 imagery. 
The satellite imagery can be downloaded from https://earthexplorer.usgs.gov/ . Note that the Sentinel-2 imagery requires preprocessing with ESA's sen2cor commandline tool: https://step.esa.int/main/snap-supported-plugins/sen2cor/ . For Landsat imagery, level 2 imagery can be used without any preprocessing.
The scripts output a classified map containing 6 classes (snow, ice, algae: high + low, rocks). Below you can see computed results for the Corbassiere glacier, as well as a map of the western coast of Greenland:

![Corbassiere_Landsat7](https://user-images.githubusercontent.com/83270197/127006358-d7099711-63c8-4551-8711-deb95428aba6.png)
![Greenland_Landsat7](https://user-images.githubusercontent.com/83270197/127006384-99e2f18e-7465-4527-b1b3-67b5493454b6.png)


# Scripts

data_utils.py - contains functions that gather and process training data, define the bands for each mission and set the colors for each class
image_utils.py - contains functions that deal with masking and cropping the satellite images, normalize their values and create multidimensional image matrices for interpretation
main.py - contains the classification algorithm and main function


# How to use:

1. Download tiles containing the Corbassiere glacier. If you are using Sentinel-2 imagery, make sure to preprocess them.

2. From image_utils.py run the function "crop_images" to crop and mask the images you downloaded. The function will output two sets of images: one with the masked images and another one with cropped images in the shape of a rectangle; it should receive as arguments:
    - img_source is the path to the directory containing the images
    - img_destination is the path to the directory where you want the masked images to be stored
    - xmin, ymin, xmax, ymax are UTM32 coordinates for cropping
    - mission should be either "sentinel2", "landsat7" or "landsat8"
If no mask is available, the classification can then be done on the cropped images.

3. From main.py run the function "minimum_distance_classification". It should receive the arguments:
    - source_dir is the path to the directory containing all the cropped or masked images
    - output is the name you want to give the map
    - mission should be either "sentinel2", "landsat7" or "landsat8"
    - title should contain the title for the final figure 


# Python modules

gdal, PIL, numpy, matplotlib, os, pandas, glob, cv2, osgeo, inspect, datetime
