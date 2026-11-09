# Cómo armar el PDF de evidencias

El docente pide subir en la plataforma un PDF con el enlace al repositorio. Las capturas tienen que salir de una máquina donde Docker sí se ejecutó. No sirven imágenes inventadas.

Repositorio: https://github.com/DomVes/calculadora-ci

## Antes de capturar

```powershell
Copy-Item .env.example .env
notepad .env
```

Cambien `BITACORA_TOKEN` por una clave del grupo. No dejen esa clave en el PDF: tapen el valor si aparece en pantalla.

## Capturas, en este orden

1. `docker compose build`. Debe terminar sin error y mostrar las dos imágenes, `calculadora:entrega1` y `bitacora:entrega1`.
2. `docker compose up -d`. Deben verse los dos servicios en la red `calculadora_red`.
3. `docker compose ps`. Los dos contenedores en ejecución.
4. `docker network inspect calculadora_red`. En la salida deben aparecer los nombres `calculadora` y `bitacora`.
5. La prueba de comunicación:

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:5000/operar -ContentType "application/json" -Body '{"operacion":"sumar","a":2,"b":3}'
```

Tiene que verse `destino : http://bitacora:8080`, un `guardado` con id y un `leido` con el mismo id y `resultado : 5`.

## Diagrama para pegar en el PDF

```text
[ equipo del grupo ] -- localhost:5000 --> [ calculadora ]
                                              |
                                              | http://bitacora:8080
                                              v
                                         [ bitacora ]
                                              |
                                              v
                                    volumen bitacora_datos
                                    /datos/registros.json
```

## Conclusiones que pueden usar

La calculadora y la bitácora quedan en contenedores separados y solo se ven por la red de Compose. Guardar la operación y leerla de inmediato demuestra que el dato cruzó de un servicio al otro y quedó en el volumen. Usar el nombre `bitacora`, y no localhost ni una IP fija, permite que Docker resuelva la dirección aunque los contenedores cambien de IP. La clave no viaja en el código: entra por `.env` al crear los contenedores, y GitHub Actions construye las dos imágenes en cada push.

## Referencias (APA 7)

Docker Inc. (2026). *Dockerfile reference*. https://docs.docker.com/reference/dockerfile/

Docker Inc. (2026). *Networking in Compose*. https://docs.docker.com/compose/how-tos/networking/

GitHub. (2026). *Workflow syntax for GitHub Actions*. https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax

Olarte, J. (2026). *Entrega proyecto 1: Docker con dos contenedores comunicados* [indicaciones de clase]. Politécnico Grancolombiano.
