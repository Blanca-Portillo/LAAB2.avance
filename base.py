import sqlite3
from datetime import datetime
class BaseDeDatos:
    def __init__(self):
        self.conn = sqlite3.connect('finanzas.db')
        self.create_tables()

    def create_tables(self):
        # Crear tablas de ingresos y gastos
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS ingresos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                cantidad REAL,
                fecha TEXT
            )
        ''')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS gastos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                cantidad REAL,
                categoria TEXT,
                es_gasto_pequeño BOOLEAN,
                fecha TEXT
            )
        ''')

    def obtener_ingresos(self, usuario_id):
        """Obtiene todos los ingresos de un usuario específico."""
        cursor = self.conn.execute('''
            SELECT * FROM ingresos WHERE usuario_id = ?
        ''', (usuario_id,))
        return cursor.fetchall()

    def obtener_gastos(self, usuario_id):
        """Obtiene todos los gastos de un usuario específico."""
        cursor = self.conn.execute('''
            SELECT * FROM gastos WHERE usuario_id = ?
        ''', (usuario_id,))
        return cursor.fetchall()

    def agregar_ingreso(self, usuario_id, cantidad, fecha):
        """Agrega un ingreso a la base de datos."""
        self.conn.execute('''
            INSERT INTO ingresos (usuario_id, cantidad, fecha) 
            VALUES (?, ?, ?)
        ''', (usuario_id, cantidad, fecha))
        self.conn.commit()

    def agregar_gasto(self, usuario_id, cantidad, categoria, es_gasto_pequeño, fecha):
        """Agrega un gasto a la base de datos."""
        self.conn.execute('''
            INSERT INTO gastos (usuario_id, cantidad, categoria, es_gasto_pequeño, fecha) 
            VALUES (?, ?, ?, ?, ?)
        ''', (usuario_id, cantidad, categoria, es_gasto_pequeño, fecha))
        self.conn.commit()
