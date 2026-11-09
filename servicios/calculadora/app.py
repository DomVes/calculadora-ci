"""Aplicación de la calculadora.

Habla con el otro contenedor por el nombre del servicio `bitacora`.
Cada operación se guarda y se vuelve a leer antes de responder.
"""

import json
import os
import urllib.error
import urllib.request

from flask import Flask, jsonify, request

from calculadora import dividir, multiplicar, potencia, restar, sumar
from config import cargar_config

app = Flask(__name__)

OPERACIONES = {
    "sumar": sumar,
    "restar": restar,
    "multiplicar": multiplicar,
    "dividir": dividir,
    "potencia": potencia,
}

BITACORA_URL = os.environ.get("BITACORA_URL", "http://bitacora:8080").rstrip("/")
TOKEN = os.environ.get("BITACORA_TOKEN", "")


def pedir(metodo: str, ruta: str, cuerpo: dict | None = None) -> dict:
    if not TOKEN:
        raise RuntimeError("Falta BITACORA_TOKEN")
    datos = None if cuerpo is None else json.dumps(cuerpo).encode("utf-8")
    peticion = urllib.request.Request(
        f"{BITACORA_URL}{ruta}",
        data=datos,
        headers={"Content-Type": "application/json", "X-Token": TOKEN},
        method=metodo,
    )
    with urllib.request.urlopen(peticion, timeout=5) as respuesta:
        return json.load(respuesta)


def guardar_y_leer(operacion: str, a, b, resultado: float) -> tuple[dict, dict]:
    guardado = pedir(
        "POST",
        "/registros",
        {"operacion": operacion, "a": a, "b": b, "resultado": resultado},
    )
    leido = pedir("GET", f"/registros/{guardado['id']}")
    if leido.get("id") != guardado.get("id") or leido.get("resultado") != resultado:
        raise RuntimeError("La bitacora no devolvio el mismo registro")
    return guardado, leido


@app.get("/salud")
def salud():
    ambiente, config = cargar_config()
    return jsonify(
        {
            "estado": "ok",
            "ambiente": ambiente,
            "base_datos": config["base_datos"],
            "bitacora": BITACORA_URL,
        }
    )


@app.post("/operar")
def operar():
    cuerpo = request.get_json(silent=True) or {}
    operacion = cuerpo.get("operacion")
    if operacion not in OPERACIONES:
        return jsonify({"error": "operacion desconocida"}), 400
    if "a" not in cuerpo or "b" not in cuerpo:
        return jsonify({"error": "faltan operandos"}), 400
    try:
        resultado = OPERACIONES[operacion](cuerpo["a"], cuerpo["b"])
        guardado, leido = guardar_y_leer(operacion, cuerpo["a"], cuerpo["b"], resultado)
    except ZeroDivisionError:
        return jsonify({"error": "division por cero"}), 400
    except (urllib.error.URLError, RuntimeError, KeyError, TimeoutError) as exc:
        return jsonify({"error": "sin comunicacion con bitacora", "detalle": str(exc)}), 502
    return jsonify(
        {
            "operacion": operacion,
            "a": cuerpo["a"],
            "b": cuerpo["b"],
            "resultado": resultado,
            "destino": BITACORA_URL,
            "guardado": guardado,
            "leido": leido,
        }
    )


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("Falta BITACORA_TOKEN. Copia .env.example a .env.")
    app.run(host="0.0.0.0", port=5000)
