"""API HTTP que expone las operaciones de la calculadora."""

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


@app.get("/salud")
def salud():
    ambiente, config = cargar_config()
    return jsonify(
        {
            "estado": "ok",
            "ambiente": ambiente,
            "base_datos": config["base_datos"],
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
    except ZeroDivisionError:
        return jsonify({"error": "division por cero"}), 400
    return jsonify(
        {
            "operacion": operacion,
            "a": cuerpo["a"],
            "b": cuerpo["b"],
            "resultado": resultado,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
