import sqlite3
class BaseDeDatos:
    def __init__(self):
        # Inicialización de la conexión a la base de datos
        pass

    def agregar_ingreso(self, usuario_id, cantidad, fecha):
        # Implementación para agregar un ingreso
        print(f"Ingreso agregado: Usuario ID: {usuario_id}, Cantidad: {cantidad}, Fecha: {fecha}")

    def agregar_gasto(self, usuario_id, cantidad, categoria, es_gasto_pequeño, fecha):
        # Implementación para agregar un gasto
        print(f"Gasto agregado: Usuario ID: {usuario_id}, Cantidad: {cantidad}, Categoría: {categoria}, Pequeño: {es_gasto_pequeño}, Fecha: {fecha}")
