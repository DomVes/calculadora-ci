FROM python:3.13.18-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY calculadora.py config.py ./
COPY servicios/calculadora/app.py ./app.py

ENV BITACORA_URL=http://bitacora:8080
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]
