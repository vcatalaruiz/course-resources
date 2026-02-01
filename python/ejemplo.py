# ---------------------------------------------
# Ejemplo 3.8: tamaño de objetos y límites de recursión
# ---------------------------------------------
import sys

# Medimos tamaños de objetos básicos.
print("sizeof(int):", sys.getsizeof(42))
print("sizeof(str vacía):", sys.getsizeof(""))
print("sizeof(lista vacía):", sys.getsizeof([]))

# Demostramos que getsizeof de una lista no suma el tamaño de sus elementos.
lista = [1, 2, 3, 4, 5]
tam_lista = sys.getsizeof(lista)
tam_elementos = sum(sys.getsizeof(x) for x in lista)
print(f"Tamaño lista: {tam_lista} bytes; elementos: {tam_elementos} bytes (no incluidos).")

# Límite de recursión actual (número máximo de llamadas recursivas antes de lanzar RecursionError).
print("Límite de recursión:", sys.getrecursionlimit())