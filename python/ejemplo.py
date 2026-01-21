# Recorridos de directorios
import os

# 1) Listar nombres rápidamente
# print("Contenido de . :", os.listdir("."))

# 2) Recorrer con información de tipo (más rápido que multiple os.stat)
# with os.scandir(".") as it:
#     for entry in it:
#         tipo = "DIR" if entry.is_dir() else ("FILE" if entry.is_file() else "OTRO")
#         print(f"{entry.name}: {tipo}")

# # 3) Recorrido recursivo del árbol (subcarpetas)
for root, dirs, files in os.walk("."):
    print("Directorio:", root)
    for f in files:
        print("  -", f)