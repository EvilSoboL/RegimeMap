from .reader import read_csv
from .rbf import rbf_approx
from .filtering import apply_filters
from .exporter import export_surface

def build_surface(
    input_csv,
    output_csv,
    resolution=(100, 100),
    median_size=20,
    clamp_zero=True,
    kernel="linear"
):
    df = read_csv(input_csv)
    f_axis, a_axis, surface = rbf_approx(df, resolution, kernel)
    surface = apply_filters(surface, median_size, clamp_zero)
    export_surface(output_csv, f_axis, a_axis, surface)

    return f_axis, a_axis, surface
