
#Imagen de python ligera
FROM ubuntu:20.04 AS builder

#Espacio  de trabajo
WORKDIR /server/

#Copiar los archivos del codigo de la fuente 
COPY . .
COPY requirements.txt .

ENV DEBIAN_FRONTEND=noninteractive

# Actualiza los repositorios de apt e instala Python y las herramientas necesarias
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
#Instala las dependencias necesarias para correr el codigo
RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_ENV development
ENV FLASK_RUN_PORT 5000
ENV FLASK_RUN_HOST 0.0.0.0




