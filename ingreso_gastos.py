class IngresosGastos:
    def __init__(self, base_de_datos):
        self.base_de_datos = base_de_datos

    def agregar_ingreso(self, usuario_id, cantidad, fecha):
        # Lógica para agregar un ingreso
        self.base_de_datos.guardar_ingreso(usuario_id, cantidad, fecha)

    def agregar_gasto(self, usuario_id, cantidad, categoria, es_gasto_pequeño, fecha):
        # Lógica para agregar un gasto
        self.base_de_datos.guardar_gasto(usuario_id, cantidad, categoria, es_gasto_pequeño, fecha)
