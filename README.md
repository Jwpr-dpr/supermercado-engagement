# Sistema ETL para Clientes Recurrentes – Okuo Assessment

Este proyecto es una solución técnica al reto de Okuo Analytics, orientado a identificar **clientes recurrentes**, predecir **cuándo volverán a comprar** y **qué productos comprarán**, con el objetivo de ofrecerles descuentos personalizados.

---

## Objetivo del sistema

Como gerente del supermercado, quiero:
- Saber **qué clientes compran recurrentemente**.
- Saber **cuándo volverán a comprar**.
- Saber **qué productos comprarán ese día**, para ofrecer descuentos.

---

## Criterio de recurrencia

Un **cliente recurrente** es aquel que:
- Ha realizado **más de una compra cada 30 días**.
- Y **cada compra contiene más de 10 productos**.

---

## Estructura del proyecto

okuo/
│
├── README.md                   # Descripción del proyecto, cómo correrlo, decisiones tomadas
├── docker/                     # Dockerfile y assets necesarios para la imagen
│   └── Dockerfile
├── lambda/                     # Código de la lambda con ETL
│   ├── app.py
│   ├── requirements.txt
│   └── __init__.py
├── etl/                        # Lógica para extracción, transformación y carga
│   ├── extractor.py
│   ├── transformer.py
│   ├── loader.py
│   └── __init__.py
├── model/                      # Modelos de predicción
│   ├── predictor.py
│   ├── training.py
│   └── __init__.py
├── data/                       # Esquema local para pruebas (simulación de s3)
│   └── data.csv
├── notebooks/                  # Exploración y validación de hipótesis
│   └── exploratory_analysis.ipynb
├── tests/                      # Pruebas unitarias
│   ├── test_extractor.py
│   ├── test_transformer.py
│   ├── test_predictor.py
│   └── __init__.py
├── .gitignore
├── pyproject.toml             # Ruff, mypy, black, etc.
└── mypy.ini                   # Configuración estática de tipos

## Tecnologías usadas

* Python 3.11
* pandas, boto3, pyarrow
* Docker + AWS Lambda
* S3 (lectura y escritura)
* GitHub + Gitflow + Conventional Commits
* Tipado con mypy, formateo con ruff, uv, docstrings

