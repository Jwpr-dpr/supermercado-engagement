# tests/test_training.py

import pandas as pd
import os
from model import training


def test_entrenar_modelo_fecha(tmp_path):
    df = pd.DataFrame({
        "usuario": [1, 1, 1, 2, 2],
        "fecha_compra": pd.to_datetime([
            "2024-01-01", "2024-01-10", "2024-01-20", 
            "2024-01-03", "2024-01-30"
        ])
    })

    training.entrenar_modelo_fecha(df)
    assert os.path.exists("model_fecha.pkl"), "El modelo de fecha no se guardó correctamente."


def test_generar_top_productos(tmp_path):
    df = pd.DataFrame({
        "usuario": [1, 1, 1, 2, 2, 2, 2],
        "producto": ["pan", "leche", "pan", "huevos", "pan", "arroz", "pan"]
    })

    training.generar_tabla_top_productos(df)
    assert os.path.exists("top_productos.pkl"), "El archivo de productos no se guardó correctamente."


def test_evaluar_recomendacion_productos(capsys):
    df = pd.DataFrame({
        "usuario": [1, 1, 1, 1],
        "fecha_compra": pd.to_datetime([
            "2024-01-01", "2024-01-05", "2024-01-10", "2024-01-15"
        ]),
        "producto": ["pan", "leche", "pan", "leche"]
    })

    training.evaluar_recomendacion_productos(df)
    captured = capsys.readouterr()
    assert "Hit@3" in captured.out
