"""Comprueba que la calculadora guardó y leyó el dato en la bitácora."""

import json
import urllib.request


def main() -> None:
    datos = json.dumps({"operacion": "sumar", "a": 2, "b": 3}).encode("utf-8")
    peticion = urllib.request.Request(
        "http://127.0.0.1:5000/operar",
        data=datos,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(peticion, timeout=10) as respuesta:
        cuerpo = json.load(respuesta)
    print(json.dumps(cuerpo, ensure_ascii=False, indent=2))
    if cuerpo.get("destino") != "http://bitacora:8080":
        raise SystemExit("La calculadora no uso el nombre del servicio bitacora")
    if cuerpo.get("resultado") != 5:
        raise SystemExit("Resultado inesperado")
    if cuerpo["guardado"]["id"] != cuerpo["leido"]["id"]:
        raise SystemExit("El registro leido no es el que se guardo")
    if cuerpo["leido"]["resultado"] != 5:
        raise SystemExit("La bitacora no devolvio el dato guardado")
    print("Comunicacion correcta: guardado y leido por http://bitacora:8080")


if __name__ == "__main__":
    main()
