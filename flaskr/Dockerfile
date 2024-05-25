FROM python:3.10

WORKDIR /flaskr

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000


ENV FLASK_ENV development
ENV FLASK_RUN_PORT 5000
ENV FLASK_RUN_HOST 0.0.0.0
ENV REDIS_URL=redis://localhost:6379

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]
