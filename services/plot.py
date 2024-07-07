import matplotlib.pyplot as plt


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