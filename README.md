# Calculadora CI

Proyecto de la **primera entrega** del módulo Integración Continua (Politécnico Grancolombiano) y de la guía *Manejo de repositorios*. Una calculadora pequeña recorre el flujo completo: primer commit, ramas, conflicto, reversión, integración de un cambio, ambientes, pipeline y dos contenedores que se comunican.

## Cómo ejecutar las pruebas

```powershell
python -m pip install pytest
python -m pytest
```

Resultado esperado en `main`: 9 pruebas en verde.

## Cómo levantar los dos contenedores

Hace falta Docker Desktop en ejecución. Son dos servicios con papeles distintos:

- `calculadora` es la aplicación. Publica el puerto 5000.
- `bitacora` guarda cada operación en un volumen y la devuelve cuando se le pide.

La aplicación llama a `http://bitacora:8080`. Ese nombre solo existe dentro de la red `calculadora_red`. La clave está en `.env`, que no se sube al repositorio.

```powershell
Copy-Item .env.example .env
docker compose build
docker compose up -d
docker compose ps
docker network inspect calculadora_red
Invoke-RestMethod -Method Post -Uri http://localhost:5000/operar -ContentType "application/json" -Body '{"operacion":"sumar","a":2,"b":3}'
```

La respuesta debe traer `destino` igual a `http://bitacora:8080`, y el mismo registro en `guardado` y en `leido`. Para apagar:

```powershell
docker compose down
```

El detalle está en [docs/entrega-1.md](docs/entrega-1.md). Las capturas del PDF están indicadas en [docs/como-armar-el-pdf.md](docs/como-armar-el-pdf.md).

## Mapa del repositorio

| Ruta | Rol |
| --- | --- |
| `calculadora.py` | Operaciones: sumar, restar, dividir, multiplicar y potencia |
| `test_calculadora.py` | Pruebas de esas operaciones |
| `config.py` | Configuración de desarrollo, pruebas y producción |
| `test_config.py` | Pruebas de ambientes |
| `.github/workflows/ci.yml` | Pruebas en Python 3.12 y 3.13, y construcción de las dos imágenes |
| `.env.example` | Variables de ejemplo. La clave real va en `.env`, que no se versiona |
| `servicios/calculadora/` | Contenedor de la aplicación |
| `servicios/bitacora/` | Contenedor que guarda y devuelve cada operación |
| `docker-compose.yml` | Red, puertos, volumen, variables y `depends_on` |
| `docs/respuestas-guia.md` | Respuestas de la guía y tabla de ambientes |
| `docs/entrega-1.md` | Evidencia de la entrega 1 |
| `docs/como-armar-el-pdf.md` | Orden de las capturas, diagrama, conclusiones y referencias APA |

`.gitignore` excluye `__pycache__/`, `.pytest_cache/` y `.env`.

## Ramas

| Rama | Estado | Qué demuestra |
| --- | --- | --- |
| `main` | Integración | Historia que se puede entregar |
| `feature/multiplicar` | Conservada | El cambio que chocó con `dividir` |
| `feature/potencia` | Fusionada en `main` | Cambio integrado al estilo de un colaborador |
| `feature/ambientes` | Fusionada en `main` | Configuración por ambiente, pipeline y matriz de Python |
| `prueba/romper-ci` | Fusionada en `main` | Primer error deliberado y `git revert`, dentro del historial |
| `feature/entrega1-docker` | Fusionada en `main` | Dos contenedores comunicados y esta documentación |
| `prueba/checks-ci` | Fusionada en `main` | Pull request [#1](https://github.com/DomVes/calculadora-ci/pull/1): check rojo y después verde |

Historial:

```text
git log --oneline --graph --decorate --all
```

Las respuestas a las preguntas de la guía están en [docs/respuestas-guia.md](docs/respuestas-guia.md).

## Rúbrica de la guía

| Criterio | Evidencia |
| --- | --- |
| Commits claros y `.gitignore` correcto | Mensajes en español y `.gitignore` del primer commit |
| Conflicto resuelto sin perder cambios | `Fusiona multiplicar con dividir`: `dividir` y `multiplicar` conviven, separadas por dos líneas en blanco |
| Reversión sin reescribir el historial | `Ajusta sumar` sigue en el log; el commit siguiente es `Revert "Ajusta sumar"` |
| Pull request revisado y fusionado | [#1](https://github.com/DomVes/calculadora-ci/pull/1), con dos comentarios y fusión `974d46b`. El cambio del colaborador está en `feature/potencia`, fusionada en `674b269` |
| Configuración por ambiente | `config.py`, `test_config.py` y la tabla en `docs/respuestas-guia.md` |
| Pipeline que detecta el error y luego pasa | En el PR #1, *Ejecutar pruebas* falló en Python 3.12 y 3.13 ([run rojo](https://github.com/DomVes/calculadora-ci/actions/runs/42637037227)) y, tras el revert, pasó en las dos versiones ([run verde](https://github.com/DomVes/calculadora-ci/actions/runs/42637119575)) |

## Primera entrega del módulo

La entrega del 10 de noviembre pide dos contenedores comunicados y un PDF con capturas. `calculadora` guarda cada operación en `bitacora` y la vuelve a leer, usando el nombre del servicio dentro de `calculadora_red`. El PDF se sube en la plataforma, junto con el enlace de este repositorio. Jenkins, Travis CI y Codeship corresponden a las entregas siguientes.

## Repositorio

El remoto `origin` es [github.com/DomVes/calculadora-ci](https://github.com/DomVes/calculadora-ci). Se creó vacío, sin README ni `.gitignore` de GitHub, y después se publicó `main` junto con las ramas de trabajo.

El pull request revisado es el [número 1](https://github.com/DomVes/calculadora-ci/pull/1). Su primer check quedó rojo y el siguiente, después de `git revert`, quedó verde.
