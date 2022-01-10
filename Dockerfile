FROM python:3.9

WORKDIR /app
COPY . /app

EXPOSE 80

RUN pip install --no-cache-dir --upgrade -r requirements.txt