# tests/test_loader.py

import pandas as pd
from unittest.mock import patch
from etl.loader import S3Loader


@patch("etl.loader.boto3.client")
def test_save_parquet(mock_boto_client):
    """
    Testea que save_parquet llama correctamente a S3 sin realizar la operación real.
    """
    mock_s3 = mock_boto_client.return_value
    mock_s3.upload_fileobj.return_value = None  # Simula éxito

    df = pd.DataFrame({
        "usuario": [1, 2],
        "fecha_compra": pd.to_datetime(["2024-01-01", "2024-01-10"]),
        "cantidad_productos": [11, 12]
    })

    loader = S3Loader(bucket_name="fake-bucket", s3_output_path="fake-path/output.parquet")
    loader.save_parquet(df)

    # Asegura que upload_fileobj fue llamado una vez
    assert mock_s3.upload_fileobj.called
