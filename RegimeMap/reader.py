import pandas as pd

REQUIRED_COLUMNS = ["fuel", "additive", "component"]

def read_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"CSV missing columns: {missing}")

    return df
