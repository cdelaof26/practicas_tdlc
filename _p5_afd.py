
if __name__ == "__main__":
    print("  -- Programa realizado en clase --")
    print("AFD que válida a*|b+c*")
    print("Ingresa la palabra a validar")
    estado = 0
    alfabeto = [c for c in "abc"]
    palabra = input("> ")
    for c in palabra:
        if c not in alfabeto:
            raise ValueError("El carácter %a no es parte del alfabeto" % c)

        if estado == 0:
            estado = 1 if c == "a" else 2 if c == "b" else 4
        elif estado == 1:
            estado = 1 if c == "a" else 4
        elif estado == 2:
            estado = 2 if c == "b" else 3 if c == "c" else 4
        elif estado == 3:
            estado = 3 if c == "c" else 4

    print(f"La palabra %a es " % palabra + ("válida" if estado != 4 else "inválida"))
