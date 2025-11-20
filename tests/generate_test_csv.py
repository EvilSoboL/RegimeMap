import numpy as np
import pandas as pd

# Генерация тестовых данных
np.random.seed(42)

n_points = 50

# Генерируем данные с некоторой закономерностью + шум
fuel = np.random.uniform(10, 90, n_points)
additive = np.random.uniform(5, 45, n_points)

# Создаем зависимость: component = f(fuel, additive) + noise
# Квадратичная зависимость с шумом для более интересной поверхности
component = (
    20 +
    0.8 * fuel +
    1.2 * additive +
    0.015 * fuel * additive -
    0.005 * fuel**2 -
    0.01 * additive**2 +
    np.random.normal(0, 8, n_points)
)

# Создаем DataFrame
df = pd.DataFrame({
    'fuel': fuel,
    'additive': additive,
    'component': component
})

# Сортируем для лучшей читаемости
df = df.sort_values(['additive', 'fuel']).reset_index(drop=True)

# Округляем значения для читаемости
df = df.round(2)

# Сохраняем в CSV
df.to_csv('test.csv', index=False)

print(f"Создан файл test.csv с {len(df)} записями")
print("\nПервые 5 строк:")
print(df.head())
print("\nСтатистика:")
print(df.describe())
