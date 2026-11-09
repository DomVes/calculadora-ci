# Respuestas de la guía de manejo de repositorios

Las respuestas usan el historial real de este repositorio.

## Ejercicio 1. Directorio de trabajo, preparación y repositorio

Son tres sitios distintos:

- **Directorio de trabajo.** La carpeta `calculadora-ci` con los archivos que se editan. Cambiar `calculadora.py` solo modifica esta copia.
- **Área de preparación.** El índice de Git. `git add` copia ahí la versión exacta que entrará en el próximo commit. `git status` separa lo que ya está preparado de lo que sigue solo en el directorio de trabajo.
- **Repositorio.** El historial guardado en `.git`. `git commit` no empaqueta “toda la carpeta”: registra lo que está en el área de preparación y lo enlaza con el commit anterior. `git log` lee ese historial.

Por eso el primer ejercicio ejecutó las pruebas, revisó `git status`, hizo `git add .` y solo entonces `git commit`. El commit `6d0d548` (*Agrega calculadora con pruebas*) contiene `calculadora.py`, `test_calculadora.py` y `.gitignore`.

## Ejercicio 2. Por qué Git no eligió una de las dos versiones

`feature/multiplicar` y `main` salieron del mismo commit y escribieron funciones distintas en las mismas líneas del final de `calculadora.py`. Git no sabe si la versión válida es `multiplicar`, `dividir` o las dos. Elegir una habría borrado trabajo de la otra rama.

El merge se detuvo con este conflicto:

```text
<<<<<<< HEAD
def dividir(a, b):
    return a / b
=======
def multiplicar(a, b):
    return a * b
>>>>>>> feature/multiplicar
```

La resolución borró los marcadores y dejó las dos funciones, con dos líneas en blanco entre ellas. El commit de esa decisión es `9217374` (*Fusiona multiplicar con dividir*). Las pruebas siguieron en 2 passed, porque en ese punto solo existían `test_sumar` y `test_restar`.

## Ejercicio 3. Por qué se prefiere `git revert`

`79fb7e9` (*Ajusta sumar*) cambió `return a + b` por `return a - b`. Pytest lo detectó: 1 failed, 1 passed (`sumar(2, 3)` devolvía `-1`).

`git revert --no-edit HEAD` creó `d72be4f` (*Revert "Ajusta sumar"*). El error sigue en el historial y un commit posterior lo deshace. Las pruebas volvieron a 2 passed.

Borrar el commit con `git reset` reescribe la historia. Si otra persona ya tiene ese commit, su copia y el remoto dejan de coincidir. `git revert` se publica con un push normal y no obliga a nadie a rehacer su clon.

### Reto de los dos commits atrás

Después del revert se ejecutó:

```text
git restore --source=HEAD~2 calculadora.py
git diff
git restore calculadora.py
```

`git diff` salió vacío. Es el resultado correcto de esa secuencia: `HEAD` ya es el revert, con `sumar` arreglada; `HEAD~1` es el commit roto; `HEAD~2` es la fusión `9217374`, que también tiene `return a + b`. Restaurar `HEAD~2` produce el mismo archivo que la versión actual. `git restore calculadora.py` devolvió el directorio de trabajo a esa versión, sin crear un commit.

La versión rota se puede mirar sin mover la rama:

```powershell
git show 79fb7e9:calculadora.py
```

## Ejercicio 4. Si GitHub no está disponible

Siguen existiendo todas las copias locales: este repositorio en el equipo y el clon de cada persona del equipo. También seguiría existiendo cualquier fork o respaldo que ya se hubiera hecho. Lo que se detiene es la copia compartida en GitHub, junto con los pull requests y GitHub Actions.

El equipo puede seguir haciendo commits, ramas y pruebas en local. Cuando el servicio vuelve, publica con `git push` y retoma los pull requests. No hace falta reconstruir el proyecto desde cero: el historial ya está en cada `.git`.

En este trabajo la rama del colaborador es `feature/potencia` (`b82b5d6`, *Agrega potencia*). Añade `potencia(base, exponente)` y cubre con pruebas `multiplicar`, `dividir` y `potencia`, que hasta ese commit no tenían prueba. La fusión en `main` es `674b269` (*Fusiona rama feature/potencia*).

El ejercicio pide además un comentario de revisión en el pull request de GitHub. Esa evidencia aparece al publicar el remoto; en esta máquina `gh` aún no tiene una sesión iniciada. Los pasos están al final del `README.md`.

## Ejercicio 5. Tabla de ambientes

`APP_ENV` elige la entrada de `CONFIG`. Si la variable no existe, el ambiente es `desarrollo`. Un nombre desconocido, por ejemplo `staging`, lanza `ValueError`. Cada ambiente tiene su propia base de datos: `dev.db`, `test.db` y `prod.db`. Producción es el único con `depuracion` en `False`.

Comprobación pedida por la guía: con `depuracion` en `True` dentro de producción, `test_produccion_sin_depuracion` falla. El archivo quedó otra vez en `False`.

| Situación | Clasificación |
| --- | --- |
| Una desarrolladora prueba una función nueva con datos ficticios | Desarrollo |
| El equipo QA ejecuta sus pruebas en un servidor compartido | Pruebas |
| El cliente y usuarios invitados evalúan una versión antes del lanzamiento | Entorno intermedio |
| Un desarrollador copia datos reales de clientes a su portátil | Mala práctica |
| Alguien edita un archivo directamente en el servidor que atiende a los usuarios | Mala práctica |

La copia de datos reales al portátil saca información de producción del control de acceso y del registro de cambios. Editar el servidor a mano salta el repositorio, las pruebas y el pipeline: el arreglo no queda versionado y no se puede repetir ni revertir con seguridad.

## Ejercicio 6. Qué parte manual del ejercicio 1 hace ahora el pipeline

En el ejercicio 1 la instalación de pytest y `python -m pytest` se hacían a mano antes de guardar la versión. `.github/workflows/ci.yml` lo hace solo en cada `push` a `main` y en cada `pull_request` hacia `main`:

1. Descarga el commit (`actions/checkout`).
2. Prepara Python. El reto de la guía amplía el job a una matriz con **3.12** y **3.13** (`fail-fast: false`, para ver las dos versiones aunque una falle).
3. Instala pytest.
4. Ejecuta `python -m pytest`.

El commit `30c13b9` agrega el pipeline con Python 3.13. El commit `3560451` agrega la matriz. La fusión a `main` es `54229f4`.

La rama `prueba/romper-ci` vuelve a cambiar `sumar` para que reste. Ese commit, `06375f3` (*Rompe sumar a proposito*), deja la suite en 1 failed y 8 passed. `e70141a` (*Revert "Rompe sumar a proposito"*) la devuelve a 9 passed sin borrar el commit del error. En GitHub, el primer push de esa rama marca el check en rojo y el push del revert lo pasa a verde. Aquí esa secuencia quedó verificada con pytest en local; los checks de Actions se generan al publicar el pull request.
