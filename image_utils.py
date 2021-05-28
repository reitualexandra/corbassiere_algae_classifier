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
    "Landsat": ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12"],
    "Sentinel": ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B8A", "B09", "B10", "B11", "B12"]
}

def log(msg):
    now = datetime.datetime.now()
    caller = inspect.stack()[1].function
    print("[{}][{}:{}:{}]: {}".format(caller, now.hour, now.minute, now.second, msg))


def crop_images(img_source, img_destination, xmin, ymin, xmax, ymax):
    coordinates = []
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
                img_names = [x for x in BANDS['Sentinel'] + BANDS["Landsat"] if x in image]
                img_name = max(img_names, key=len)
                img_name = int(''.join(c for c in img_name if c.isdigit()))
            except ValueError:
                img_name = None

            if img_name is not None:
                log("Converting image {}".format(image))
                bbox = (xmin, ymin, xmax, ymax)
                gdal.Translate(os.path.join(img_destination, str(img_name) + "." + img_extension), image, projWin=bbox)

        return 0


def normalize_image(source_image, min_value=0, max_value=1):
    img = Image.open("{}".format(source_image))
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


"""
# USAGE EXAMPLE: 

crop_images(img_source="/Users/areitu/Desktop/S2A_MSIL2A_20200720T102031_N0214_R065_T32TMS_20200720T131523.SAFE/GRANULE/L2A_T32TMS_A026517_20200720T102636/IMG_DATA/R20m",
            img_destination="/Users/areitu/espace_bfea/Sentinel-2", upper_left_x=900, upper_left_y=2100, width=700, length=1000)

crop_images(img_source="/Users/areitu/Downloads/S2B_MSIL2A_20210429T161829_N0300_R040_T21XWC_20210429T210017.SAFE/GRANULE/L2A_T21XWC_A021659_20210429T161824/IMG_DATA/R20m/",
            img_destination="/Users/areitu/espace_bfea/Sentinel-2", upper_left_x=0, upper_left_y=0, width=5490, length=5490)
create_raster(source_dir="/Users/areitu/espace_bfea/Sentinel-2/")
"""

#crop_images(img_source="/Users/areitu/Downloads/S2B_MSIL2A_20200718T102559_N9999_R108_T32TLR_20210517T190440.SAFE/GRANULE/L2A_T32TLR_A017580_20200718T103605/IMG_DATA/R20m/",
#            img_destination="/Users/areitu/espace_bfea/Sentinel-2/MerDeGlace", xmin=338327.25, ymin=5087868.95, xmax=343451.29, ymax=5084045.51)
