# Entrega 1. Repositorio y dos contenedores

Semana 3 del módulo. El corte pide el proyecto en un repositorio y, con Docker, dos contenedores comunicados entre sí. Jenkins, Travis CI y Codeship quedan para las entregas siguientes.

## Los dos contenedores

| Contenedor | Imagen | Función |
| --- | --- | --- |
| `api` | `calculadora-api:entrega1` | Publica la calculadora en HTTP, puerto 5000 |
| `cliente` | `calculadora-cliente:entrega1` | Llama a la API y comprueba sumar, restar, multiplicar, dividir y potencia |

Compose crea la red puente `calculadora_red` y conecta ahí a los dos. No se hablan por la red del anfitrión.

```text
cliente                         red calculadora_red                      api
  |                                     |                                  |
  |  GET  http://api:5000/salud         |                                  |
  |------------------------------------>|  APP_ENV=desarrollo              |
  |  {"estado":"ok","ambiente":...}     |  base_datos=dev.db               |
  |<------------------------------------|                                  |
  |  POST http://api:5000/operar        |                                  |
  |  {"operacion":"sumar","a":2,"b":3}  |                                  |
  |------------------------------------>|  calculadora.sumar(2, 3)        |
  |  {"resultado":5}                    |                                  |
  |<------------------------------------|                                  |
```

`depends_on` con `condition: service_healthy` hace que `cliente` espere el healthcheck de `api`. El healthcheck abre `http://127.0.0.1:5000/salud` **dentro** del contenedor de la API. El cliente, en cambio, usa el nombre `api`: dentro de su propio contenedor, `127.0.0.1` sería él mismo y no llegaría al otro.

`api` lee `APP_ENV`. En Compose vale `desarrollo`, así que `/salud` informa `dev.db`. Es la misma `cargar_config()` de `config.py`, no una configuración aparte.

## Contrato HTTP

`GET /salud` responde 200 con el ambiente activo y el nombre de su base de datos.

`POST /operar` recibe JSON:

```json
{"operacion": "sumar", "a": 2, "b": 3}
```

Operaciones aceptadas: `sumar`, `restar`, `multiplicar`, `dividir`, `potencia`. Una operación desconocida o un operando ausente responden 400. Dividir entre cero también responde 400.

El proceso del cliente sale con código 0 solo si los cinco resultados coinciden con los esperados. Ese código es el que usa:

```powershell
docker compose up --build --abort-on-container-exit --exit-code-from cliente
```

## Qué archivo construye cada imagen

`api/Dockerfile` parte de `python:3.13-slim`, instala `requirements.txt` (Flask) y copia `calculadora.py`, `config.py` y el paquete `api`. El comando es `python -m api.app`.

`cliente/Dockerfile` solo copia `cliente/cliente.py`. Habla con la biblioteca estándar (`urllib`), así que no instala Flask.

`.dockerignore` deja fuera `.git`, la caché de pytest y los documentos, para que la imagen no arrastre el historial ni archivos locales.

## Comprobación sin Docker Desktop

En este equipo no está instalado Docker. El mismo cliente se ejecutó contra la API en `http://127.0.0.1:5000`, que es el equivalente de un solo host. La comunicación entre contenedores hay que verla con el comando de Compose de arriba, porque el nombre `api` lo resuelve la red de Docker y no el sistema operativo.

## Relación con la guía de repositorios

La guía deja el proyecto versionado, con ramas y con un pipeline que prueba `calculadora.py` y `config.py` en cada pull request. Esta entrega añade el empaquetado: el mismo código corre en dos procesos aislados y se comunican por la red. El pipeline de la guía sigue instalando solo pytest, porque las pruebas unitarias no importan Flask. La dependencia web vive en la imagen `api`.

## Qué no incluye esta entrega

La entrega 2 pide un documento para implementar Jenkins. La entrega 3 pide la plataforma integrada con Jenkins, Travis CI y Codeship, más el historial de cambios y las responsabilidades del grupo. Esos puntos no se adelantan aquí.
