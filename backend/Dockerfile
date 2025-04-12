FROM python:3.9-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .

#python manage.py collectstatic --noinput
#cp -r /app/collected_static/. /backend_static/static/

#CMD ["sh", "-c", "python manage.py migrate && python manage.py load_db && gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000"]
CMD ["sh", "-c", "python manage.py migrate && gunicorn foodgram_backend.wsgi:application --bind 0.0.0.0:8000"]
