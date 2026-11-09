FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY calculadora.py config.py ./
COPY api ./api

ENV APP_ENV=desarrollo
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "-m", "api.app"]
