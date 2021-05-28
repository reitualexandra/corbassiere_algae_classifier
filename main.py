from PIL import Image
import numpy
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import image_utils
import data_utils
import os
from image_utils import log


def minimum_distance_classification(source_dir, output="Classification.png", title="Glacier Classification"):
    data_utils.create_dataset(file=data_utils.HCRF_FILE, savefig=True)
    IMAGES = image_utils.create_raster(source_dir)
    bands = list(IMAGES.keys())
    bands.remove("coordinates")
    coordinates = IMAGES["coordinates"]

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
            d_CI = numpy.linalg.norm(p - numpy.array(CI))
            d_SN = numpy.linalg.norm(p - numpy.array(SN))
            d_LA = numpy.linalg.norm(p - numpy.array(LA))
            d_HA = numpy.linalg.norm(p - numpy.array(HA))
            d_WAT = numpy.linalg.norm(p - WAT)
            d_CC = numpy.linalg.norm(p - CC)
            distances = [d_CI, d_SN, d_LA, d_HA, d_WAT, d_CC]

            MAP_DATA[i, j] = data_utils.COLORS[distances.index(min(distances)) + 1]

    img = Image.fromarray(MAP_DATA, 'RGB')
    img.save(output)

    custom_lines = [Line2D([0], [0], color="lightskyblue", lw=4),
                    Line2D([0], [0], color="white", lw=4),
                    Line2D([0], [0], color="mediumseagreen", lw=4),
                    Line2D([0], [0], color="darkgreen", lw=4),
                    Line2D([0], [0], color="royalblue", lw=4),
                    Line2D([0], [0], color="black", lw=4)]

    fig, ax = plt.subplots()
    ax.legend(custom_lines, ['Ice', 'Snow', 'Low Algae', 'High Algae', 'Water', 'Cryoconite'])
    plt.imshow(img)
    plt.title(title)

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    # [(45.892286764906586, 6.982004862263944), (45.925461654837385, 6.9147668470067005)]

    Xcoord = numpy.linspace(coordinates[0][0], coordinates[1][0], img.size[0])
    Xcoord = numpy.around(Xcoord, 4)
    plt.xticks(range(0,img.size[0]), Xcoord)
    plt.locator_params(axis='x', nbins=6)

    Ycoord = numpy.linspace(coordinates[0][1], coordinates[1][1], img.size[1])
    Ycoord = numpy.around(Ycoord, 4)
    plt.yticks(range(0, img.size[1]), Ycoord)
    plt.locator_params(axis='y', nbins=6)

    plt.savefig(os.path.join(os.getcwd(), output))
    plt.show()


def main():
    #minimum_distance_classification(source_dir=os.path.join(os.getcwd(), "Sentinel-2", "Greenland"), output="Sentinel_Greenland.png")
    #minimum_distance_classification(source_dir=os.path.join(os.getcwd(), "Sentinel-2", "Aletsch"), output="Sentinel_Aletsch.png")
    #minimum_distance_classification(source_dir=os.path.join(os.getcwd(), "Sentinel-2", "Morteratsch"), output="Sentinel_Morteratsch.png")
    #minimum_distance_classification(source_dir=os.path.join(os.getcwd(), "Sentinel-2", "Fiescher"), output="Fiescher.png")
    #minimum_distance_classification(source_dir=os.path.join(os.getcwd(), "Sentinel-2", "Gorner"), output="Gorner.png")
    minimum_distance_classification(source_dir=os.path.join(os.getcwd(), "Sentinel-2", "MerDeGlace"), output="MerDeGlaceMe.png")


if __name__ == "__main__":
    main()