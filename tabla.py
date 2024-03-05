from typing import Union


def encontrar_mayor(datos: list) -> int:
    mayor = -1
    for elemento in datos:
        longitud_de_elemento = len(str(elemento))
        if longitud_de_elemento > mayor:
            mayor = longitud_de_elemento

    return mayor


def encontrar_longitud_de_tabla(tabla: list[list]) -> tuple[int, int]:
    columna_mayor = 0
    for columna in tabla:
        longitud_de_columna = len(columna)
        if longitud_de_columna > columna_mayor:
            columna_mayor = longitud_de_columna

    return columna_mayor, len(tabla)


def rellenar_tabla(tabla: list[list], m: int, n: int):
    if len(tabla) < n:
        tabla += [[""] * (n - len(tabla))]

    for i, columna in enumerate(tabla):
        longitud_de_columna = len(columna)
        if longitud_de_columna < m:
            tabla[i] = columna + [""] * (m - longitud_de_columna)


def ensamblar_tabla_simple(tabla: list[str]):
    elemento_mayor = encontrar_mayor(tabla)
    borde = f"+{'-' * (elemento_mayor + 2)}+"

    tabla_str = borde + "\n"

    for dato in tabla:
        dato = str(dato).ljust(elemento_mayor, " ")
        tabla_str += f"| {dato} |\n"

    return tabla_str + borde


def es_lista_de_listas(tabla: list) -> bool:
    lista_de_listas = True
    for elemento in tabla:
        lista_de_listas = lista_de_listas and isinstance(elemento, list)
        if not lista_de_listas:
            break

    return lista_de_listas


def encontrar_lista_de_elementos_mayores(tabla: list[list]):
    elementos_mayores = list()
    for columna in tabla:
        elementos_mayores.append(encontrar_mayor(columna))

    return elementos_mayores


def ensamblar_borde_compuesto(elementos_mayores: list[int], para_tabla: bool = True):
    borde = "+"

    if not para_tabla:
        borde += "--"

    for mayor in elementos_mayores:
        if para_tabla:
            mayor += 2
            borde += '-' * mayor + "+"
        else:
            mayor += 1
            borde += '-' * mayor

    borde = borde[:-1]
    borde += "+"

    return borde


def ensamblar_tabla(tabla: list[list], elementos_mayores: list[int], borde: str, como_tabla: bool) -> str:
    tabla_str = borde + "\n"
    m, n = encontrar_longitud_de_tabla(tabla)
    rellenar_tabla(tabla, m, n)

    for j in range(m):
        if j == 1 and como_tabla:
            tabla_str += borde + "\n"

        if not como_tabla:
            tabla_str += "| "

        for i in range(n):
            dato = str(tabla[i][j]).ljust(elementos_mayores[i], " ")
            if not como_tabla:
                tabla_str += f"{dato} "
            else:
                tabla_str += f"| {dato} "
        tabla_str += "|\n"

    return tabla_str + borde


def crear_recuadro(datos: Union[list[list], list[str]], como_tabla: bool = True) -> str:
    if not datos:
        return ""

    lista_de_listas = es_lista_de_listas(datos)

    if len(datos) == 1 and lista_de_listas:
        lista_de_listas = False
        datos = datos[0]

    if not lista_de_listas:
        return ensamblar_tabla_simple(datos)

    elementos_mayores = encontrar_lista_de_elementos_mayores(datos)
    borde = ensamblar_borde_compuesto(elementos_mayores, como_tabla)

    return ensamblar_tabla(datos, elementos_mayores, borde, como_tabla)
