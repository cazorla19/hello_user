FROM python:3.7.4-alpine3.10

WORKDIR /app

ENV APP_VERSION=0.1.0

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

ENTRYPOINT ["python", "hello_user/api.py"]
