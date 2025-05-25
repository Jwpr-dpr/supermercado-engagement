# tests/test_extractor.py

from etl.extractor import S3Extractor

# Reemplazar con tus datos
BUCKET = "assessment-86fc5eb8"
KEY = "raw-data/data.csv"

extractor = S3Extractor(bucket_name=BUCKET, s3_key=KEY)
df = extractor.extract_csv()

print(df.head())