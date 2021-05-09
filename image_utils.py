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


BANDS = {
    "Landsat": ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12"],
    "Sentinel": ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B8A", "B09", "B10", "B11", "B12"]
}

def log(msg):
    now = datetime.datetime.now()
    caller = inspect.stack()[1].function
    print("[{}][{}:{}:{}]: {}".format(caller, now.hour, now.minute, now.second, msg))


def crop_images(img_source, img_destination, upper_left_x, upper_left_y, width, length):
    if img_source is None:
        log("ERROR: No image source")
        return 1
    elif upper_left_x is None or upper_left_y is None:
        log("ERROR: No upper left corner given")
        return 1
    elif width is None or length is None:
        log("ERROR: Image dimensions not given")
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
                cmd = "convert {} -crop {}x{}+{}+{} {}.{}".format(image, width, length,
                                                                 upper_left_x, upper_left_y,
                                                                 os.path.join(img_destination, str(img_name)), img_extension)
                os.system(cmd)
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
    return IMAGES

"""
# USAGE EXAMPLE: 

crop_images(img_source="/Users/areitu/Desktop/S2A_MSIL2A_20200720T102031_N0214_R065_T32TMS_20200720T131523.SAFE/GRANULE/L2A_T32TMS_A026517_20200720T102636/IMG_DATA/R20m",
            img_destination="/Users/areitu/espace_bfea/Sentinel-2", upper_left_x=900, upper_left_y=2100, width=700, length=1000)

create_raster(source_dir="/Users/areitu/espace_bfea/Sentinel-2/")
"""