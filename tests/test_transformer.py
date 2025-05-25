# tests/test_transformer.py

from etl.extractor import S3Extractor
from etl.transformer import PurchaseTransformer

BUCKET = "assessment-86fc5eb8"
KEY = "raw-data/data.csv"

extractor = S3Extractor(bucket_name=BUCKET, s3_key=KEY)
df = extractor.extract_csv()

transformer = PurchaseTransformer(df)
df_clean = transformer.clean_columns()
df_recurrentes = transformer.get_recurrent_customers()

print(df_recurrentes.head())
