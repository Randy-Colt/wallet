FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install gunicorn==20.1.0

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY ./wallet_app .

EXPOSE 8000

CMD python manage.py migrate && gunicorn --bind 0.0.0.0:8000 wallet_app.wsgi