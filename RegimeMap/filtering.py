import numpy as np
from scipy.ndimage import median_filter

def apply_filters(surface, median_size=7, clamp_zero=True):
    if clamp_zero:
        surface = np.where(surface < 0, 0, surface)

    if median_size:
        surface = median_filter(surface, size=median_size)

    return surface
