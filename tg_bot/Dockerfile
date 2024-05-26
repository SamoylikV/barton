FROM python:3.9-slim

WORKDIR /bot

COPY ../requirements.txt /bot/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /bot/

COPY .env /bot/.env

CMD ["python", "main.py"]