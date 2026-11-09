from calculadora import dividir, multiplicar, potencia, restar, sumar


def test_sumar():
    assert sumar(2, 3) == 5


def test_restar():
    assert restar(5, 3) == 2


def test_multiplicar():
    assert multiplicar(4, 3) == 12


def test_dividir():
    assert dividir(8, 2) == 4


def test_potencia():
    assert potencia(2, 3) == 8
