FROM python:3.10

WORKDIR /server

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["cd", "flaskr/"]
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]
