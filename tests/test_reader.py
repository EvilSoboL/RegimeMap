import pandas as pd
from RegimeMap.reader import read_csv
import pytest
import tempfile


def test_reader_ok():
    df = pd.DataFrame({
        "fuel": [1,2],
        "additive": [3,4],
        "component": [5,6]
    })

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    df.to_csv(tmp.name, index=False)

    out = read_csv(tmp.name)
    assert len(out) == 2

def test_reader_missing_column():
    df = pd.DataFrame({"fuel": [1]})
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    df.to_csv(tmp.name, index=False)

    with pytest.raises(ValueError):
        read_csv(tmp.name)