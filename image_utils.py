"""
This module contains a few functions for image pre-processing.
Here you will find a function for cropping/ masking images, as well as
functions used to create normalized images or translate the corner
coordinates for cropping.
"""

import os
import glob
from numpy import asarray
import numpy
import cv2
import inspect
import datetime
from osgeo import osr, ogr
from osgeo import gdal


BANDS = {
    "Landsat8": ["B1.", "B2.", "B3.", "B4.", "B5.", "B6.", "B7.", "B8.", "B9."],
    "Landsat7": ["B1.", "B2.", "B3.", "B4.", "B5.", "B7.", "B8."],
    "Sentinel": ["B01", "B02", "B03"]#, "B04", "B05", "B06", "B07", "B8A", "B09", "B10", "B11", "B12"]
}

def log(msg):
    now = datetime.datetime.now()
    caller = inspect.stack()[1].function
    print("[{}][{}:{}:{}]: {}".format(caller, now.hour, now.minute, now.second, msg))


def crop_images(img_source, img_destination, xmin, ymin, xmax, ymax, mission="sentinel2"):
    band_list = BANDS["Sentinel"]
    if mission=="landsat8":
        band_list = BANDS["Landsat8"]
    elif mission=="landsat7":
        band_list = BANDS["Landsat7"]
    if img_source is None:
        log("ERROR: No image source")
        return 1
    else:
        if img_destination is None:
            img_destination = os.path.dirname(os.path.realpath(__file__))
        os.makedirs(img_destination, exist_ok=True)
        os.makedirs(img_destination + "_cropped", exist_ok=True)

        for image in glob.glob(os.path.join(img_source, "*")):
            try:
                img_names = [x for x in band_list if x in image]
                img_name = max(img_names, key=len)
                img_name = int(''.join(c for c in img_name if c.isdigit()))
            except ValueError:
                img_name = None

            if img_name is not None:
                log("Converting image {}".format(image))
                options = "-projwin {} {} {} {} -of GTIFF ".format(xmin, ymin, xmax, ymax)
                output_cropped = os.path.join(img_destination + "_cropped", str(img_name) + ".TIF")
                cmd = "gdal_translate {} {} {}".format(options, image, output_cropped)
                os.system(cmd)

                xml_files = os.listdir(img_destination)
                for item in xml_files:
                    if item.endswith(".xml"):
                        os.remove(os.path.join(img_destination, item))

                output_masked = os.path.join(img_destination, str(img_name) + ".TIF")
                cmd = "gdalwarp {} {} -cutline mask.gpkg -crop_to_cutline".format(image, output_masked)
                os.system(cmd)

                xml_files = os.listdir(img_destination + "_cropped")
                for item in xml_files:
                    if item.endswith(".xml"):
                        os.remove(os.path.join(img_destination + "_cropped", item))

        return 0


def normalize_image(source_image, min_value=0, max_value=1, mission='sentinel2'):
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


#crop_images(img_source="/Users/areitu/Downloads/LC08_L2SP_007013_20170814_20200903_02_T1",
#            img_destination="/Users/areitu/espace_bfea/Landsat-8/Greenland",
#            xmin=500000, ymin=7499941, xmax=610000, ymax=7392608, mission="landsat8")
#crop_images(img_source="/Users/areitu/Downloads/S2A_MSIL2A_20170809T145921_N9999_R125_T22WEV_20210602T172205.SAFE/GRANULE/L2A_T22WEV_A011133_20170809T150205/IMG_DATA/R60m",
#            img_destination="/Users/areitu/espace_bfea/Sentinel-2/Greenland",
#            xmin=500000, ymin=7499941, xmax=614215, ymax=7392608, mission="sentinel2")
#crop_images(img_source="/Users/areitu/Downloads/LE07_L2SP_195028_20100707_20200911_02_T1",
#            img_destination="/Users/areitu/espace_bfea/Landsat-7/Corbassiere",
#            xmin=364090.59, ymin=5096444.81, xmax=370806.25, ymax=5089472.68, mission="landsat7")


#crop_images(img_source="C:\\Users\\Win10\\Downloads\\LC08_L2SP_195028_20200811_20200918_02_T1",
#            img_destination=".\\Landsat-8\\Corbassiere",
#            xmin=364090.59, ymin=5096444.81, xmax=370806.25, ymax=5089472.68, mission="landsat8")
#crop_images(img_source="C:\\Users\\Win10\\Downloads\\L1C_T32TLR_A026846_20200812T103752\\S2A_MSIL2A_20200812T103031_N9999_R108_T32TLR_20210620T195206.SAFE\\GRANULE\\L2A_T32TLR_A026846_20200812T103752\\IMG_DATA\\R20m",
#            img_destination=".\\Sentinel-2\\Corbassiere",
#            xmin=364090.59, ymin=5096444.81, xmax=370806.25, ymax=5089472.68, mission="sentinel2")