import utilidades


def calcular_factorial(n: int) -> int:
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i

    return factorial


def calcular_combinacion(n: int, p: int) -> float:
    # n son la cantidad de elementos
    # p son cuantos se toman por combinación
    return calcular_factorial(n) / (calcular_factorial(n - p) * calcular_factorial(p))


def calcular_tam_en_bytes(_conjunto: list[str], _elemento_compuesto: bool) -> tuple[int, int, str]:
    # La cantidad de elementos son 2 ** n
    #   Donde 'n' es la cantidad de elementos en el conjunto
    #
    # Si el conjunto contiene elementos compuestos (como "hola"), entonces el tamaño crece.
    # El problema es saber cuantos elementos compuestos hay en un elemento del conjunto
    # supongo que ese problema quedará pendiente...
    #    ** Al igual que con la potenciación de alfabetos
    #
    elementos_en_conjunto_exp = 2 ** len(_conjunto)

    if _elemento_compuesto:
        return elementos_en_conjunto_exp, 0, ""

    # Suponemos que las cadenas solo contienen caracteres ASCII, por lo que el tamaño es de 1 byte,
    # aunque en Python las cadenas son UTF-8 y pueden contener caracteres con más peso.
    tam_en_bytes = 0
    for tam_elemento in range(1, len(_conjunto) + 1):
        elementos_en_subconjunto = calcular_combinacion(len(_conjunto), tam_elemento)
        tam_en_bytes += elementos_en_subconjunto * tam_elemento
        # Comas y espacios
        tam_en_bytes += (elementos_en_subconjunto - 1) * 2

    #    {{}, {a, b, c}, {ab, ac, bc}, {abc}}
    #    {{}, {a, b, c, d}, {ab, ac, ad, bc, bd, cd}, {abc, abd, acd, bcd}, {abcd}}
    #
    tam_en_bytes += len(_conjunto) * 2 + 4  # Caracteres llaves
    tam_en_bytes += len(_conjunto) * 3  # Espacios y comas y saltos de línea

    tam_en_bytes, _prefijo = utilidades.reducir_magnitud(tam_en_bytes)

    return elementos_en_conjunto_exp, tam_en_bytes, _prefijo


def cambiar_binario_por_elemento(_conjunto: list[str], cadena_binaria: str) -> str:
    cadena = [elemento if c == "1" else "" for elemento, c in zip(_conjunto, cadena_binaria)]
    return "".join(cadena)
    # Código extendido:
    #   Parece que no hace mucha diferencia en rendimiento...
    #
    # cadena = ""
    # for i, c in enumerate(cadena_binaria):
    #     if c == "0":
    #         continue
    #     cadena += _conjunto[i]
    # return cadena


def potenciar_conjunto(_conjunto: list[str]) -> list[list[str]]:
    elementos_binarios = 2 ** len(_conjunto) - 1
    total = elementos_binarios
    longitud_de_numero = 0

    conjunto_potencia = []
    while elementos_binarios >= 0:
        if longitud_de_numero == 0:
            numero_binario = str(bin(elementos_binarios))[2:]
            longitud_de_numero = len(numero_binario)
            conjunto_potencia = [[] for _ in range(longitud_de_numero + 1)]
        else:
            numero_binario = bin(elementos_binarios)[2:].zfill(longitud_de_numero)

        elementos_binarios -= 1

        print(f"  {total - elementos_binarios} elementos de {total}", end="\r")

        # Esto nos dice a que conjunto corresponde,
        # si no existe el conjunto en el conjunto potencia, entonces lo creamos
        cantidad_de_unos = numero_binario.count("1")
        conjunto_potencia[cantidad_de_unos].append(cambiar_binario_por_elemento(_conjunto, numero_binario))

    print()

    return conjunto_potencia


if __name__ == "__main__":
    print("  Práctica 4 - Conjunto potencia")
    print(" De La O Flores Cristopher - 4CV1\n")

    conjunto, elemento_compuesto = utilidades.nuevo_conjunto(True, "conjunto")
    if conjunto is None:
        exit(1)

    utilidades.limpiar_pantalla()

    elementos, tam, prefijo = calcular_tam_en_bytes(conjunto, elemento_compuesto)

    if not utilidades.continuar_operacion(elementos, tam, prefijo):
        exit(0)

    utilidades.limpiar_pantalla()

    if not elemento_compuesto:
        print(f"Tamaño estimado del conjunto: %.2f {prefijo}" % tam)
    else:
        print("  No es posible obtener una estimación del espacio en memoria que se requiere.")

    print("Conjunto =", conjunto, f"; {len(conjunto)} elemento(s)", f"; elementos en P(c): {2 ** len(conjunto)}")

    try:
        print("Potenciando conjunto...")
        conjunto_exp = potenciar_conjunto(conjunto)
    except KeyboardInterrupt:
        exit(1)  # Terminamos el programa para que se libere la memoria al momento de la excepción

    for i, subconjunto in enumerate(conjunto_exp):
        conjunto_exp[i] = "{" + ", ".join(subconjunto) + "}"

    utilidades.mostrar_o_guardar_datos(conjunto_exp, "conjunto_pot", True)
    exit(0)
