
#  Predicción de Clientes Recurrentes y Productos – Supermercado

##  Descripción

Este proyecto implementa una solución completa de análisis y predicción de comportamiento de clientes en un supermercado, cumpliendo con los siguientes objetivos:

-  **ETL (Extract – Transform – Load)** desde un archivo `.csv` almacenado en AWS S3.
-  **Modelo de predicción de fechas**: estimar cuándo un cliente volverá a comprar.
-  **Recomendación de productos**: predecir los 3 productos más probables que comprará.
-  **Despliegue en Lambda** usando **Docker**, simulando entorno sin servidor.
-  **Validación de resultados** y generación de archivos `.parquet`.

---


---

## Criterios de Recurrencia

Un cliente se considera **recurrente** si:
- Tiene más de **una compra por mes**.
- En cada compra adquirió **más de 10 productos**.

---

## Flujo de trabajo

### 1.  ETL

El archivo `etl/` contiene módulos para:

| Módulo        | Función                                                                 |
|---------------|-------------------------------------------------------------------------|
| `extractor.py`| Conecta con S3 y extrae `data.csv`                                      |
| `transformer.py` | Limpia datos, convierte fechas, detecta clientes recurrentes        |
| `loader.py`   | Guarda un `.parquet` limpio en S3                                       |

Ejecutado automáticamente desde `lambda/app.py`.

---

### 2.  Entrenamiento de Modelos

Archivo: `model/training.py`

- `entrenar_modelo_fecha()`: predice días hasta la próxima compra (con `RandomForest` o `XGBoost`).
- `generar_tabla_top_productos()`: calcula los 3 productos más frecuentes por cliente.
- `evaluar_recomendacion_productos()`: evalúa precisión con Hit@3.

---

### 3. Predicción

Archivo: `model/predictor.py`

- `FechaPredictor`: estima fecha futura por cliente.
- `ProductoPredictor`: entrega top-3 productos por cliente.

---

### 4. Generación de Entregable

Script: `scripts/generate_predictions.py`

Genera y guarda:

predicciones_clientes.parquet

Con columnas:

| cliente_id | fecha_estimada | top_productos         |
|------------|----------------|------------------------|
| 12345      | 2025-06-01     | ['Pan', 'Leche', 'Huevos'] |

---

##  Métricas de Evaluación

###  Fecha de próxima compra

| Métrica | Train | Test |
|---------|-------|------|
| MAE     | 1.29  | 1.30 |
| RMSE    | 3.92  | 3.95 |
| R²      | 0.006 | 0.006 |

###  Recomendación de productos

- Hit@3 (recall): 56.46% (1097 hits / 1943 clients)

---

## ☁️ Lambda con Docker

El archivo `lambda/app.py` implementa el handler compatible con AWS Lambda.

La imagen Docker incluye todo el proyecto y se ejecuta como Lambda local:

```dockerfile
FROM public.ecr.aws/lambda/python:3.11

COPY etl/ /var/task/etl/
COPY lambda/app.py /var/task/
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["app.handler"]
```
## Ejecución local

docker build -t lambda-etl -f docker/Dockerfile .
docker run -p 9000:8080 -e AWS_ACCESS_KEY_ID=... -e AWS_SECRET_ACCESS_KEY=... lambda-etl

# En otra terminal
curl -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" -d "{}"

ests
Ubicados en tests/. Incluyen validaciones para:

Entrenamiento y guardado de modelos.

Predicción de fechas y productos.

Guardado correcto de .parquet.

Uso de mock para evitar dependencias con S3 real.

pytest tests/

## Archivos generados

| Archivo                         | Descripción                                 |
| ------------------------------- | ------------------------------------------- |
| `clientes_recurrentes.parquet`  | Clientes filtrados y transformados desde S3 |
| `model_fecha.pkl`               | Modelo entrenado para predicción de fechas  |
| `top_productos.pkl`             | Tabla con top-3 productos por cliente       |
| `predicciones_clientes.parquet` | Entregable final con fecha + productos      |

## Estado del Proyecto

| Componente                       | Estado |
| -------------------------------- | ------ |
| ETL desde S3 → S3 (`.parquet`)   | ✅      |
| Lambda Docker invocable local    | ✅      |
| Modelos de predicción entrenados | ✅      |
| Evaluación de métricas           | ✅      |
| Generación de entregable final   | ✅      |
| Tests automatizados              | ✅      |
