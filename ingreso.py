import datetime

class IngresosGastos:
    def __init__(self, bd):
        self.bd = bd

    def validar_fecha(self, fecha):
        """Verifica si la fecha tiene el formato correcto (DD/MM/YYYY)."""
        try:
            # Cambié el formato de fecha de %d/%m/%yyyy a %d/%m/%Y, que es el formato correcto para año.
            datetime.datetime.strptime(fecha, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def agregar_ingreso(self, usuario_id, cantidad, fecha):
        if self.validar_fecha(fecha):
            self.bd.conn.execute('''
                INSERT INTO ingresos (usuario_id, cantidad, fecha)
                VALUES (?, ?, ?)
            ''', (usuario_id, cantidad, fecha))
            self.bd.conn.commit()
            print("Ingreso agregado correctamente.")
        # Si la fecha no es válida, no muestra ningún mensaje ni realiza ninguna acción.

    def agregar_gasto(self, usuario_id, cantidad, categoria, fecha, es_gasto_pequeño):
        if self.validar_fecha(fecha):
            self.bd.conn.execute('''
                INSERT INTO gastos (usuario_id, cantidad, categoria, es_gasto_pequeño, fecha)
                VALUES (?, ?, ?, ?, ?)
            ''', (usuario_id, cantidad, categoria, es_gasto_pequeño, fecha))
            self.bd.conn.commit()
            print("Gasto agregado correctamente.")
        # Si la fecha no es válida, no muestra ningún mensaje ni realiza ninguna acción.
