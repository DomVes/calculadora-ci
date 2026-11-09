# Calculadora CI

Proyecto de la **primera entrega** del módulo Integración Continua (Politécnico Grancolombiano) y de la guía *Manejo de repositorios*. Una calculadora pequeña recorre el flujo completo: primer commit, ramas, conflicto, reversión, integración de un cambio, ambientes, pipeline y dos contenedores que se comunican.

## Cómo ejecutar las pruebas

```powershell
python -m pip install pytest
python -m pytest
```

Resultado esperado en `main`: 9 pruebas en verde.

## Cómo levantar los dos contenedores

Hace falta Docker Desktop en ejecución. Los contenedores `api` y `cliente` comparten la red `calculadora_red`. El cliente llama a `http://api:5000`; ese nombre solo existe dentro de la red de Compose.

```powershell
docker compose up --build --abort-on-container-exit --exit-code-from cliente
```

El cliente termina con código 0 cuando las cinco operaciones responden bien. El detalle del diseño está en [docs/entrega-1.md](docs/entrega-1.md).

Sin Docker se puede comprobar el mismo protocolo en la máquina:

```powershell
python -m pip install -r requirements.txt
$env:APP_ENV = "desarrollo"
python -m api.app
```

En otra terminal:

```powershell
$env:API_URL = "http://127.0.0.1:5000"
python cliente/cliente.py
Remove-Item Env:API_URL
```

## Mapa del repositorio

| Ruta | Rol |
| --- | --- |
| `calculadora.py` | Operaciones: sumar, restar, dividir, multiplicar y potencia |
| `test_calculadora.py` | Pruebas de esas operaciones |
| `config.py` | Configuración de desarrollo, pruebas y producción |
| `test_config.py` | Pruebas de ambientes |
| `.github/workflows/ci.yml` | GitHub Actions: Python 3.12 y 3.13 |
| `api/` | Contenedor que publica la calculadora por HTTP |
| `cliente/` | Contenedor que consume la API y valida las respuestas |
| `docker-compose.yml` | Red y arranque de los dos contenedores |
| `docs/respuestas-guia.md` | Respuestas de la guía y tabla de ambientes |
| `docs/entrega-1.md` | Evidencia de la entrega 1 |

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

La lectura del módulo pide, en la semana 3, el proyecto en GitHub y **dos contenedores comunicados**. Este repositorio es esa base. La comunicación es HTTP: `cliente` espera a `api` y le envía las operaciones. Jenkins, Travis CI y Codeship corresponden a las entregas 2 y 3; no forman parte de este corte.

## Repositorio

El remoto `origin` es [github.com/DomVes/calculadora-ci](https://github.com/DomVes/calculadora-ci). Se creó vacío, sin README ni `.gitignore` de GitHub, y después se publicó `main` junto con las ramas de trabajo.

El pull request revisado es el [número 1](https://github.com/DomVes/calculadora-ci/pull/1). Su primer check quedó rojo y el siguiente, después de `git revert`, quedó verde.
