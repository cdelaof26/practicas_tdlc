import utilidades
import re


alfabeto: list[str]
l1: list[str]
l2: list[str]


def combinar_lenguajes(_l1: list[str], _l2: list[str]) -> list[str]:
    l3 = []
    for p1 in _l1:
        for p2 in _l2:
            l3.append(p1 + p2)

    return l3


if __name__ == "__main__":
    print("  Práctica 3 - Operaciones con alfabetos")
    print(" De La O Flores Cristopher - 4CV1\n")

    alfabeto, _ = utilidades.nuevo_alfabeto(True)
    l1, l2 = utilidades.obtener_lenguaje(alfabeto, "l1"), utilidades.obtener_lenguaje(alfabeto, "l2")

    print("L1 U L2:", l1 + l2)
    print("L1*L2:", combinar_lenguajes(l1, l2), "\n")

    utilidades.set_potencia(["l1", "l2"], [l1, l2], "l")

    l_a_reflejar = utilidades.seleccionar_opcion_en_lista(["l1", "l2"], [l1, l2], "Ingresa el lenguaje a reflejar")
    print("L^-1:", [p[::1] for p in l_a_reflejar])
