"""Bitácora: guarda y devuelve las operaciones de la calculadora.

Los datos viven en un archivo del volumen, no en la imagen.
La clave llega por BITACORA_TOKEN; no está escrita en el código.
"""

import hmac
import json
import os
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)
DATOS = Path(os.environ.get("DATOS_DIR", "/datos"))
TOKEN = os.environ.get("BITACORA_TOKEN", "")


def archivo() -> Path:
    DATOS.mkdir(parents=True, exist_ok=True)
    return DATOS / "registros.json"


def leer() -> list:
    ruta = archivo()
    if not ruta.exists():
        return []
    return json.loads(ruta.read_text(encoding="utf-8"))


def escribir(registros: list) -> None:
    archivo().write_text(
        json.dumps(registros, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def autorizado() -> bool:
    if not TOKEN:
        return False
    recibido = request.headers.get("X-Token", "")
    return hmac.compare_digest(recibido, TOKEN)


@app.get("/salud")
def salud():
    return jsonify({"estado": "ok", "servicio": "bitacora"})


@app.post("/registros")
def crear():
    if not autorizado():
        return jsonify({"error": "no autorizado"}), 401
    cuerpo = request.get_json(silent=True) or {}
    registros = leer()
    nuevo = {
        "id": (registros[-1]["id"] + 1) if registros else 1,
        "operacion": cuerpo.get("operacion"),
        "a": cuerpo.get("a"),
        "b": cuerpo.get("b"),
        "resultado": cuerpo.get("resultado"),
    }
    registros.append(nuevo)
    escribir(registros)
    return jsonify(nuevo), 201


@app.get("/registros/<int:registro_id>")
def obtener(registro_id: int):
    if not autorizado():
        return jsonify({"error": "no autorizado"}), 401
    for registro in leer():
        if registro["id"] == registro_id:
            return jsonify(registro)
    return jsonify({"error": "no encontrado"}), 404


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("Falta BITACORA_TOKEN. Copia .env.example a .env.")
    app.run(host="0.0.0.0", port=8080)
