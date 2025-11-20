import os
from RegimeMap.pipeline import build_surface


def main():
    """
    Точка входа библиотечного режима.
    Теперь: входная папка → выходная папка.
    Для каждого CSV в папке создается файл:
        approx_<исходное_имя>.csv
    """

    # === Настройки пользователя ===
    input_dir = "data/source/"      # папка с входными CSV
    output_dir = "data/result/"     # папка для сохранения результатов

    resolution = (100, 100)
    median_size = 20
    clamp_zero = True
    kernel = "linear"

    print("=== RegimeMap Surface Builder (Batch Mode) ===")
    print(f"Input folder:   {input_dir}")
    print(f"Output folder:  {output_dir}")
    print("Processing...\n")

    # Создаём выходную папку, если её нет
    os.makedirs(output_dir, exist_ok=True)

    # Перебираем все CSV в папке
    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(".csv"):
            continue

        input_csv = os.path.join(input_dir, filename)
        output_csv = os.path.join(output_dir, "approx_" + filename)

        print(f"→ Processing file: {filename}")

        try:
            fuel_axis, additive_axis, surface = build_surface(
                input_csv=input_csv,
                output_csv=output_csv,
                resolution=resolution,
                median_size=median_size,
                clamp_zero=clamp_zero,
                kernel=kernel,
            )
            print(f"   Saved: {output_csv}")
        except Exception as e:
            print(f"   ERROR processing {filename}: {e}")

    print("\nDone! All surfaces saved to:", output_dir)


if __name__ == "__main__":
    main()
