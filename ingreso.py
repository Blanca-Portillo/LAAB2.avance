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
        """Agrega un ingreso a la base de datos si la fecha es válida."""
        if self.validar_fecha(fecha):
            try:
                self.bd.conn.execute('''INSERT INTO ingresos (usuario_id, cantidad, fecha)
                                         VALUES (?, ?, ?)''', (usuario_id, cantidad, fecha))
                self.bd.conn.commit()
                print("Ingreso agregado correctamente.")
            except Exception as e:
                print(f"Error al agregar ingreso: {e}")

    def agregar_gasto(self, usuario_id, cantidad, categoria, fecha, es_gasto_pequeño):
        """Agrega un gasto a la base de datos si la fecha es válida."""
        if self.validar_fecha(fecha):
            try:
                self.bd.conn.execute('''INSERT INTO gastos (usuario_id, cantidad, categoria, es_gasto_pequeño, fecha)
                                         VALUES (?, ?, ?, ?, ?)''', (usuario_id, cantidad, categoria, es_gasto_pequeño, fecha))
                self.bd.conn.commit()
                print("Gasto agregado correctamente.")
            except Exception as e:
                print(f"Error al agregar gasto: {e}")

    def obtener_total_mes(self, usuario_id, mes, tipo):
        """Obtiene el total de ingresos o gastos para un usuario en un mes específico."""
        tabla = 'ingresos' if tipo == 'ingreso' else 'gastos'
        query = f"SELECT SUM(cantidad) FROM {tabla} WHERE usuario_id = ? AND strftime('%m', fecha) = ?"
        result = self.bd.conn.execute(query, (usuario_id, str(mes).zfill(2)))
        return result.fetchone()[0] or 0

    def obtener_progreso_mensual(self, usuario_id, mes):
        """Obtiene el progreso mensual en forma de ingresos y gastos."""
        ingresos = self.obtener_total_mes(usuario_id, mes, 'ingreso')
        gastos = self.obtener_total_mes(usuario_id, mes, 'gasto')
        balance = ingresos - gastos
        return {
            "ingresos": ingresos,
            "gastos": gastos,
            "balance": balance
        }

    def obtener_desglose_gastos(self, usuario_id, mes):
        """Obtiene un desglose de los gastos por categoría."""
        query = '''
            SELECT categoria, SUM(cantidad) 
            FROM gastos 
            WHERE usuario_id = ? AND strftime('%m', fecha) = ?
            GROUP BY categoria
        '''
        result = self.bd.conn.execute(query, (usuario_id, str(mes).zfill(2)))
        return result.fetchall()  # Devuelve el desglose de gastos por categoría
