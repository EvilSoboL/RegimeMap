import numpy as np
from scipy.interpolate import RBFInterpolator

def rbf_approx(df, resolution=(100, 100), kernel="linear"):
    """
    df: contains 'fuel', 'additive', 'component'
    resolution: (Nx, Ny) grid size
    """

    fuel = df["fuel"].to_numpy().reshape(-1, 1)
    additive = df["additive"].to_numpy().reshape(-1, 1)
    component = df["component"].to_numpy()

    points = np.hstack([fuel, additive])

    rbf = RBFInterpolator(points, component, kernel=kernel)

    # Generate uniform grid
    f_min, f_max = df["fuel"].min(), df["fuel"].max()
    a_min, a_max = df["additive"].min(), df["additive"].max()

    f_axis = np.linspace(f_min, f_max, resolution[0])
    a_axis = np.linspace(a_min, a_max, resolution[1])

    f_grid, a_grid = np.meshgrid(f_axis, a_axis)

    grid_points = np.stack([f_grid.ravel(), a_grid.ravel()], axis=1)
    surface = rbf(grid_points).reshape(f_grid.shape)

    return f_axis, a_axis, surface
