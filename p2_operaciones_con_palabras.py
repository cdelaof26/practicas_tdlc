import utilidades
import tabla


alfabeto: list[str]
w1: str
w2: str


def redefinir_datos():
    global alfabeto, w1, w2

    print("Redefinir el alfabeto requiere redefinir las palabras")
    print(" ¿Continuar con la operación?")
    print("1. Si")
    print("2. No")
    print("Selecciona una opción")
    if utilidades.seleccionar_opcion(["1", "2"], [False, True]):
        return

    utilidades.limpiar_pantalla()

    _alfabeto, _ = utilidades.nuevo_alfabeto(True)
    if _alfabeto is None:
        return

    alfabeto = _alfabeto
    _w1 = w1
    _w2 = w2
    w1 = utilidades.obtener_palabra_de_alfabeto(alfabeto, "w1", palabra=w1)
    w2 = utilidades.obtener_palabra_de_alfabeto(alfabeto, "w2", palabra=w2)
    if _w1 == w1:
        print("Se ha definido w1 como %a" % w1)
    if _w2 == w2:
        print("Se ha definido w2 como %a" % w2)


def seleccionar_palabra(instrucciones: str) -> bool:
    print(instrucciones)
    print("1. w1")
    print("2. w2")
    print("Selecciona una opción")
    seleccion = utilidades.seleccionar_opcion(["1", "2"], [True, False])

    utilidades.limpiar_pantalla()

    return seleccion


def prefijos_y_sufijos(cadena: str) -> str:
    prefijo_base, sufijo_base = cadena, cadena
    prefijos, sufijos = ["Prefijos"], ["Sufijos"]
    while prefijo_base:
        prefijos.append("%a" % prefijo_base)
        sufijos.append("%a" % sufijo_base)

        prefijo_base = prefijo_base[:-1]
        sufijo_base = sufijo_base[1:]

    prefijos.append("''")
    sufijos.append("''")

    return tabla.crear_recuadro([prefijos, sufijos])


def set_prefijos_sufijos():
    usar_w1 = seleccionar_palabra("Obtener los prefijos y sufijos de ...")
    print("  w = %a" % (w1 if usar_w1 else w2))
    print(prefijos_y_sufijos(w1 if usar_w1 else w2))


def potenciar_cadena(cadena: str, exponente: int) -> str:
    potencia = cadena * abs(exponente)
    if exponente < 0:
        return potencia[::-1]
    return potencia


def set_potencia():
    usar_w1 = seleccionar_palabra("Potenciar ...")

    print("Ingresa el exponente")
    exp = utilidades.obtener_entero()

    print("  w = %a" % (w1 if usar_w1 else w2))
    print(potenciar_cadena(w1 if usar_w1 else w2, exp))


def contar_simbolo(cadena: str, simbolo: str) -> int:
    return cadena.count(simbolo)


def set_contar_simbolo():
    global alfabeto

    usar_w1 = seleccionar_palabra("Evaluar ...")

    print("Símbolos disponibles")
    simbolo = utilidades.seleccionar_opcion_en_lista(alfabeto)

    print(f" |w|{simbolo} =", contar_simbolo(w1 if usar_w1 else w2, simbolo))


def menu_uno():
    global alfabeto, w1, w2

    menu = [
        "  Menu de operaciones ",
        "1. Ingresar palabras",
        "2. Redefinir alfabeto",
        "",
        "S. Salir"
    ]

    print(tabla.crear_recuadro(menu))
    print("Selecciona una opción")
    seleccion = utilidades.seleccionar_opcion(["1", "2", "S"])

    if seleccion != "S":
        utilidades.limpiar_pantalla()

    if seleccion == "1":
        if alfabeto is None:
            print("Se requiere definir un alfabeto!")
        else:
            w1 = utilidades.obtener_palabra_de_alfabeto(alfabeto, "w1")
            w2 = utilidades.obtener_palabra_de_alfabeto(alfabeto, "w2")
    elif seleccion == "2":
        alfabeto, _ = utilidades.nuevo_alfabeto(True)
    else:
        exit(0)


def menu_dos():
    global alfabeto, w1, w2

    menu = [
        "    Menu de operaciones ",
        "1. Redefinir w1 = %a" % w1,
        "2. Redefinir w2 = %a" % w2,
        "3. Redefinir alfabeto",
        "",
        "4. Longitud de w1 y w2",
        "5. Prefijos y sufijos de ...",
        "6. Concatenar w1 y w2",
        "7. Longitud de concatenar w1 y w2",
        "8. Potenciar ...",
        "9. Evaluar ... en N",
        "",
        "S. Salir"
    ]

    print(tabla.crear_recuadro(menu))
    print("Selecciona una opción")
    seleccion = utilidades.seleccionar_opcion([f"{i}" for i in range(1, 11 + 1)] + ["S"])

    if seleccion != "S":
        utilidades.limpiar_pantalla()

    if seleccion == "1":
        w1 = utilidades.obtener_palabra_de_alfabeto(alfabeto, "w1")
    elif seleccion == "2":
        w2 = utilidades.obtener_palabra_de_alfabeto(alfabeto, "w2")
    elif seleccion == "3":
        redefinir_datos()
    elif seleccion == "4":
        print("|w1| =", len(w1))
        print("|w2| =", len(w2))
    elif seleccion == "5":
        set_prefijos_sufijos()
    elif seleccion == "6":
        print("w1•w2 =", w1 + w2)
    elif seleccion == "7":
        print("|w1•w2| =", len(w1 + w2))
    elif seleccion == "8":
        set_potencia()
    elif seleccion == "9":
        set_contar_simbolo()

    if seleccion != "S":
        utilidades.mostrar_proceso_terminado()
    else:
        exit(0)


if __name__ == "__main__":
    print("  Práctica 2 - Operaciones con palabras")
    print(" De La O Flores Cristopher - 4CV1\n")

    alfabeto, _ = utilidades.nuevo_alfabeto(True)
    w1, w2 = "", ""

    while True:
        utilidades.limpiar_pantalla()

        try:
            if not w1:
                menu_uno()
                continue

            menu_dos()

            utilidades.limpiar_pantalla()
        except KeyboardInterrupt:
            utilidades.mostrar_proceso_terminado(True)
