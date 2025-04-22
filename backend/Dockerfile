# backend/Dockerfile
FROM python:3.9-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .

CMD ["sh", "-c", "python manage.py migrate && \
                    python load_data.py && \
                    python manage.py collectstatic --noinput && \
                    cp -r /app/collected_static/. /backend_static/static/ && \
                    gunicorn foodgram_backend.wsgi:application --bind 0.0.0.0:8000"]
