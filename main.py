import numpy as np
import matplotlib.pyplot as plt
from services.error import calculate_error
from services.interpolation import inverse_distance_weighting, shape_function


def plot_data(data, title):
    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]

    plt.figure()
    plt.scatter(x, y, c=z, cmap="viridis")
    plt.colorbar(label="Interpolated Value")
    plt.title(title)
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.show()


def main():
    data = np.genfromtxt("./data/data.csv", delimiter=",")

    # Inverse Distance Weighting
    interpolated_data = inverse_distance_weighting(data)
    combined_array = np.vstack((interpolated_data, data))
    np.savetxt(
        "./data/interpolation/inverse_distance_weighting.csv",
        np.unique(interpolated_data, axis=0),
        delimiter=",",
        fmt="%f"
    )
    plot_data(combined_array, "Inverse Distance Weighting")

    mae, rmse, mse = calculate_error("./data/error/inverse_distance_weighting/actual_vs_calculated_rows.csv")
    print(f"Inverse Distance Weighting MAE:  {mae:.4f}")
    print(f"Inverse Distance Weighting RMSE: {rmse:.4f}")
    print(f"Inverse Distance Weighting MSE:  {mse:.4f}")

    # Shape Function Interpolation
    interpolated_data = shape_function(data)
    combined_array = np.vstack((interpolated_data, data))
    np.savetxt(
        "./data/interpolation/shape_function.csv",
        np.unique(interpolated_data, axis=0),
        delimiter=",",
        fmt="%f"
    )
    plot_data(combined_array, "Shape Function Interpolation")

    mae, rmse, mse = calculate_error("./data/error/shape_function/actual_vs_calculated_rows.csv")
    print(f"Shape Function MAE:  {mae:.4f}")
    print(f"Shape Function RMSE: {rmse:.4f}")
    print(f"Shape Function MSE:  {mse:.4f}")


if __name__ == "__main__":
    main()