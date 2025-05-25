# model/training.py

import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
import numpy as np


def entrenar_modelo_fecha(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42) -> None:
    """
    Train a model to predict how many days until the next purchase per client,
    print training/test metrics, and save the model.

    :param df: DataFrame with columns usuario, fecha_compra
    :param test_size: Proportion of data used for test split
    :param random_state: Reproducibility seed
    """
    df = df.copy()
    df.sort_values(["usuario", "fecha_compra"], inplace=True)
    df["fecha_compra"] = pd.to_datetime(df["fecha_compra"])

    df["dias_entre"] = df.groupby("usuario")["fecha_compra"].diff().dt.days
    df = df.dropna()

    df["dia"] = df["fecha_compra"].dt.dayofweek
    df["mes"] = df["fecha_compra"].dt.month

    features = ["dia", "mes"]
    X = df[features]
    y = df["dias_entre"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    model = RandomForestRegressor(n_estimators=100, random_state=random_state)
    model.fit(X_train, y_train)

    def print_metrics(y_true, y_pred, label: str):
        mae = mean_absolute_error(y_true, y_pred)
        rmse = root_mean_squared_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        print(f"{label} metrics:")
        print(f"    MAE  = {mae:.2f}")
        print(f"    RMSE = {rmse:.2f}")
        print(f"    R²   = {r2:.3f}")

    print("Date Prediction Model Evaluation:")
    print_metrics(y_train, model.predict(X_train), "Train")
    print_metrics(y_test, model.predict(X_test), "Test")

    joblib.dump(model, "model_fecha.pkl")
    print("\nDate prediction model saved as model_fecha.pkl")


def generar_tabla_top_productos(df: pd.DataFrame) -> None:
    """
    Generate top-3 most frequently purchased products per client and save it.

    :param df: DataFrame with usuario and producto columns
    """
    df = df.copy()
    if "producto" not in df.columns:
        raise ValueError("Column 'producto' is required")

    product_counts = (
        df.groupby(["usuario", "producto"])
        .size()
        .reset_index(name="frecuencia")
    )

    product_counts["rank"] = product_counts.groupby("usuario")["frecuencia"].rank("first", ascending=False)
    top_3 = product_counts[product_counts["rank"] <= 3]

    top_3_final = (
        top_3.sort_values(["usuario", "rank"])
        .groupby("usuario")["producto"]
        .apply(list)
        .reset_index()
        .rename(columns={"producto": "top_productos"})
    )

    joblib.dump(top_3_final, "top_productos.pkl")
    print("Top-3 product table saved as top_productos.pkl")


def evaluar_recomendacion_productos(df: pd.DataFrame) -> None:
    """
    Evaluate product recommendation accuracy by testing whether the real product
    in a client's last purchase is in their top-3 product history.

    Prints Hit@3 (recall).
    """
    df = df.copy()
    if "producto" not in df.columns:
        raise ValueError("Column 'producto' is required")

    df["fecha_compra"] = pd.to_datetime(df["fecha_compra"])
    ultima = df.sort_values("fecha_compra").groupby("usuario").tail(1)
    previas = df[~df.index.isin(ultima.index)]

    top_previos = (
        previas.groupby(["usuario", "producto"])
        .size()
        .reset_index(name="frecuencia")
    )
    top_previos["rank"] = top_previos.groupby("usuario")["frecuencia"].rank("first", ascending=False)
    top_3 = top_previos[top_previos["rank"] <= 3]

    top_3_final = (
        top_3.sort_values(["usuario", "rank"])
        .groupby("usuario")["producto"]
        .apply(list)
        .reset_index()
        .rename(columns={"producto": "top_productos"})
    )

    merged = ultima[["usuario", "producto"]].merge(top_3_final, on="usuario", how="left")

    def hit(row):
        return int(isinstance(row["top_productos"], list) and row["producto"] in row["top_productos"])

    merged["hit"] = merged.apply(hit, axis=1)

    hit_rate = merged["hit"].mean()
    print(f"Product Recommender Evaluation:")
    print(f"    Hit@3 (recall): {hit_rate:.2%} ({merged['hit'].sum()} hits / {len(merged)} clients)")
