FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev

WORKDIR /app

COPY ../requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

COPY .env /app/.env

RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]