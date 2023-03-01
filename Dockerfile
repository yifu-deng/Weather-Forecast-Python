FROM alpine:latest
RUN apk update && apk add bash


FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY repeat.sh /app

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["uvicorn", "app", "--host", "0.0.0.0", "--port", "8080"]

