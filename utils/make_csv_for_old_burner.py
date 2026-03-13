import pandas as pd
import os

def split_components(input_csv: str, fuel_name="diesel", additive="steam"):
    df = pd.read_csv(input_csv)

    # соответствие для столбцов
    component_list = ["O2", "CO", "NO"]

    # На выходе будут файлы в той же папке
    base_dir = os.path.dirname(input_csv)

    for comp in component_list:
        if comp not in df.columns:
            print(f"❗ Компонента {comp} нет в файле, пропускаю")
            continue

        # Формируем новый DataFrame
        new_df = pd.DataFrame({
            "fuel": df["F_fuel"],
            "additive": df["F_steam"],
            "component": df[comp]
        })

        # Формируем имя файла
        output_name = f"approx_{fuel_name}_{additive}_{comp}.csv"
        output_path = os.path.join(base_dir, output_name)

        # Сохраняем
        new_df.to_csv(output_path, index=False)

        print(f"✔ Создан файл: {output_path}")

if __name__ == "__main__":
    split_components("C:/Users/evils/PycharmProjects/RegimeMap/data/old_burner_source/diesel_steam.csv")
