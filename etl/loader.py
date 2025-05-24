# etl/loader.py

from typing import Optional
import pandas as pd
import boto3
import logging
import io

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class S3Loader:
    def __init__(self, bucket_name: str, s3_output_path: str, aws_region: Optional[str] = "us-east-1"):
        """
        Clase encargada de guardar un DataFrame procesado en S3 en formato Parquet.

        :param bucket_name: Nombre del bucket S3
        :param s3_output_path: Ruta destino del archivo dentro del bucket (ej. processed-data/clientes_recurrentes.parquet)
        :param aws_region: Región de AWS
        """
        self.bucket_name = bucket_name
        self.s3_output_path = s3_output_path
        self.aws_region = aws_region
        self.s3 = boto3.client("s3", region_name=self.aws_region)

    def save_parquet(self, df: pd.DataFrame, compression: str = "snappy") -> None:
        """
        Guarda un DataFrame como archivo Parquet en S3.

        :param df: DataFrame a guardar
        :param compression: Tipo de compresión ("snappy", "gzip", etc.)
        """
        try:
            logger.info(f"Guardando archivo parquet en s3://{self.bucket_name}/{self.s3_output_path}")
            buffer = io.BytesIO()
            df.to_parquet(buffer, index=False, compression=compression)
            buffer.seek(0)
            self.s3.upload_fileobj(buffer, self.bucket_name, self.s3_output_path)
            logger.info("Archivo guardado exitosamente.")
        except Exception as e:
            logger.error(f"Error al guardar archivo en S3: {e}")
            raise
