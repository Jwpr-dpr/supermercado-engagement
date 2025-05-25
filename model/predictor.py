# model/predictor.py

import pandas as pd
import joblib
from datetime import timedelta
from typing import List


class FechaPredictor:
    def __init__(self, model_path: str = "model_fecha.pkl"):
        self.model = joblib.load(model_path)

    def predecir_proxima_fecha(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Predict next purchase date per client based on their last purchase.

        :param df: DataFrame with usuario and fecha_compra
        :return: DataFrame with usuario and fecha_estimada
        """
        df = df.copy()
        df["fecha_compra"] = pd.to_datetime(df["fecha_compra"])
        ultimas = df.groupby("usuario")["fecha_compra"].max().reset_index()

        ultimas["dia"] = ultimas["fecha_compra"].dt.dayofweek
        ultimas["mes"] = ultimas["fecha_compra"].dt.month

        X = ultimas[["dia", "mes"]]
        dias_estimados = self.model.predict(X)

        ultimas["dias_estimados"] = dias_estimados.round().astype(int)
        ultimas["fecha_estimada"] = ultimas["fecha_compra"] + ultimas["dias_estimados"].apply(lambda d: timedelta(days=d))

        return ultimas[["usuario", "fecha_estimada"]]


class ProductoPredictor:
    def __init__(self, productos_path: str = "top_productos.pkl"):
        self.top_productos = joblib.load(productos_path)  # DataFrame with usuario and top_productos

    def predecir_productos(self, clientes: pd.Series) -> pd.DataFrame:
        """
        Predict top-3 products for a list of client IDs.

        :param clientes: Series of usuario values
        :return: DataFrame with usuario and top_productos (list)
        """
        base = pd.DataFrame({"usuario": clientes})
        resultado = base.merge(self.top_productos, on="usuario", how="left")
        resultado["top_productos"] = resultado["top_productos"].apply(lambda x: x if isinstance(x, list) else [])
        return resultado
