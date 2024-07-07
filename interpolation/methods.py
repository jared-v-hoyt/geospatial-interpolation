import numpy as np
from scipy.spatial import Delaunay
from tqdm import tqdm


def inverse_distance_weighting(points: np.ndarray, resolution: int, power: int):
    x_min, x_max = points[:, 0].min(), points[:, 0].max()
    y_min, y_max = points[:, 1].min(), points[:, 1].max()

    x_grid, y_grid = np.meshgrid(
        np.linspace(x_min, x_max, resolution), 
        np.linspace(y_min, y_max, resolution)
    )

    z_grid = np.zeros_like(x_grid)

    for i in tqdm(
        range(x_grid.shape[0]),
        desc="Inverse Distance Weighting",
        total=x_grid.shape[0]
    ):
        for j in range(x_grid.shape[1]):
            xi, yi = x_grid[i, j], y_grid[i, j]

            distances = np.sqrt(
                abs((points[:, 0] - xi)) ** power +
                abs((points[:, 1] - yi)) ** power
            )

            distances[distances == 0] = 0.0001 # Avoid division by zero in case of exact matches

            weights = 1 / (distances ** power)
            weighted_sum = np.sum(weights * points[:, 2])
            sum_of_weights = np.sum(weights)

            z_grid[i, j] = weighted_sum / sum_of_weights

    return np.column_stack((x_grid.flatten(), y_grid.flatten(), z_grid.flatten()))


def shape_function(points: np.ndarray, resolution: int):
    delaunay_triangulation = Delaunay(points[:, :2])

    x_min, x_max = points[:, 0].min(), points[:, 0].max()
    y_min, y_max = points[:, 1].min(), points[:, 1].max()

    x_grid, y_grid = np.meshgrid(
        np.linspace(x_min, x_max, resolution), 
        np.linspace(y_min, y_max, resolution)
    )

    z_grid = np.zeros_like(x_grid)

    for i in tqdm(
        range(x_grid.shape[0]),
        desc="Shape Function Interpolation",
        total=x_grid.shape[0]
    ):

        for j in range(x_grid.shape[1]):
            xi, yi = x_grid[i, j], y_grid[i, j]
            
            simplex = delaunay_triangulation.find_simplex(np.array([xi, yi]))

            # Checks if the point (xi, yi) exists within the convex hull
            if simplex == -1:
                continue
            
            p1, p2, p3 = delaunay_triangulation.simplices[simplex]
            p1, p2, p3 = points[p1], points[p2], points[p3]
            
            x1, y1, z1 = p1
            x2, y2, z2 = p2
            x3, y3, z3 = p3

            determinant = np.linalg.det([
                np.concatenate((np.array([1]), p1[:2])),
                np.concatenate((np.array([1]), p2[:2])),
                np.concatenate((np.array([1]), p3[:2]))
            ])

            N1 = (xi * (y2 - y3) - yi * (x2 - x3) + (x2 * y3 - x3 * y2)) / determinant
            N2 = (xi * (y3 - y1) - yi * (x3 - x1) + (x3 * y1 - x1 * y3)) / determinant
            N3 = (xi * (y1 - y2) - yi * (x1 - x2) + (x1 * y2 - x2 * y1)) / determinant

            z_grid[i, j] = N1 * z1 + N2 * z2 + N3 * z3

    x_flat = x_grid.flatten()
    y_flat = y_grid.flatten()
    z_flat = z_grid.flatten()

    # Will exclude all vertices that fall outside of the convex hull
    mask = z_flat != 0

    return np.column_stack((x_flat[mask], y_flat[mask], z_flat[mask]))