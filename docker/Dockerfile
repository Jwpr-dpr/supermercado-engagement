# docker/Dockerfile

FROM public.ecr.aws/lambda/python:3.11

# Copiamos módulos y dependencias
COPY etl/ /var/task/etl/
COPY lambda/app.py /var/task/app.py
COPY requirements.txt /var/task/

# Instalamos las dependencias
RUN pip install -r /var/task/requirements.txt

# Indicamos el entrypoint
CMD ["app.handler"]
