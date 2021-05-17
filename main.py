from PIL import Image
import numpy
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import image_utils
import data_utils
import os
from image_utils import log


def minimum_distance_classification(source_dir, output="Classification.png", title="Glacier Classification"):
    data_utils.create_dataset(file=data_utils.HCRF_FILE)
    IMAGES = image_utils.create_raster(source_dir)

    CI = [data_utils.CI[x] for x in IMAGES.keys()]
    SN = [data_utils.SN[x] for x in IMAGES.keys()]
    LA = [data_utils.LA[x] for x in IMAGES.keys()]
    HA = [data_utils.HA[x] for x in IMAGES.keys()]
    WAT = [data_utils.WAT[x] for x in IMAGES.keys()]
    CC = [data_utils.CC[x] for x in IMAGES.keys()]

    image_shape = numpy.shape(list(IMAGES.items())[0][1])
    MAP_DATA = numpy.zeros([image_shape[0], image_shape[1], 3], dtype=numpy.uint8)
    MAP_DATA.fill(255)
    for i in range(0, image_shape[0]):
        for j in range(0, image_shape[1]):
            p = []
            for band in IMAGES.keys():
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
    plt.savefig(os.path.join(os.getcwd(), output))
    plt.show()


def main():
    minimum_distance_classification(source_dir=os.path.join(os.getcwd(), "Sentinel-2"), output="Sentinel.png")



if __name__ == "__main__":
    main()