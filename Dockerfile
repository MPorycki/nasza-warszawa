FROM python:3.7

RUN apt-get update && apt-get install -y netcat vim

RUN pip install --upgrade pip setuptools

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY . /app
WORKDIR /app


RUN ["chmod" ,"+x", "start.sh"]
ENTRYPOINT ["/app/start.sh"]

