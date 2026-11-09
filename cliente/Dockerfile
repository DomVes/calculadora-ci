FROM python:3.13-slim

WORKDIR /app

COPY cliente/cliente.py .

ENV API_URL=http://api:5000
ENV PYTHONUNBUFFERED=1

CMD ["python", "cliente.py"]
