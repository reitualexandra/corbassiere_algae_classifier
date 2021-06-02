"""
This file contains python functions that crop an image to the wanted dimensions.
Modules needed to run these functions:
    Commandline module:
    - imagemagik - download from https://imagemagick.org/script/download.php
    Python modules:
    - numpy - pip3 install numpy
    - PIL - pip3 install numpy

You should also have the needed images downloaded locally.
"""

import os
import glob
from PIL import Image
from numpy import asarray
import cv2
import inspect
import datetime
from osgeo import osr, ogr
from osgeo import gdal


BANDS = {
    "Landsat": ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9"],
    "Sentinel": ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B8A", "B09", "B10", "B11", "B12"]
}

def log(msg):
    now = datetime.datetime.now()
    caller = inspect.stack()[1].function
    print("[{}][{}:{}:{}]: {}".format(caller, now.hour, now.minute, now.second, msg))


def crop_images(img_source, img_destination, xmin, ymin, xmax, ymax, mission="sentinel2"):
    band_list = BANDS["Sentinel"]
    if mission=="landsat8":
        band_list = BANDS["Landsat"]
    if img_source is None:
        log("ERROR: No image source")
        return 1
    else:
        if img_destination is None:
            img_destination = os.path.dirname(os.path.realpath(__file__))
        os.makedirs(img_destination, exist_ok=True)

        for image in glob.glob(os.path.join(img_source, "*")):
            img_extension = image.split(".")[-1]
            try:
                img_names = [x for x in band_list if x in image]
                img_name = max(img_names, key=len)
                img_name = int(''.join(c for c in img_name if c.isdigit()))
            except ValueError:
                img_name = None

            if img_name is not None:
                log("Converting image {}".format(image))
                options = "-projwin {} {} {} {} -of JP2OpenJPEG".format(xmin, ymin, xmax, ymax)
                output = os.path.join(img_destination, str(img_name) + ".jp2")
                cmd = "gdal_translate {} {} {}".format(options, image, output)
                os.system(cmd)
                os.system("rm -f {}/*.xml".format(img_destination))

        return 0


def normalize_image(source_image, min_value=0, max_value=1):
    img = cv2.imread("{}".format(source_image))
    numpy_img = asarray(img)
    numpy_img_normalized = cv2.normalize(numpy_img, None, min_value, max_value, cv2.NORM_MINMAX, dtype=cv2.CV_64F)
    return numpy_img_normalized


def create_raster(source_dir):
    IMAGES = {}
    image_paths = glob.glob(os.path.join(source_dir, "*"))
    image_extension = image_paths[0].split(".")[-1]

    image_names = [os.path.split(x)[-1].replace(image_extension, "") for x in image_paths]
    image_names = [int(x.replace(".", "")) for x in image_names]
    image_names.sort()

    for image_name in image_names:
        band = image_name
        image_path = os.path.join(source_dir, "{}.{}".format(image_name, image_extension))
        image_data = normalize_image(image_path)
        IMAGES[band] = image_data
        IMAGES["coordinates"] = img_corners(img=image_path)

    return IMAGES

def utm32_latlon(pointX, pointY):
    inputEPSG = 32632
    outputEPSG = 4326
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(pointX, pointY)
    inSpatialRef = osr.SpatialReference()
    inSpatialRef.ImportFromEPSG(inputEPSG)
    outSpatialRef = osr.SpatialReference()
    outSpatialRef.ImportFromEPSG(outputEPSG)
    coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)
    point.Transform(coordTransform)

    return (point.GetX(), point.GetY())


def img_corners(img):
    src = gdal.Open(img, gdal.GA_ReadOnly)
    ulx, xres, xskew, uly, yskew, yres = src.GetGeoTransform()
    lrx = ulx + (src.RasterXSize * xres)
    lry = uly + (src.RasterYSize * yres)

    return [utm32_latlon(lrx, lry), utm32_latlon(ulx, uly)]


#crop_images(img_source="/Users/areitu/Downloads/S2B_MSIL2A_20200718T102559_N9999_R108_T32TLR_20210517T190440.SAFE/GRANULE/L2A_T32TLR_A017580_20200718T103605/IMG_DATA/R20m/",
#            img_destination="/Users/areitu/espace_bfea/Sentinel-2/MerDeGlace", xmin=338327.25, ymin=5087868.95, xmax=343451.29, ymax=5084045.51)

#crop_images(img_source="/Users/areitu/Downloads/S2A_MSIL2A_20200707T101031_N9999_R022_T33TUN_20210529T112354.SAFE/GRANULE/L2A_T33TUN_A026331_20200707T101405/IMG_DATA/R20m",
#            img_destination="/Users/areitu/espace_bfea/Sentinel-2/Pasterze", xmin=324766.37, ymin=5218555.44, xmax=329318.48, ymax=5215457.10)

#crop_images(img_source="/Users/areitu/Downloads/S2B_MSIL2A_20200718T102559_N9999_R108_T32TMS_20210529T115725.SAFE/GRANULE/L2A_T32TMS_A017580_20200718T103605/IMG_DATA/R20m",
#            img_destination="/Users/areitu/espace_bfea/Sentinel-2/Rhone", xmin=452190.56, ymin=5165781.54, xmax=455495.53, ymax=5161342.15)

#crop_images(img_source="/Users/areitu/Downloads/LC08_L2SP_007013_20200705_20200913_02_T1/",
#            img_destination="/Users/areitu/espace_bfea/Landsat8/Greenland", xmin=500000, ymin=7499941, xmax=614215, ymax=7392608)
