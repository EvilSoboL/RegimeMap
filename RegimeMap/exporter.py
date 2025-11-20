import pandas as pd

def export_surface(path, f_axis, a_axis, surface):
    flat = []

    for i, a in enumerate(a_axis):
        for j, f in enumerate(f_axis):
            flat.append({
                "fuel": f,
                "additive": a,
                "component": float(surface[i, j])
            })

    pd.DataFrame(flat).to_csv(path, index=False)
