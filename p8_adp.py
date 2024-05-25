
if __name__ == "__main__":
    print("  Práctica 8 - Autómata de pila")
    print("AFD que válida a^n·b^n | n > 0")
    print(" De La O Flores Cristopher - 4CV1\n")

    # Tenemos 3 estados:
    # q0: inicial, con 'a' nos trasladamos a q0, con 'b' a q1
    #   - Pop: epsilon
    #   - Push: 'a'
    #
    # Transición q0 -> q1:
    #   - Pop: 'a'
    #   - Push: epsilon
    #   - Si la pila está vacía antes del pop, nos trasladamos a q3
    #
    # q1: final, con 'a' nos trasladamos a q3, con 'b' a q1
    #   - Pop: 'a'
    #   - Push: epsilon
    #   - Si la pila no queda vacía, nos trasladamos a q3.
    #   - Si la pila está vacía antes del pop, nos trasladamos a q3
    # q3: error, con 'a' y 'b' nos trasladamos q3

    print("Ingresa la palabra a validar")
    pila = []
    estado = 0
    alfabeto = ["a", "b"]
    palabra = input("> ")
    for c in palabra:
        if c not in alfabeto:
            raise ValueError("El carácter %a no es parte del alfabeto" % c)

        es_entrada_a = c == "a"
        if estado == 0:
            if es_entrada_a:
                pila.append(c)
                continue

            estado = 1 if pila else 2
            if estado == 1:
                pila.pop()
        elif estado == 1:
            if es_entrada_a or not pila:
                estado = 2
                continue

            pila.pop()

    la_palabra_es_valida = estado == 1 and not pila

    print(f"La palabra %a es " % palabra + ("válida" if la_palabra_es_valida else "inválida"))
