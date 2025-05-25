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

supermercado-engagement/  
├── README.md                   
├── docker/                     
│----|── Dockerfile  
├── lambda/                     
│----├── app.py  
│----├── requirements.txt  
│----|── init.py  
├── etl/                        
│----├── extractor.py  
│----├── transformer.py  
│----├── loader.py  
│----|── init.py  
├── model/                      
│----├── predictor.py  
│----├── training.py  
│----|── init.py  
├── data/                       
│----|── data.csv  
├── notebooks/                  
│----|── exploratory_analysis.ipynb  
├── tests/                      
│----├── test_extractor.py  
│----├── test_transformer.py  
│----├── test_predictor.py  
│----|── init.py  
├── .gitignore  
├── pyproject.toml               
└── mypy.ini                   

## Tecnologías usadas

* Python 3.11
* pandas, boto3, pyarrow
* Docker + AWS Lambda
* S3 (lectura y escritura)
* GitHub + Gitflow + Conventional Commits
* Tipado con mypy, formateo con ruff, uv, docstrings

