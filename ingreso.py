import datetime

class IngresosGastos:
    def __init__(self, bd):
        self.bd = bd

    def validar_fecha(self, fecha):
        """Verifica si la fecha tiene el formato correcto (DD/MM/YYYY)."""
        try:
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

    def agregar_gasto(self, usuario_id, cantidad, categoria, fecha, es_gasto_pequeño):
        if self.validar_fecha(fecha):
            self.bd.conn.execute('''
                INSERT INTO gastos (usuario_id, cantidad, categoria, es_gasto_pequeño, fecha)
                VALUES (?, ?, ?, ?, ?)
            ''', (usuario_id, cantidad, categoria, es_gasto_pequeño, fecha))
            self.bd.conn.commit()
            print("Gasto agregado correctamente.")

    def obtener_ingresos_mes(self, usuario_id, mes):
        """Obtiene el total de ingresos para un usuario en un mes específico."""
        query = '''
            SELECT SUM(cantidad) 
            FROM ingresos 
            WHERE usuario_id = ? AND strftime('%m', fecha) = ?
        '''
        result = self.bd.conn.execute(query, (usuario_id, str(mes).zfill(2)))
        return result.fetchone()[0] or 0  # Devuelve la suma de los ingresos o 0 si no hay ingresos

    def obtener_gastos_mes(self, usuario_id, mes):
        """Obtiene el total de gastos para un usuario en un mes específico."""
        query = '''
            SELECT SUM(cantidad) 
            FROM gastos 
            WHERE usuario_id = ? AND strftime('%m', fecha) = ?
        '''
        result = self.bd.conn.execute(query, (usuario_id, str(mes).zfill(2)))
        return result.fetchone()[0] or 0  # Devuelve la suma de los gastos o 0 si no hay gastos
