FROM python:3.12

WORKDIR /app

COPY ./app ./app
COPY ./models ./models
COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "/app/app/main.py"]
