import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from RegimeMap.rbf import rbf_approx


def test_rbf_shape():
    df = pd.DataFrame({
        "fuel": [0, 1, 0, 1],
        "additive": [0, 0, 1, 1],
        "component": [1, 2, 3, 4]
    })

    # Создаем исходную матрицу для визуализации
    original_matrix = df.pivot_table(
        values='component',
        index='additive',
        columns='fuel',
        aggfunc='mean'
    )

    # Получаем аппроксимированную матрицу
    f, a, s = rbf_approx(df, resolution=(20, 30))

    # Проверяем форму
    assert s.shape == (30, 20)

    # Визуализация
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Исходная матрица
    sns.heatmap(original_matrix, annot=True, fmt='.2f', cmap='viridis',
                ax=axes[0], cbar_kws={'label': 'Component'})
    axes[0].set_title('Исходная матрица')
    axes[0].set_xlabel('Fuel')
    axes[0].set_ylabel('Additive')

    # Аппроксимированная матрица
    sns.heatmap(s, cmap='viridis', ax=axes[1],
                cbar_kws={'label': 'Component'})
    axes[1].set_title(f'Аппроксимированная матрица RBF ({s.shape[0]}x{s.shape[1]})')
    axes[1].set_xlabel('Fuel (интерполированный)')
    axes[1].set_ylabel('Additive (интерполированный)')

    plt.tight_layout()
    plt.show()


# Запуск теста
test_rbf_shape()
