# kakao-weatherapp-dockerfile-backup

FROM python:3.10

WORKDIR /app

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./app /app

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "9090", "--reload"]