# etl/extractor.py

from typing import Optional
import boto3
import pandas as pd
from io import StringIO
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class S3Extractor:
    def __init__(self, bucket_name: str, s3_key: str, aws_region: Optional[str] = "us-east-1"):
        """
        Clase encargada de extraer datos desde un bucket S3.

        :param bucket_name: Nombre del bucket
        :param s3_key: Ruta dentro del bucket (ej. /raw-data/data.csv)
        :param aws_region: Región de AWS
        """
        self.bucket_name = bucket_name
        self.s3_key = s3_key
        self.aws_region = aws_region
        self.s3 = boto3.client("s3", region_name=self.aws_region)

    def extract_csv(self) -> pd.DataFrame:
        """
        Extrae el archivo CSV desde S3 y lo convierte a un DataFrame de pandas.

        :return: DataFrame con los datos leídos
        """
        try:
            logger.info(f"Descargando archivo desde s3://{self.bucket_name}/{self.s3_key}")
            obj = self.s3.get_object(Bucket=self.bucket_name, Key=self.s3_key)
            csv_bytes = obj["Body"].read().decode("utf-8")
            df = pd.read_csv(StringIO(csv_bytes))
            logger.info(f"Datos cargados exitosamente. {df.shape[0]} filas, {df.shape[1]} columnas.")
            return df
        except Exception as e:
            logger.error(f"Error al extraer datos desde S3: {e}")
            raise
