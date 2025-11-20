from RegimeMap.pipeline import build_surface


def main():
    """
    Точка входа библиотечного режима.
    Здесь можно менять входные данные, разрешение RBF-сетки и параметры фильтрации.
    """

    # === Настройки пользователя ===
    input_csv = "data/source/diesel_steam_O2.csv"          # путь к исходным данным
    output_csv = "data/result/approx_diesel_steam_O2.csv"   # куда сохранить аппроксимированную поверхность

    resolution = (100, 100)          # размер сетки (например 50x50, 200x200)
    median_size = 20                  # медианная фильтрация (None или 0 — отключить)
    clamp_zero = True                # удалять отрицательные значения
    kernel = "linear"                # ядро RBF: linear, multiquadric, cubic, gaussian …

    print("=== RegimeMap Surface Builder ===")
    print(f"Input CSV:   {input_csv}")
    print(f"Output CSV:  {output_csv}")
    print(f"Resolution:  {resolution}")
    print(f"Median:      {median_size}")
    print(f"Clamp zero:  {clamp_zero}")
    print(f"Kernel:      {kernel}")
    print("Processing...")

    # запуск конвейера
    fuel_axis, additive_axis, surface = build_surface(
        input_csv=input_csv,
        output_csv=output_csv,
        resolution=resolution,
        median_size=median_size,
        clamp_zero=clamp_zero,
        kernel=kernel
    )

    print("Done! Surface saved to:", output_csv)


if __name__ == "__main__":
    main()
