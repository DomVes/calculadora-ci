# Entrega 1. Dos contenedores comunicados

Corte del 10 de noviembre de 2026. La aplicación y la bitácora son servicios distintos. La calculadora guarda un dato en la bitácora y lo lee de vuelta, usando el nombre `bitacora` dentro de la red de Compose.

## Papel de cada contenedor

| Servicio | Imagen | Papel |
| --- | --- | --- |
| `calculadora` | `calculadora:entrega1`, construida con `python:3.13.18-slim-bookworm` | Aplicación. Expone el puerto 5000 y arranca con `python app.py` |
| `bitacora` | `bitacora:entrega1`, la misma imagen base fijada | Almacén. Guarda cada operación en el volumen `bitacora_datos` y la devuelve por el puerto 8080 |

La etiqueta de la imagen base es la versión `3.13.18` sobre Debian Bookworm. No se usa `latest`.

## Ida y vuelta

```text
quien prueba                red calculadora_red
    |                                |
    |  POST localhost:5000/operar    |
    |-------------------------------> calculadora
    |                                |  POST http://bitacora:8080/registros
    |                                |---------------------------> bitacora
    |                                |  guarda en /datos/registros.json
    |                                |  GET  http://bitacora:8080/registros/1
    |                                |<---------------------------|
    |  destino, guardado y leido     |
    |<-------------------------------|
```

`localhost` solo aparece en el equipo de quien prueba, para entrar a la aplicación. De un contenedor al otro la dirección es `http://bitacora:8080`, declarada en `docker-compose.yml`.

`depends_on` espera a que el healthcheck de `bitacora` pase. La clave `BITACORA_TOKEN` llega desde `.env` a los dos servicios. El archivo `.env` está en `.gitignore`. En el repositorio solo está `.env.example`.

## Comandos

```powershell
Copy-Item .env.example .env
docker compose build
docker compose up -d
docker compose ps
docker network inspect calculadora_red
Invoke-RestMethod -Method Post -Uri http://localhost:5000/operar -ContentType "application/json" -Body '{"operacion":"sumar","a":2,"b":3}'
docker compose down
```

En la respuesta, `destino` debe ser `http://bitacora:8080` y `leido` debe repetir el registro que acaba de guardarse.

## Pipeline

El job `imagenes` de `.github/workflows/ci.yml` copia `.env.example` a `.env`, ejecuta `docker compose build`, levanta los dos contenedores y hace la misma operación de guardar y leer. El check queda verde solo si esa ida y vuelta funciona.
