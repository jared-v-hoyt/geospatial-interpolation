import argparse
import numpy as np
import os
from interpolation.methods import inverse_distance_weighting, shape_function
from services.plot import plot_data


def main():
    parser = argparse.ArgumentParser(
        description="A Python-based interpolation application that utilizes real-world point-cloud data and spatial interpolation techniques to create a smooth heightmap of a given area.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("method", type=str, choices=["inverse_distance_weighting", "shape_function"], help="The interpolation method used.")
    parser.add_argument("points", type=str, help="The relative path to the CSV file containing the 3-dimensional point data.")
    parser.add_argument("-p", "--power", type=int, required=False, default=2, help="The power parameter used in the Inverse Distance Weighting equation.")
    parser.add_argument("-r", "--resolution", type=int, required=False, default=50, help="The number of subdivisions along each axis.")
    parser.add_argument("-s", "--save", action="store_true", help="Save the data as a CSV file to the same directory where the 3-dimensional point data is stored.")

    args = parser.parse_args()

    points = np.genfromtxt(args.points, delimiter=",")

    match args.method:
        case "inverse_distance_weighting":
            interpolated_data = inverse_distance_weighting(points, args.resolution, args.power)
        case "shape_function":
            interpolated_data = shape_function(points, args.resolution)

    combined_array = np.vstack((interpolated_data, interpolated_data))

    if args.save:
        np.savetxt(
            os.path.dirname(args.points) + "/interpolated_data.csv",
            np.unique(interpolated_data, axis=0),
            delimiter=",",
            fmt="%f"
        )

    plot_data(combined_array, "Inverse Distance Weighting")


if __name__ == "__main__":
    main()