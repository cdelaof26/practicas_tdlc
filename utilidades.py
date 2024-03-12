from typing import Optional, Union
from datetime import datetime
from subprocess import call
import re


SISTEMA = "nt"
try:
    from os import uname
    SISTEMA = uname()[0]
except ImportError:
    pass


def limpiar_pantalla():
    global SISTEMA
    if SISTEMA == "nt":
        call("cls", shell=True)
    else:
        call("clear", shell=True)


def seleccionar_opcion(opciones: list[str], valores: Optional[list] = None) -> any:
    if valores is not None and len(opciones) != len(valores):
        raise ValueError("La lista de opciones debe ser del mismo tamaño que la de valores")

    opcion = ""
    while not opcion:
        opcion = input("> ").upper()
        if opcion not in opciones:
            print("  -> La opción ingresada no es parte del menú")
            opcion = ""

    if valores is not None:
        return valores[opciones.index(opcion)]

    return opcion


def seleccionar_opcion_en_lista(
        opciones: list[str], valores: Optional[list] = None, instrucciones: str = ""
) -> any:
    if not opciones:
        return None

    if valores is not None and len(opciones) != len(valores):
        raise ValueError("La lista de opciones debe ser del mismo tamaño que la de valores")

    if instrucciones:
        print(instrucciones)

    seleccionables = []
    for i, v in zip(range(1, len(opciones) + 1), opciones):
        seleccionables.append(f"{i}")
        print(f"{i}. {v}")

    print("Selecciona una opción")
    seleccion = seleccionar_opcion(seleccionables, opciones)
    if valores is not None:
        return valores[opciones.index(seleccion)]

    return seleccion


def obtener_natural(permitir_cero: bool) -> int:
    numero = ""
    regex = "[0-9]" if permitir_cero else "[1-9]"
    rango = "[" if permitir_cero else "("

    while not numero:
        numero = input("> ")
        if re.sub(regex, "", numero):
            print(f"La cadena {numero} no es número entero el en rango {rango}0, inf)")
            numero = ""

    return int(numero)


def obtener_entero() -> int:
    numero = ""

    while not numero:
        numero = input("> ")
        if re.sub("-?[0-9]", "", numero):
            print(f"La cadena {numero} no es número entero")
            numero = ""

    return int(numero)


def obtener_lista_como_alfabeto() -> tuple[list[str], bool]:
    lista = []
    elemento_compuesto = False

    print("  -> Ingresa una cadena vacía para terminar")
    while True:
        print(f"Ingresa un elemento ; ingresados: {len(lista)}")
        e = input("> ")
        if not e:
            break

        if not elemento_compuesto:
            elemento_compuesto = len(e) > 1

        lista.append(e)
        limpiar_pantalla()

    return lista, elemento_compuesto


def obtener_alfabeto(como_lista: bool) -> tuple[list[str], bool]:
    limpiar_pantalla()

    if not como_lista:
        print("Ingresa la cadena")
        alf = input("> ")
        return re.findall(".", alf), False
    
    print("Ingresa el alfabeto")
    return obtener_lista_como_alfabeto()


def nuevo_conjunto(requerido: bool, elemento="alfabeto") -> tuple[Optional[list[str]], Optional[bool]]:
    print(f"Obtención del {elemento}")
    print("1. Seleccionar todos los caracteres en una cadena")
    print("2. Ingresar los elementos uno por uno")
    print("Selecciona una opción")
    seleccion = seleccionar_opcion(["1", "2"], [False, True])
    conjunto, elemento_compuesto = obtener_alfabeto(seleccion)

    if not conjunto and requerido:
        print(f"No se ingreso un {elemento}, terminando...")
        return None, None

    return conjunto, elemento_compuesto


def palabra_pertenece_a_alfabeto(alfabeto: list[str], palabra: str) -> bool:
    caracteres_no_permitidos = []

    for c in palabra:
        if c not in alfabeto:
            caracteres_no_permitidos.append(c)

    if caracteres_no_permitidos:
        print(f"Los caracteres {caracteres_no_permitidos} no pertenecen al alfabeto dado")
        return False

    return True


def obtener_palabra_de_alfabeto(alfabeto: list[str], nombre: str, palabra: Optional[str] = None) -> str:
    do_one = palabra is not None
    if not do_one:
        palabra = ""

    while not palabra or do_one:
        do_one = False
        if not palabra:
            print(f"Ingresa la palabra {nombre}")
            palabra = input("> ")

        if not palabra_pertenece_a_alfabeto(alfabeto, palabra):
            palabra = ""

    return palabra


def obtener_lenguaje(alfabeto: list[str], nombre: str, permitir_vacio=False) -> list[str]:
    print(f"Ingresa las palabras del alfabeto {nombre}")
    print("  Ingresa una cadena vacía para terminar")

    lenguaje = []
    while True:
        print(f"{len(lenguaje)} palabras ingresadas para {nombre}")
        palabra = input("> ")
        if not palabra:
            if permitir_vacio:
                print("Se requiere de al menos un elemento!")
                continue
            break

        if not palabra_pertenece_a_alfabeto(alfabeto, palabra):
            continue

        lenguaje.append(palabra)
        limpiar_pantalla()

    return lenguaje


def reducir_magnitud(tam_en_bytes: int) -> tuple[int, str]:
    prefijos = ["B", "KB", "MB", "GB", "TB"]
    index_prefijo = 0

    while tam_en_bytes > 1000:
        tam_en_bytes /= 1000

        if index_prefijo + 1 < len(prefijos):
            index_prefijo += 1
        else:
            break

    return tam_en_bytes, prefijos[index_prefijo]


def continuar_operacion(elementos: int, tam: int, prefijo: str) -> bool:
    if (tam > 500 and prefijo == "MB") or prefijo == "GB" \
            or prefijo == "TB" or (not prefijo and elementos > 10 ** 6):
        if prefijo:
            print(f"La operación requiere de %.2f {prefijo} de espacio en memoria" % tam)
        else:
            cantidad_de_elementos = numero_separado_por_comas(elementos)
            print("  No es posible obtener una estimación del espacio en memoria que se requiere.")
            print(f"El alfabeto potenciado tendrá un total de {cantidad_de_elementos} elementos")

        print("  ¿Continuar con la operación?")
        print("1. Si")
        print("2. No, cancelar")
        print("Selecciona una opción")
        return seleccionar_opcion(["1", "2"], [True, False])

    return True


def potenciar_elementos(elementos: Union[str, list], exponente: int) -> str:
    potencia = elementos * abs(exponente)

    if exponente < 0:
        if isinstance(elementos, list):
            for i, e in elementos:
                elementos[i] = e[::1]

        return potencia[::-1]

    return potencia


def set_potencia(opciones: list[str], valores: list, nombre: str):
    seleccion = seleccionar_opcion_en_lista(opciones, valores, "Potenciar ...")

    print("Ingresa el exponente")
    exp = obtener_entero()

    print(f"  {nombre} = %a" % seleccion)
    print(potenciar_elementos(seleccion, exp))


def numero_separado_por_comas(numero: int) -> str:
    _numero_reversa = str(numero)[::-1]
    if len(_numero_reversa) < 4:
        return str(numero)

    _numero = re.findall(r"\d{3}", _numero_reversa)
    
    for i, _num in enumerate(_numero):
        _numero[i] = _num[::-1]

    if len(_numero) * 3 < len(_numero_reversa):
        diferencia = len(_numero) * 3 - len(_numero_reversa)
        numeros_restantes = _numero_reversa[diferencia:]
        _numero.append(numeros_restantes[::-1])

    return ",".join(_numero[::-1])


def mostrar_proceso_terminado(ex: bool = False):
    if ex:
        print("\n    Proceso interrumpido!")

    input(" Presiona enter para continuar ")


def guardar(datos: list[str], usar_llaves: bool = False):
    nombre = datetime.now().strftime("%y_%m_%d %H.%M.%S") + ".txt"

    with open(nombre, "w") as fichero:
        if usar_llaves:
            cadena = ", \n".join(datos)
            cadena = "{" + cadena + "}"
        else:
            cadena = "\n".join(datos)
        fichero.write(cadena)

    print(" Guardado como:", nombre)


def mostrar_o_guardar_datos(datos: list[str], nombre: str, usar_llaves: bool = False):
    print("Operación terminanada!")
    print("1. Mostrar nuevo conjunto")
    print("2. Guardar nuevo conjunto")
    print("S. Salir")
    print("Selecciona una opción")
    seleccion = seleccionar_opcion(["1", "2", "S"])

    if seleccion == "1":
        cadena = str(datos)
        if usar_llaves:
            cadena = str(datos).replace("'", "").replace("[", "{").replace("]", "}")

        print(nombre, "=", cadena)
    elif seleccion == "2":
        guardar(datos, usar_llaves)
