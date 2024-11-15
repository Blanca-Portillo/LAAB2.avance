import sqlite3

class BaseDeDatos:
    def __init__(self):
        self.conn = sqlite3.connect('finanzas.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ingresos (
                                id INTEGER PRIMARY KEY, 
                                usuario_id INTEGER, 
                                cantidad REAL, 
                                fecha TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS gastos (
                                id INTEGER PRIMARY KEY, 
                                usuario_id INTEGER, 
                                cantidad REAL, 
                                categoria TEXT, 
                                es_pequeno BOOLEAN, 
                                fecha TEXT)''')
        self.conn.commit()

    def agregar_ingreso(self, usuario_id, cantidad, fecha):
        self.cursor.execute("INSERT INTO ingresos (usuario_id, cantidad, fecha) VALUES (?, ?, ?)", 
                            (usuario_id, cantidad, fecha))
        self.conn.commit()

    def agregar_gasto(self, usuario_id, cantidad, categoria, es_pequeno, fecha):
        self.cursor.execute("INSERT INTO gastos (usuario_id, cantidad, categoria, es_pequeno, fecha) VALUES (?, ?, ?, ?, ?)", 
                            (usuario_id, cantidad, categoria, es_pequeno, fecha))
        self.conn.commit()

    def obtener_ingresos(self, usuario_id):
        self.cursor.execute("SELECT cantidad, fecha FROM ingresos WHERE usuario_id = ?", (usuario_id,))
        return [{'cantidad': row[0], 'fecha': row[1]} for row in self.cursor.fetchall()]

    def obtener_gastos(self, usuario_id):
        self.cursor.execute("SELECT cantidad, categoria, fecha FROM gastos WHERE usuario_id = ?", (usuario_id,))
        return [{'cantidad': row[0], 'categoria': row[1], 'fecha': row[2]} for row in self.cursor.fetchall()]
