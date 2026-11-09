FROM python:3.13.18-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY servicios/bitacora/app.py ./app.py

ENV DATOS_DIR=/datos
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /datos

EXPOSE 8080

VOLUME ["/datos"]

CMD ["python", "app.py"]
