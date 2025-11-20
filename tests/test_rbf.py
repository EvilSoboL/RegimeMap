import pandas as pd
from RegimeMap.rbf import rbf_approx

def test_rbf_shape():
    df = pd.DataFrame({
        "fuel": [0, 1, 0, 1],
        "additive": [0, 0, 1, 1],
        "component": [1, 2, 3, 4]
    })

    f, a, s = rbf_approx(df, resolution=(100, 100))
    print(s)
    assert s.shape == (100, 100)
