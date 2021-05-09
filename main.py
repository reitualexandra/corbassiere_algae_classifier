from PIL import Image
from numpy import asarray
import numpy
from operator import itemgetter
import image_utils
import data_utils
from image_utils import log



def minimum_distance_classification(source_dir, output="output.png"):
    IMAGES = image_utils.create_raster(source_dir)

    ICE = [data_utils.ICE[x] for x in IMAGES.keys()]
    SNOW = [data_utils.SNOW[x] for x in IMAGES.keys()]
    ALGAE_LOW = [data_utils.ALGAE_LOW[x] for x in IMAGES.keys()]
    ALGAE_HIGH = [data_utils.ALGAE_HIGH[x] for x in IMAGES.keys()]
    SOIL = [data_utils.SOIL[x] for x in IMAGES.keys()]
    GRASS = [data_utils.GRASS[x] for x in IMAGES.keys()]

    image_shape = numpy.shape(list(IMAGES.items())[0][1])
    log(image_shape)
    MAP_DATA = numpy.zeros(shape=image_shape + (3,))
    for i in range(0, image_shape[0]):
        for j in range(0, image_shape[1]):
            p = []
            for band in IMAGES.keys():
                image = IMAGES[band]
                p.append(image[i, j])

            p = numpy.array(p)
            d_ICE = numpy.linalg.norm(p - ICE)
            d_SNOW = numpy.linalg.norm(p - SNOW)
            d_ALGAE_LOW = numpy.linalg.norm(p - ALGAE_LOW)
            d_ALGAE_HIGH = numpy.linalg.norm(p - ALGAE_HIGH)
            d_SOIL = numpy.linalg.norm(p - SOIL)
            d_GRASS = numpy.linalg.norm(p - GRASS)
            distances = [d_ICE, d_SNOW, d_ALGAE_LOW, d_ALGAE_HIGH, d_SOIL, d_GRASS]

            classified_pixel_color = data_utils.COLORS[min(enumerate(distances), key=itemgetter(1))[0] + 1]
            MAP_DATA[i, j] = asarray(classified_pixel_color)

    img = Image.fromarray(MAP_DATA, 'RGB')
    img.save(output)
    img.show()


def main():
    minimum_distance_classification(source_dir="/Users/areitu/espace_bfea/Sentinel-2")

if __name__ == "__main__":
    main()