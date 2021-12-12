FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app
ADD ./requirements.txt /
RUN pip install -r /requirements.txt
COPY ./src/ /app/
RUN mkdir -p /static/
WORKDIR /app