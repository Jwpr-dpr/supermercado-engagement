# docker/Dockerfile

FROM public.ecr.aws/lambda/python:3.11

# Copiar archivos del proyecto
COPY etl/ /var/task/etl/
COPY lambda/app.py /var/task/app.py

# Instalar dependencias
COPY requirements.txt .
RUN pip install -r requirements.txt

# Lambda handler
CMD ["app.handler"]
