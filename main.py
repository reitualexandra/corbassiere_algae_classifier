from PIL import Image
import numpy
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import image_utils
import data_utils
from image_utils import log



def minimum_distance_classification(source_dir, output="output.png", title="Classification of Aletsch glacier - 2020"):
    IMAGES = image_utils.create_raster(source_dir)

    ICE = [data_utils.ICE[x] for x in IMAGES.keys()]
    SNOW = [data_utils.SNOW[x] for x in IMAGES.keys()]
    ALGAE_LOW = [data_utils.ALGAE_LOW[x] for x in IMAGES.keys()]
    ALGAE_HIGH = [data_utils.ALGAE_HIGH[x] for x in IMAGES.keys()]

    SOIL = [data_utils.SOIL[x] for x in IMAGES.keys()]
    GRASS = [data_utils.GRASS[x] for x in IMAGES.keys()]

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
            d_ICE = numpy.linalg.norm(p - numpy.array(ICE))
            d_SNOW = numpy.linalg.norm(p - numpy.array(SNOW))
            d_ALGAE_LOW = numpy.linalg.norm(p - numpy.array(ALGAE_LOW))
            d_ALGAE_HIGH = numpy.linalg.norm(p - numpy.array(ALGAE_HIGH))
            d_SOIL = numpy.linalg.norm(p - SOIL)
            d_GRASS = numpy.linalg.norm(p - GRASS)
            distances = [d_ICE, d_SNOW, d_ALGAE_LOW, d_ALGAE_HIGH, d_SOIL, d_GRASS]

            MAP_DATA[i, j] = data_utils.COLORS[distances.index(min(distances)) + 1]

    img = Image.fromarray(MAP_DATA, 'RGB')
    img.save(output)

    custom_lines = [Line2D([0], [0], color="skyblue", lw=4),
                    Line2D([0], [0], color="white", lw=4),
                    Line2D([0], [0], color="lightgreen", lw=4),
                    Line2D([0], [0], color="green", lw=4),
                    Line2D([0], [0], color="darkgreen", lw=4),
                    Line2D([0], [0], color="saddlebrown", lw=4)]

    fig, ax = plt.subplots()
    ax.legend(custom_lines, ['Ice', 'Snow', 'Low Algae', 'High Algae', 'Grass', 'Soil'])
    plt.imshow(img)
    plt.title(title)
    plt.savefig(output)
    plt.show()


def main():
    minimum_distance_classification(source_dir="/Users/areitu/espace_bfea/Sentinel-2", output="Sentinel_2020.png")

if __name__ == "__main__":
    main()