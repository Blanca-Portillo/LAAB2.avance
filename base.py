import sqlite3
from datetime import datetime

class BaseDeDatos:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('finanzas.db')
            self.crear_tablas()
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def crear_tablas(self):
        try:
            # Crear la tabla de usuarios
            self.conn.execute(''' 
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY,
                    nombre_usuario TEXT NOT NULL,
                    contraseña TEXT NOT NULL
                );
            ''')
            
            # Crear la tabla de ingresos
            self.conn.execute(''' 
                CREATE TABLE IF NOT EXISTS ingresos (
                    id INTEGER PRIMARY KEY,
                    usuario_id INTEGER NOT NULL,
                    cantidad REAL NOT NULL,
                    fecha TEXT NOT NULL,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                );
            ''')
            
            # Crear la tabla de gastos
            self.conn.execute(''' 
                CREATE TABLE IF NOT EXISTS gastos (
                    id INTEGER PRIMARY KEY,
                    usuario_id INTEGER NOT NULL,
                    cantidad REAL NOT NULL,
                    categoria TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    es_gasto_pequeño BOOLEAN NOT NULL,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                );
            ''')
            
            # Crear la tabla de metas de ahorro
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS metas_ahorro (
                    id INTEGER PRIMARY KEY,
                    usuario_id INTEGER NOT NULL,
                    nombre_meta TEXT NOT NULL,
                    cantidad_meta REAL NOT NULL,
                    fecha_limite TEXT NOT NULL,
                    progreso REAL NOT NULL DEFAULT 0,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                );
            ''')
            
            # Crear la tabla de presupuestos
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS presupuestos (
                    id INTEGER PRIMARY KEY,
                    usuario_id INTEGER NOT NULL,
                    categoria TEXT NOT NULL,
                    monto_asignado REAL NOT NULL,
                    fecha_inicio TEXT NOT NULL,
                    fecha_fin TEXT NOT NULL,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                );
            ''')

            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al crear tablas: {e}")

    def agregar_usuario(self, nombre_usuario, contraseña):
        try:
            # Insertar un nuevo usuario
            self.conn.execute(''' 
                INSERT INTO usuarios (nombre_usuario, contraseña)
                VALUES (?, ?)
            ''', (nombre_usuario, contraseña))
            self.conn.commit()
            print("Usuario registrado correctamente.")
        except sqlite3.Error as e:
            print(f"Error al agregar usuario: {e}")

    def obtener_usuario(self, nombre_usuario):
        try:
            # Obtener un usuario por nombre de usuario
            cursor = self.conn.execute(''' 
                SELECT id, nombre_usuario, contraseña FROM usuarios
                WHERE nombre_usuario = ?
            ''', (nombre_usuario,))
            usuario = cursor.fetchone()
            if usuario:
                return usuario  # Devuelve una tupla (id, nombre_usuario, contraseña)
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error al obtener usuario: {e}")
            return None

    def agregar_ingreso(self, usuario_id, cantidad, fecha):
        try:
            # Validar formato de fecha
            datetime.strptime(fecha, '%Y-%m-%d')  # Cambia el formato según sea necesario
            
            self.conn.execute(''' 
                INSERT INTO ingresos (usuario_id, cantidad, fecha)
                VALUES (?, ?, ?)
            ''', (usuario_id, cantidad, fecha))
            self.conn.commit()
            print("Ingreso registrado correctamente.")
        except ValueError:
            print("Error: La fecha debe estar en el formato YYYY-MM-DD.")
        except sqlite3.Error as e:
            print(f"Error al agregar ingreso: {e}")

    def agregar_gasto(self, usuario_id, cantidad, categoria, es_gasto_pequeño, fecha):
        try:
            # Validar formato de fecha
            datetime.strptime(fecha, '%Y-%m-%d')  # Cambia el formato según sea necesario
            
            self.conn.execute(''' 
                INSERT INTO gastos (usuario_id, cantidad, categoria, es_gasto_pequeño, fecha)
                VALUES (?, ?, ?, ?, ?)
            ''', (usuario_id, cantidad, categoria, es_gasto_pequeño, fecha))
            self.conn.commit()
            print("Gasto registrado correctamente.")
        except ValueError:
            print("Error: La fecha debe estar en el formato YYYY-MM-DD.")
        except sqlite3.Error as e:
            print(f"Error al agregar gasto: {e}")

    def agregar_meta_ahorro(self, usuario_id, nombre_meta, cantidad_meta, fecha_limite):
        try:
            # Validar formato de fecha
            datetime.strptime(fecha_limite, '%Y-%m-%d')
            
            self.conn.execute('''
                INSERT INTO metas_ahorro (usuario_id, nombre_meta, cantidad_meta, fecha_limite)
                VALUES (?, ?, ?, ?)
            ''', (usuario_id, nombre_meta, cantidad_meta, fecha_limite))
            self.conn.commit()
            print("Meta de ahorro registrada correctamente.")
        except ValueError:
            print("Error: La fecha debe estar en el formato YYYY-MM-DD.")
        except sqlite3.Error as e:
            print(f"Error al agregar meta de ahorro: {e}")

    def obtener_metas_ahorro(self, usuario_id):
        try:
            cursor = self.conn.execute('''
                SELECT nombre_meta, cantidad_meta, fecha_limite, progreso FROM metas_ahorro
                WHERE usuario_id = ?
            ''', (usuario_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener metas de ahorro: {e}")
            return []

    def actualizar_progreso_meta(self, usuario_id, meta_id, progreso):
        try:
            self.conn.execute('''
                UPDATE metas_ahorro
                SET progreso = ?
                WHERE usuario_id = ? AND id = ?
            ''', (progreso, usuario_id, meta_id))
            self.conn.commit()
            print("Progreso de la meta actualizado correctamente.")
        except sqlite3.Error as e:
            print(f"Error al actualizar el progreso de la meta: {e}")

    def agregar_presupuesto(self, usuario_id, categoria, monto_asignado, fecha_inicio, fecha_fin):
        try:
            # Validar formato de fecha
            datetime.strptime(fecha_inicio, '%Y-%m-%d')
            datetime.strptime(fecha_fin, '%Y-%m-%d')
            
            self.conn.execute('''
                INSERT INTO presupuestos (usuario_id, categoria, monto_asignado, fecha_inicio, fecha_fin)
                VALUES (?, ?, ?, ?, ?)
            ''', (usuario_id, categoria, monto_asignado, fecha_inicio, fecha_fin))
            self.conn.commit()
            print("Presupuesto registrado correctamente.")
        except ValueError:
            print("Error: La fecha debe estar en el formato YYYY-MM-DD.")
        except sqlite3.Error as e:
            print(f"Error al agregar presupuesto: {e}")

    def obtener_presupuesto(self, usuario_id):
        try:
            cursor = self.conn.execute('''
                SELECT categoria, monto_asignado FROM presupuestos
                WHERE usuario_id = ?
            ''', (usuario_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener el presupuesto: {e}")
            return []

    def obtener_gastos_por_categoria(self, usuario_id):
        try:
            cursor = self.conn.execute('''
                SELECT categoria, SUM(cantidad) FROM gastos
                WHERE usuario_id = ?
                GROUP BY categoria
            ''', (usuario_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener los gastos por categoría: {e}")
            return []

    def cerrar_conexion(self):
        """Cerrar la conexión a la base de datos."""
        if self.conn:
            self.conn.close()

# Ejemplo de uso
bd = BaseDeDatos()

# Agregar un usuario
bd.agregar_usuario("usuario1", "contraseña123")

# Agregar un ingreso
bd.agregar_ingreso(1, 5000, "2024-11-16")

# Agregar un gasto
bd.agregar_gasto(1, 200, "Alimentación", False, "2024-11-16")

# Agregar una meta de ahorro
bd.agregar_meta_ahorro(1, "Fondo de emergencia", 10000, "2025-01-01")

# Agregar un presupuesto
bd.agregar_presupuesto(1, "Alimentación", 500, "2024-11-01", "2024-11-30")

# Obtener gastos por categoría
gastos_categoria = bd.obtener_gastos_por_categoria(1)
print(gastos_categoria)

# Obtener metas de ahorro
metas = bd.obtener_metas_ahorro(1)
print(metas)

# Obtener presupuesto
presupuesto = bd.obtener_presupuesto(1)
print(presupuesto)

# Cerrar conexión
bd.cerrar_conexion()
