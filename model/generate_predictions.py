# model/generate_predictions.py

import pandas as pd
from predictor import FechaPredictor, ProductoPredictor
import joblib

def generar_predicciones():
    # Leer el dataset limpio (ya generado por la Lambda)
    df = pd.read_parquet("\\Users\\Dell\\OneDrive\\Escritorio\\Python\\supermercado-engagement\\data\\clientes_recurrentes.parquet")

    # Instanciar los modelos ya entrenados
    fecha_model = FechaPredictor("\\Users\\Dell\\OneDrive\\Escritorio\\Python\\supermercado-engagement\\model_fecha_csv.pkl")
    producto_model = ProductoPredictor("\\Users\\Dell\\OneDrive\\Escritorio\\Python\\supermercado-engagement\\top_productos_parquet.pkl")

    # Predecir fechas por cliente
    df_fechas = fecha_model.predecir_proxima_fecha(df)

    # Predecir productos por cliente
    df_productos = producto_model.predecir_productos(df_fechas["usuario"])

    # Unir resultados
    resultado = df_fechas.merge(df_productos, on="usuario")

    # Guardar como .parquet
    resultado.to_parquet("predicciones_clientes_ensemble.parquet", index=False)
    print("Archivo predicciones_clientes.parquet generado correctamente.")

if __name__ == "__main__":
    generar_predicciones()
