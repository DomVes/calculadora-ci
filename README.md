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
| `prueba/romper-ci` | Fusionada en `main` | Error deliberado y `git revert` que lo corrige |
| `feature/entrega1-docker` | Fusionada en `main` | Dos contenedores comunicados y esta documentación |

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
| Pull request revisado y fusionado | Rama `feature/potencia`, fusionada en `674b269`. El comentario de revisión en GitHub falta porque `gh` todavía no tiene sesión en este equipo |
| Configuración por ambiente | `config.py`, `test_config.py` y la tabla en `docs/respuestas-guia.md` |
| Pipeline que detecta el error y luego pasa | En local, `Rompe sumar a proposito` deja `test_sumar` en rojo (1 failed, 8 passed) y `Revert "Rompe sumar a proposito"` lo devuelve a 9 passed. En GitHub Actions el check rojo y el verde aparecen al publicar esa secuencia en un pull request |

## Primera entrega del módulo

La lectura del módulo pide, en la semana 3, el proyecto en GitHub y **dos contenedores comunicados**. Este repositorio es esa base. La comunicación es HTTP: `cliente` espera a `api` y le envía las operaciones. Jenkins, Travis CI y Codeship corresponden a las entregas 2 y 3; no forman parte de este corte.

## Publicar en GitHub

El remoto todavía no está conectado. Cuando la cuenta esté autenticada, desde esta carpeta:

```powershell
gh auth login --hostname github.com --git-protocol https --web
gh repo create calculadora-ci --public --source=. --remote=origin --push
git push -u origin feature/multiplicar feature/potencia feature/ambientes feature/entrega1-docker prueba/romper-ci
```

El repositorio de GitHub debe crearse **sin** README ni `.gitignore`, para que el primer `push` de `main` no sea rechazado. Después de publicarlo, cada push y cada pull request hacia `main` ejecutan `.github/workflows/ci.yml`.
