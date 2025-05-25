# scripts/generate_predictions.py

import pandas as pd
from model.predictor import FechaPredictor, ProductoPredictor
import boto3

# Cargar datos procesados desde S3 
df = pd.read_parquet("data/clientes_recurrentes.parquet")

# Generar predicciones
fecha_model = FechaPredictor()
producto_model = ProductoPredictor()

df_fecha = fecha_model.predecir_proxima_fecha(df)
df_prod = producto_model.predecir_productos(df_fecha["usuario"])

resultado = df_fecha.merge(df_prod, on="usuario")

# Guardar local
resultado.to_parquet("predicciones_clientes.parquet", index=False)

# (Opcional) subir a S3

s3 = boto3.client("s3")
with open("predicciones_clientes.parquet", "rb") as f:
    s3.upload_fileobj(f, "assessment-86fc5eb8", "predictions/predicciones_clientes.parquet")
