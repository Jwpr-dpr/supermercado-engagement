# tests/test_predictor.py

import pandas as pd
import joblib
from model.predictor import FechaPredictor, ProductoPredictor


def test_fecha_predictor():
    # Entrena un modelo simple antes del test
    model = joblib.load("model_fecha.pkl")
    assert model is not None

    df = pd.DataFrame({
        "usuario": [1, 2],
        "fecha_compra": pd.to_datetime(["2024-01-20", "2024-02-10"])
    })

    predictor = FechaPredictor()
    resultado = predictor.predecir_proxima_fecha(df)

    assert "usuario" in resultado.columns
    assert "fecha_estimada" in resultado.columns
    assert len(resultado) == 2


def test_producto_predictor():
    productos = pd.DataFrame({
        "usuario": [1],
        "top_productos": [["pan", "leche", "huevos"]]
    })
    joblib.dump(productos, "top_productos.pkl")

    predictor = ProductoPredictor()
    resultado = predictor.predecir_productos(pd.Series([1, 2]))

    assert "usuario" in resultado.columns
    assert "top_productos" in resultado.columns
    assert isinstance(resultado["top_productos"].iloc[0], list)
