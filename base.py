

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
            
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al crear tablas: {e}")

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

    def cerrar_conexion(self):
        """Cerrar la conexión a la base de datos."""
        if self.conn:
            self.conn.close()
