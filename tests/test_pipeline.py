import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import tempfile
import os
from RegimeMap.pipeline import build_surface


def test_build_surface_visualization():
    """
    Тест функции build_surface с визуализацией исходных данных и результата
    """
    input_path = 'test.csv'

    # Создаем временный файл для выходных данных
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='_output.csv') as tmp_output:
        output_path = tmp_output.name

    try:
        # Читаем исходные данные для визуализации
        print(f"Чтение данных из {input_path}")
        original_df = pd.read_csv(input_path)
        print(f"Загружено {len(original_df)} точек данных")
        print("\nПервые 5 строк:")
        print(original_df.head())

        # Выполняем build_surface
        print("\nПостроение RBF поверхности...")
        f_axis, a_axis, surface = build_surface(
            input_csv=input_path,
            output_csv=output_path,
            resolution=(100, 100),
            median_size=5,
            clamp_zero=True,
            kernel="linear"
        )

        # Проверяем результаты
        print(f"\nРезультаты:")
        print(f"  Форма поверхности: {surface.shape}")
        print(f"  Fuel axis: [{f_axis.min():.2f}, {f_axis.max():.2f}], {len(f_axis)} точек")
        print(f"  Additive axis: [{a_axis.min():.2f}, {a_axis.max():.2f}], {len(a_axis)} точек")
        print(f"  Component range: [{surface.min():.2f}, {surface.max():.2f}]")

        assert surface.shape == (100, 100), f"Ожидалась форма (100, 100), получена {surface.shape}"
        assert len(f_axis) == 100, f"Ожидалось 100 точек по fuel, получено {len(f_axis)}"
        assert len(a_axis) == 100, f"Ожидалось 100 точек по additive, получено {len(a_axis)}"
        assert surface.min() >= 0, f"Найдены отрицательные значения: {surface.min()}"

        # Визуализация
        fig = plt.figure(figsize=(14, 6))

        # 1. Исходные данные как heatmap (грубая сетка)
        ax1 = fig.add_subplot(121)

        # Создаем грубую сетку для визуализации исходных данных
        n_bins = 15
        fuel_bins = np.linspace(original_df['fuel'].min(), original_df['fuel'].max(), n_bins)
        additive_bins = np.linspace(original_df['additive'].min(), original_df['additive'].max(), n_bins)

        original_df_copy = original_df.copy()
        original_df_copy['fuel_bin'] = pd.cut(original_df_copy['fuel'], fuel_bins, labels=False)
        original_df_copy['additive_bin'] = pd.cut(original_df_copy['additive'], additive_bins, labels=False)

        original_matrix = original_df_copy.pivot_table(
            values='component',
            index='additive_bin',
            columns='fuel_bin',
            aggfunc='mean'
        )

        sns.heatmap(
            original_matrix,
            cmap='viridis',
            ax=ax1,
            cbar_kws={'label': 'Component'},
            xticklabels=False,
            yticklabels=False,
            square=False
        )
        ax1.set_title(f'Исходные данные\n(binned heatmap {n_bins}x{n_bins})', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Fuel →', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Additive →', fontsize=12, fontweight='bold')

        # 2. RBF аппроксимированная поверхность
        ax2 = fig.add_subplot(122)
        im = ax2.imshow(
            surface,
            cmap='viridis',
            aspect='auto',
            origin='lower',
            extent=[f_axis.min(), f_axis.max(), a_axis.min(), a_axis.max()],
            interpolation='bilinear'
        )
        ax2.set_xlabel('Fuel', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Additive', fontsize=12, fontweight='bold')
        ax2.set_title(f'RBF поверхность\n({surface.shape[1]}x{surface.shape[0]} точек)',
                      fontsize=14, fontweight='bold')
        cbar2 = plt.colorbar(im, ax=ax2, label='Component')

        # Накладываем исходные точки на RBF поверхность
        ax2.scatter(
            original_df['fuel'],
            original_df['additive'],
            c='red',
            s=30,
            edgecolors='white',
            linewidth=0.5,
            alpha=0.6,
            label='Исходные точки'
        )
        ax2.legend(loc='upper right', fontsize=10)

        plt.tight_layout()
        plt.show()

        print("\n✓ Все тесты пройдены успешно!")

    finally:
        # Удаляем временный файл
        if os.path.exists(output_path):
            os.remove(output_path)


if __name__ == "__main__":
    test_build_surface_visualization()