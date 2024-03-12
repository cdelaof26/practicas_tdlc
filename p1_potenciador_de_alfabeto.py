import utilidades


def calcular_tam_en_bytes(_alfabeto: list[str], exponente: int, _elemento_compuesto: bool) -> tuple[int, int, str]:
    # Cada elemento en el alfabeto exponenciado debe tener _exponente_ veces cada elemento
    # del alfabeto original.
    #   Por ejemplo
    # alf = [a, b] ; e = 3 ; alf^e ~ [aaa, aab, aba, ...] ; len(alf^e) = 8
    #
    # Si el alfabeto contiene elementos compuestos (como "hola"), entonces el tamaño crece.
    # El problema es saber cuantos elementos compuestos hay en un elemento del alfabeto
    # supongo que ese problema quedará pendiente...
    #

    elementos_en_alf_exp = len(_alfabeto) ** exponente

    if _elemento_compuesto:
        return elementos_en_alf_exp, 0, ""

    # Suponemos que las cadenas solo contienen caracteres ASCII, por lo que el tamaño es de 1 byte,
    # aunque en Python las cadenas son UTF-8 y pueden contener caracteres con más peso.
    #
    # Al incluir "+ elementos_en_alf_exp" estamos agregando los saltos de línea
    #
    tam_en_bytes = elementos_en_alf_exp * exponente + elementos_en_alf_exp

    tam_en_bytes, _prefijo = utilidades.reducir_magnitud(tam_en_bytes)

    return elementos_en_alf_exp, tam_en_bytes, _prefijo


def combinar(_alfabeto: list[str], exponente: int = 1) -> list[str]:
    if not _alfabeto:
        raise ValueError("El alfabeto no puede ser vacío")
    
    if exponente < 0:
        raise ValueError("No se permiten exponentes negativos")

    if exponente == 1:
        return _alfabeto

    if len(_alfabeto) == 1:
        return [_alfabeto[0] * exponente]

    org_alfabeto = _alfabeto.copy()
    combinaciones = []

    # Básicamente, este algoritmo hace la "multiplicación" de todos contra todos.
    # Su complejidad temporal es n^3 en un peor caso.
    #
    # En terminos de complejidad espacial es n^2.
    #

    for e in range(exponente - 1):
        # for c1 in _alfabeto:
        #     for c2 in org_alfabeto:
        #         combinaciones.append(c1 + c2)
        #
        # Quizá un poco menos legible, pero más veloz:
        #
        combinaciones = [c1 + c2 for c1 in _alfabeto for c2 in org_alfabeto]
        
        if exponente > 1:
            _cantidad_de_elementos = utilidades.numero_separado_por_comas(len(combinaciones))
            print(f"  [{e + 2} de {exponente}] Elementos en alfabeto: {_cantidad_de_elementos}", end="\r")
            _alfabeto = combinaciones
            combinaciones = []

    if exponente > 1:
        print()
        return _alfabeto

    return combinaciones


if __name__ == "__main__":
    print("  Práctica 1 - Potenciador de alfabetos")
    print(" De La O Flores Cristopher - 4CV1\n")

    alfabeto, elemento_compuesto = utilidades.nuevo_conjunto(True)
    if alfabeto is None:
        exit(1)

    utilidades.limpiar_pantalla()
    print("Ingresa el exponente")
    exp = utilidades.obtener_natural(True)

    utilidades.limpiar_pantalla()

    elementos, tam, prefijo = calcular_tam_en_bytes(alfabeto, exp, elemento_compuesto)

    if not utilidades.continuar_operacion(elementos, tam, prefijo):
        exit(0)

    utilidades.limpiar_pantalla()
    
    if not elemento_compuesto:
        print(f"Tamaño estimado del alfabeto: %.2f {prefijo}" % tam)
    else:
        print("  No es posible obtener una estimación del espacio en memoria que se requiere.")

    print("Alfabeto =", alfabeto, f"; {len(alfabeto)} elemento(s)")
    print("Exponente =", exp)

    try:
        print("Potenciando alfabeto...")
        alf_exp = combinar(alfabeto, exp)
    except KeyboardInterrupt:
        exit(1)  # Terminamos el programa para que se libere la memoria al momento de la excepción
    
    utilidades.mostrar_o_guardar_datos(alf_exp, "alfabeto_exp")
    exit(0)
