
#Imagen de python ligera
FROM alpine

#Espacio  de trabajo
WORKDIR /server/

#Copiar los archivos del codigo de la fuente 
COPY . .
COPY requirements.txt .

ENV DEBIAN_FRONTEND=noninteractive

# Actualiza los repositorios de apt e instala Python y las herramientas necesarias
RUN apk add --no-cache python3-dev \
    && python3-pip \
    && pip3 install --upgrade pip 
    
#Instala las dependencias necesarias para correr el codigo
RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_ENV development
ENV FLASK_RUN_PORT 5000
ENV FLASK_RUN_HOST 0.0.0.0
