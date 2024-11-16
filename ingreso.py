import datetime
import calendar
from PyQt5.QtWidgets import QApplication, QComboBox, QVBoxLayout, QWidget

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
        return result.fetchone()[0] or 0

    def obtener_gastos_mes(self, usuario_id, mes):
        """Obtiene el total de gastos para un usuario en un mes específico."""
        query = '''
            SELECT SUM(cantidad) 
            FROM gastos 
            WHERE usuario_id = ? AND strftime('%m', fecha) = ?
        '''
        result = self.bd.conn.execute(query, (usuario_id, str(mes).zfill(2)))
        return result.fetchone()[0] or 0

    def obtener_progreso_mensual(self, usuario_id, mes):
        """Obtiene el progreso mensual en forma de ingresos y gastos."""
        ingresos = self.obtener_ingresos_mes(usuario_id, mes)
        gastos = self.obtener_gastos_mes(usuario_id, mes)
        balance = ingresos - gastos
        return {
            "ingresos": ingresos,
            "gastos": gastos,
            "balance": balance
        }

    def obtener_meses_con_registros(self, usuario_id):
        """Obtiene una lista de los meses (en formato numérico) donde hay ingresos o gastos."""
        query = '''
            SELECT DISTINCT strftime('%m', fecha) AS mes
            FROM (
                SELECT fecha FROM ingresos WHERE usuario_id = ?
                UNION ALL
                SELECT fecha FROM gastos WHERE usuario_id = ?
            )
            ORDER BY mes
        '''
        result = self.bd.conn.execute(query, (usuario_id, usuario_id))
        meses = [int(row[0]) for row in result.fetchall()]  # Convierte los meses a enteros
        return meses

# Función para mostrar los meses con registros en consola
def mostrar_meses_consola(ingresos_gastos, usuario_id):
    meses = ingresos_gastos.obtener_meses_con_registros(usuario_id)
    meses_es = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    nombres_meses = [meses_es[mes - 1] for mes in meses]
    print("Meses con registros:", nombres_meses)

# Función para poblar un QComboBox con los meses
def poblar_combo_meses(combo_box, ingresos_gastos, usuario_id):
    meses = ingresos_gastos.obtener_meses_con_registros(usuario_id)
    nombres_meses = [calendar.month_name[mes] for mes in meses]
    combo_box.addItems(nombres_meses)

# Prueba de interfaz con PyQt5
def crear_interfaz(ingresos_gastos, usuario_id):
    app = QApplication([])
    ventana = QWidget()
    ventana.setWindowTitle("Meses con Registros")

    combo_meses = QComboBox()
    poblar_combo_meses(combo_meses, ingresos_gastos, usuario_id)

    layout = QVBoxLayout()
    layout.addWidget(combo_meses)
    ventana.setLayout(layout)
    ventana.show()

    app.exec_()

# Uso del programa (ejemplo)
if __name__ == "__main__":
    class FakeDB:
        """Clase simulada para pruebas."""
        def __init__(self):
            import sqlite3
            self.conn = sqlite3.connect(":memory:")
            self.conn.execute('CREATE TABLE ingresos (usuario_id INTEGER, cantidad REAL, fecha TEXT)')
            self.conn.execute('CREATE TABLE gastos (usuario_id INTEGER, cantidad REAL, categoria TEXT, es_gasto_pequeño INTEGER, fecha TEXT)')

    bd = FakeDB()
    ingresos_gastos = IngresosGastos(bd)

    # Agregar datos de ejemplo
    ingresos_gastos.agregar_ingreso(1, 1000, "15/01/2024")
    ingresos_gastos.agregar_gasto(1, 200, "Alimentos", "20/01/2024", 0)
    ingresos_gastos.agregar_ingreso(1, 1500, "10/02/2024")

    # Mostrar meses en consola
    mostrar_meses_consola(ingresos_gastos, usuario_id=1)

    # Mostrar interfaz gráfica
    crear_interfaz(ingresos_gastos, usuario_id=1)
