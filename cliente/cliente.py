"""Cliente que llama a la API y comprueba la respuesta.

Dentro de Docker Compose la API se alcanza por el nombre del servicio `api`,
en la red calculadora_red. No usa localhost: ese nombre solo vería el propio
contenedor.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

API_URL = os.environ.get("API_URL", "http://api:5000").rstrip("/")

OPERACIONES = (
    ("sumar", 2, 3, 5),
    ("restar", 5, 3, 2),
    ("multiplicar", 4, 3, 12),
    ("dividir", 8, 2, 4),
    ("potencia", 2, 3, 8),
)


def esperar_api() -> None:
    ultimo_error = "sin intentos"
    for intento in range(1, 31):
        try:
            with urllib.request.urlopen(f"{API_URL}/salud", timeout=2) as respuesta:
                if respuesta.status == 200:
                    print(json.load(respuesta))
                    return
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            ultimo_error = str(exc)
            print(f"Esperando API ({intento}/30): {ultimo_error}")
            time.sleep(1)
    raise SystemExit(f"La API no respondió en {API_URL}: {ultimo_error}")


def operar(operacion: str, a: int, b: int) -> dict:
    datos = json.dumps({"operacion": operacion, "a": a, "b": b}).encode("utf-8")
    peticion = urllib.request.Request(
        f"{API_URL}/operar",
        data=datos,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(peticion, timeout=5) as respuesta:
        return json.load(respuesta)


def main() -> None:
    print(f"Conectando con {API_URL}")
    esperar_api()
    fallos = 0
    for operacion, a, b, esperado in OPERACIONES:
        cuerpo = operar(operacion, a, b)
        print(cuerpo)
        if cuerpo.get("resultado") != esperado:
            print(f"Resultado inesperado en {operacion}: {cuerpo.get('resultado')} != {esperado}")
            fallos += 1
    if fallos:
        raise SystemExit(f"{fallos} operacion(es) no coincidieron")
    print("Comunicacion correcta: el cliente recibió las cinco operaciones.")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.URLError as exc:
        print(f"No hubo comunicacion con la API: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
