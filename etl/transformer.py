# etl/transformer.py

from typing import Optional
import pandas as pd
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class PurchaseTransformer:
    def __init__(self, df: pd.DataFrame):
        """
        Clase encargada de transformar los datos crudos y filtrar clientes recurrentes.

        :param df: DataFrame crudo extraído
        """
        self.df = df.copy()

    def clean_columns(self) -> pd.DataFrame:
        """
        Asegura que las columnas tengan los nombres y formatos esperados.
        """
        df = self.df

        # Normaliza nombres de columnas
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        # Asegura tipos de datos
        df["fecha_compra"] = pd.to_datetime(df["fecha_compra"])
        df["cantidad_productos"] = pd.to_numeric(df["cantidad_productos"], errors="coerce").fillna(0).astype(int)

        self.df = df
        return df

    def get_recurrent_customers(self) -> pd.DataFrame:
        """
        Filtra los clientes que hacen más de una compra cada 30 días,
        y cada compra tiene más de 10 productos.
        """
        df = self.df

        # Filtra compras válidas (>10 productos)
        df = df[df["cantidad_productos"] > 10]

        # Agrupa por cliente y mes
        df["mes"] = df["fecha_compra"].dt.to_period("M")

        compras_mensuales = df.groupby(["cliente_id", "mes"]).size().reset_index(name="compras_mes")

        # Identifica clientes con más de una compra por mes (es decir, recurrentes)
        recurrentes = compras_mensuales[compras_mensuales["compras_mes"] > 1]["cliente_id"].unique()

        df_recurrentes = df[df["cliente_id"].isin(recurrentes)]

        logger.info(f"Clientes recurrentes encontrados: {len(recurrentes)}")
        return df_recurrentes
