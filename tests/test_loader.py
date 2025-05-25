# tests/test_loader.py

from etl.extractor import S3Extractor
from etl.transformer import PurchaseTransformer
from etl.loader import S3Loader

BUCKET_IN = "assessment-86fc5eb8"
KEY = "raw-data/data.csv"

# REEMPLAZAR con tu ruta de escritura real
BUCKET_OUT = "assessment-86fc5eb8"
OUTPUT_PATH = "processed-data/clientes_recurrentes.parquet"

extractor = S3Extractor(bucket_name=BUCKET_IN, s3_key=KEY)
df = extractor.extract_csv()

transformer = PurchaseTransformer(df)
df_clean = transformer.clean_columns()
df_recurrentes = transformer.get_recurrent_customers()

loader = S3Loader(bucket_name=BUCKET_OUT, s3_output_path=OUTPUT_PATH)
loader.save_parquet(df_recurrentes)
