# lambda/app.py

import logging
from etl.extractor import S3Extractor
from etl.transformer import PurchaseTransformer
from etl.loader import S3Loader

# Configura logging global
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Parámetros S3
BUCKET_NAME = "assessment-86fc5eb8"
INPUT_KEY = "raw-data/data.csv"
OUTPUT_KEY = "/cleaned-data/JWP966/*"  

def handler(event=None, context=None):
    """
    Función principal de la Lambda. Extrae, transforma y guarda los datos de clientes recurrentes.
    """
    try:
        logger.info("Iniciando proceso ETL...")

        # Extraer
        extractor = S3Extractor(bucket_name=BUCKET_NAME, s3_key=INPUT_KEY)
        df = extractor.extract_csv()

        # Transformar
        transformer = PurchaseTransformer(df)
        df_clean = transformer.clean_columns()
        df_recurrentes = transformer.get_recurrent_customers()

        # Cargar
        loader = S3Loader(bucket_name=BUCKET_NAME, s3_output_path=OUTPUT_KEY)
        loader.save_parquet(df_recurrentes)

        logger.info("Proceso ETL finalizado con éxito.")

    except Exception as e:
        logger.error(f"Error general en el proceso ETL: {e}")
        raise

if __name__ == "__main__":
    handler()
