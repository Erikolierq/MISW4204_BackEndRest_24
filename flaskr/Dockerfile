FROM python:3.10

WORKDIR /flaskr

COPY requirements.txt .
COPY entrypoint.sh /flaskr/entrypoint.sh
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000


ENV FLASK_ENV development
ENV FLASK_RUN_PORT 5000
ENV FLASK_RUN_HOST 0.0.0.0
ENV URL_REDIS server-redis

ENV DB_USER admin
ENV DB_PASSWORD v1d304pp
ENV DB_NAME dbvideoapp
ENV DB_CONNECTION_NAME 34.123.41.208

# Establecer el script de entrada
ENTRYPOINT ["/flaskr/entrypoint.sh"]