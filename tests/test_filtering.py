import numpy as np
from RegimeMap.filtering import apply_filters

def test_remove_negative():
    s = np.array([[1, -5], [-1, 3]])
    s2 = apply_filters(s, median_size=None, clamp_zero=True)
    print(s2)
    assert s2.min() >= 0

def test_remove_negative_2():
    s = np.array([[1, -5, 7], [-1, 3, 6]])
    s2 = apply_filters(s, median_size=None, clamp_zero=True)
    print(s2)
    assert s2.min() >= 0
