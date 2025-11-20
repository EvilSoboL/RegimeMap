import numpy as np
import pandas as pd
import tempfile
import os
from RegimeMap.exporter import export_surface


def test_export_surface_basic():
    """Тест базовой функциональности экспорта"""
    f_axis = [1.0, 2.0, 3.0]
    a_axis = [0.5, 1.5]
    surface = np.array([[10, 20, 30],
                        [40, 50, 60]])

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
        tmp_path = tmp.name

    try:
        export_surface(tmp_path, f_axis, a_axis, surface)

        # Проверяем, что файл создан
        assert os.path.exists(tmp_path)

        # Читаем и проверяем содержимое
        df = pd.read_csv(tmp_path)

        # Проверяем количество строк (должно быть len(a_axis) * len(f_axis))
        assert len(df) == 6

        # Проверяем наличие всех колонок
        assert list(df.columns) == ["fuel", "additive", "component"]

        # Проверяем первую строку
        assert df.iloc[0]["fuel"] == 1.0
        assert df.iloc[0]["additive"] == 0.5
        assert df.iloc[0]["component"] == 10.0

        # Проверяем последнюю строку
        assert df.iloc[-1]["fuel"] == 3.0
        assert df.iloc[-1]["additive"] == 1.5
        assert df.iloc[-1]["component"] == 60.0
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_export_surface_values_order():
    """Тест правильности порядка значений"""
    f_axis = [10, 20]
    a_axis = [100, 200, 300]
    surface = np.array([[1, 2],
                        [3, 4],
                        [5, 6]])

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
        tmp_path = tmp.name

    try:
        export_surface(tmp_path, f_axis, a_axis, surface)
        df = pd.read_csv(tmp_path)

        # Проверяем порядок: для каждого additive все fuel values
        expected = [
            (10, 100, 1), (20, 100, 2),
            (10, 200, 3), (20, 200, 4),
            (10, 300, 5), (20, 300, 6)
        ]

        for i, (f, a, c) in enumerate(expected):
            assert df.iloc[i]["fuel"] == f
            assert df.iloc[i]["additive"] == a
            assert df.iloc[i]["component"] == c
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_export_surface_single_element():
    """Тест с массивом из одного элемента"""
    f_axis = [5.0]
    a_axis = [2.0]
    surface = np.array([[99.5]])

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
        tmp_path = tmp.name

    try:
        export_surface(tmp_path, f_axis, a_axis, surface)
        df = pd.read_csv(tmp_path)

        assert len(df) == 1
        assert df.iloc[0]["fuel"] == 5.0
        assert df.iloc[0]["additive"] == 2.0
        assert df.iloc[0]["component"] == 99.5
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_export_surface_negative_values():
    """Тест с отрицательными значениями"""
    f_axis = [-1.0, 0.0, 1.0]
    a_axis = [-5.0, 5.0]
    surface = np.array([[-10, -20, -30],
                        [10, 20, 30]])

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
        tmp_path = tmp.name

    try:
        export_surface(tmp_path, f_axis, a_axis, surface)
        df = pd.read_csv(tmp_path)

        assert len(df) == 6
        assert df["component"].min() == -30.0
        assert df["component"].max() == 30.0
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_export_surface_float_conversion():
    """Тест конвертации в float"""
    f_axis = [1, 2]
    a_axis = [3, 4]
    surface = np.array([[10, 20],
                        [30, 40]], dtype=np.int32)

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
        tmp_path = tmp.name

    try:
        export_surface(tmp_path, f_axis, a_axis, surface)
        df = pd.read_csv(tmp_path)

        # Проверяем, что значения component являются float
        assert df["component"].dtype == np.float64
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
