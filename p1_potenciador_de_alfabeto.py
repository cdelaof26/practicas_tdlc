from datetime import datetime
import utilidades


def calcular_tam_en_bytes(_alfabeto: list[str], exponente: int, elemento_compuesto: bool) -> tuple[int, int, str]:
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

    if elemento_compuesto:
        return elementos_en_alf_exp, 0, ""

    # Suponemos que las cadenas solo contienen caracteres ASCII, por lo que el tamaño es de 1 byte,
    # aunque en Python las cadenas son UTF-8 y pueden contener caracteres con más peso.
    #
    # Al incluir "+ elementos_en_alf_exp" estamos agregando los saltos de línea
    # 
    tam_en_bytes = elementos_en_alf_exp * exponente + elementos_en_alf_exp

    prefijos = ["B", "KB", "MB", "GB", "TB"]
    index_prefijo = 0

    while tam_en_bytes > 1000:
        tam_en_bytes /= 1000

        if index_prefijo + 1 < len(prefijos):
            index_prefijo += 1
        else:
            break

    return elementos_en_alf_exp, tam_en_bytes, prefijos[index_prefijo]


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
        for i, c1 in enumerate(_alfabeto):
            for j, c2 in enumerate(org_alfabeto):
                combinaciones.append(c1 + c2)
        
        if exponente > 1:
            _cantidad_de_elementos = utilidades.numero_separado_por_comas(len(combinaciones))
            print(f"  [{e + 2} de {exponente}] Elementos en alfabeto: {_cantidad_de_elementos}", end="\r")
            _alfabeto = combinaciones
            combinaciones = []

    if exponente > 1:
        print()
        return _alfabeto

    return combinaciones


def guardar(datos: list[str]):
    nombre = datetime.now().strftime("%y_%m_%d %H.%M.%S") + ".txt"

    with open(nombre, "w") as fichero:
        fichero.write("\n".join(datos))

    print(" Guardado como:", nombre)


if __name__ == "__main__":
    print("  Práctica 1 - Potenciador de alfabetos")
    print(" De La O Flores Cristopher - 4CV1\n")

    alfabeto, elemento_compuesto = utilidades.nuevo_alfabeto(True)
    if alfabeto is None:
        exit(1)

    utilidades.limpiar_pantalla()
    print("Ingresa el exponente")
    exp = utilidades.obtener_natural(True)

    utilidades.limpiar_pantalla()

    elementos, tam, prefijo = calcular_tam_en_bytes(alfabeto, exp, elemento_compuesto)
    if (tam > 500 and prefijo == "MB") or prefijo == "GB" \
            or prefijo == "TB" or (not prefijo and elementos > 10 ** 6):
        if prefijo:
            print(f"La operación requiere de %.2f {prefijo} de espacio en memoria" % tam)
        else:
            cantidad_de_elementos = utilidades.numero_separado_por_comas(elementos)
            print("  No es posible obtener una estimación del espacio en memoria que se requiere.")
            print(f"El alfabeto potenciado tendrá un total de {cantidad_de_elementos} elementos")

        print("  ¿Continuar con la operación?")
        print("1. Si")
        print("2. No, cancelar")
        print("Selecciona una opción")
        if utilidades.seleccionar_opcion(["1", "2"], [False, True]):
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
    
    print("Operación terminanada!")
    print("1. Mostrar nuevo alfabeto")
    print("2. Guardar nuevo alfabeto")
    print("S. Salir")
    print("Selecciona una opción")
    seleccion = utilidades.seleccionar_opcion(["1", "2", "S"])

    if seleccion == "1":
        print("alfabeto_exp = ", alf_exp)
    elif seleccion == "2":
        guardar(alf_exp)

    exit(0)
