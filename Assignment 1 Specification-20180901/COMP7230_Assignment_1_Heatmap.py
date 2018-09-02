"""
COMP7230 2018 Assignment 1

Once you have completed questions 1, 2, 3 and 7, running this file
will produce the heatmap.

You do not need to modify the contents of this file.
"""

import scipy.ndimage as ndimage
import matplotlib
from COMP7230_Assignment_1_Submission import *


def main():

    # Get the data set
    data_set = read_data_set("Cyclones.csv")

    # Parse it into the required format
    for index, record in enumerate(data_set):
        data_set[index] = parse_record(record)

    # produce the data for the heat map
    heatmap = generate_heat_map(data_set)

    # read the map
    map_image = ndimage.imread("Australia_Map.jpg")
    greymap = matplotlib.colors.rgb_to_hsv(map_image)[:, :, 2]

    # rescale the heatmap
    zoom = (np.shape(greymap)[0] / np.shape(heatmap)[0], np.shape(greymap)[1] / np.shape(heatmap)[1])
    heatmap = ndimage.interpolation.zoom(heatmap, zoom)
    heatmap -= np.amin(heatmap)
    heatmap /= np.amax(heatmap)

    print(np.amax(heatmap), np.amin(heatmap))

    # merge the heat map with the map of Australia and show
    red = np.uint8(greymap / 2 + 127 * heatmap)
    blue = np.uint8(greymap / 2)
    green = np.uint8(greymap / 2 + 127 - 127 * heatmap)

    rgb = np.dstack((red, green, blue))

    plt.clf()
    plt.imshow(rgb)
    plt.show()


if __name__ == "__main__":
    main()