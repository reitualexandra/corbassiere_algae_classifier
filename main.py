"""
This module applies a minimum distance classification on the pre-processed and cropped images.
This should output a classified map of the Corbassiere glacier.
"""

from PIL import Image
import numpy
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import image_utils
import data_utils
import os


def minimum_distance_classification(source_dir, output="Classification.png", title="Glacier Classification", mission="sentinel2"):
    data_utils.create_dataset(file=data_utils.HCRF_FILE, savefig=True)
    IMAGES = image_utils.create_raster(source_dir)
    bands = list(IMAGES.keys())
    bands.remove("coordinates")
    coordinates = IMAGES["coordinates"]
    nr_pixels = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    if mission=="landsat8":
        CI = [data_utils.CI_L8[x] for x in bands]
        SN = [data_utils.SN_L8[x] for x in bands]
        LA = [data_utils.LA_L8[x] for x in bands]
        HA = [data_utils.HA_L8[x] for x in bands]
        WAT = [data_utils.WAT_L8[x] for x in bands]
        CC = [data_utils.CC_L8[x] for x in bands]
    elif mission=="landsat7":
        CI = [data_utils.CI_L7[x] for x in bands]
        SN = [data_utils.SN_L7[x] for x in bands]
        LA = [data_utils.LA_L7[x] for x in bands]
        HA = [data_utils.HA_L7[x] for x in bands]
        WAT = [data_utils.WAT_L7[x] for x in bands]
        CC = [data_utils.CC_L7[x] for x in bands]
    else:
        CI = [data_utils.CI[x] for x in bands]
        SN = [data_utils.SN[x] for x in bands]
        LA = [data_utils.LA[x] for x in bands]
        HA = [data_utils.HA[x] for x in bands]
        WAT = [data_utils.WAT[x] for x in bands]
        CC = [data_utils.CC[x] for x in bands]

    image_shape = numpy.shape(list(IMAGES.items())[0][1])
    MAP_DATA = numpy.zeros([image_shape[0], image_shape[1], 3], dtype=numpy.uint8)
    MAP_DATA.fill(255)
    for i in range(0, image_shape[0]):
        for j in range(0, image_shape[1]):
            p = []
            for band in bands:
                image = IMAGES[band]
                p.append(image[i, j])

            p = numpy.array(p)
            if p.ndim > 1:
                p = p[:, 1]
            if numpy.all(p==0):
                MAP_DATA[i, j] = data_utils.COLORS[7]
            else:
                d_CI = numpy.linalg.norm(p - numpy.array(CI))
                d_SN = numpy.linalg.norm(p - numpy.array(SN))
                d_LA = numpy.linalg.norm(p - numpy.array(LA))
                d_HA = numpy.linalg.norm(p - numpy.array(HA))
                d_WAT = numpy.linalg.norm(p - numpy.array(WAT))
                d_CC = numpy.linalg.norm(p - numpy.array(CC))
                distances = [d_CI, d_SN, d_LA, d_HA, d_WAT, d_CC]

                MAP_DATA[i, j] = data_utils.COLORS[distances.index(min(distances)) + 1]
                nr_pixels[distances.index(min(distances)) + 1] += 1

    img = Image.fromarray(MAP_DATA, 'RGB')
    img.save(output + ".png")

    custom_lines = [Line2D([0], [0], color="lightskyblue", lw=4),
                    Line2D([0], [0], color="white", lw=4),
                    Line2D([0], [0], color="mediumseagreen", lw=4),
                    Line2D([0], [0], color="darkgreen", lw=4),
                    Line2D([0], [0], color="royalblue", lw=4),
                    Line2D([0], [0], color="black", lw=4)]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.legend(custom_lines, ['Ice ({} pixels)'.format(nr_pixels[1]),
                             'Snow ({} pixels)'.format(nr_pixels[2]),
                             'Low Algae ({} pixels)'.format(nr_pixels[3]),
                             'High Algae ({} pixels)'.format(nr_pixels[4]),
                             'Water ({} pixels)'.format(nr_pixels[5]),
                             'Cryoconite ({} pixels)'.format(nr_pixels[6])], bbox_to_anchor=(2.3, 1), facecolor="lightgrey")
    plt.imshow(img)
    plt.title(title)

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    Xcoord = numpy.linspace(coordinates[0][0], coordinates[1][0], img.size[0])
    Xcoord = numpy.around(Xcoord, 2)
    plt.xticks(range(0, img.size[0]), Xcoord)
    plt.locator_params(axis='x', nbins=4)

    Ycoord = numpy.linspace(coordinates[0][1], coordinates[1][1], img.size[1])
    Ycoord = numpy.around(Ycoord, 2)
    plt.yticks(range(0, img.size[1]), Ycoord)
    plt.locator_params(axis='y', nbins=6)

    plt.savefig(os.path.join(os.getcwd(), output + "_figure.png"))
    plt.show()


def main():
    #minimum_distance_classification(source_dir=os.path.join(os.getcwd(), "Landsat-8", "Greenland"),
    #                                output="Greenland_Landsat", mission="landsat8")
    #minimum_distance_classification(source_dir=os.path.join(os.getcwd(), "Sentinel-2", "Corbassiere"),
    #                               output="Corbassiere_Sentinel2", mission="sentinel2")
    minimum_distance_classification(source_dir=os.path.join(os.getcwd(), "Landsat-7", "Corbassiere"),
                                    output="Corbassiere_Landsat7", mission="landsat7")


if __name__ == "__main__":
    main()