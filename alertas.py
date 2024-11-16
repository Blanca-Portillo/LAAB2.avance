
import threading
import time
import sqlite3
from PyQt5.QtWidgets import QMessageBox

class Notificaciones:
    def __init__(self, bd, ventana_principal):
        self.bd = bd
        self.ventana_principal = ventana_principal

    def verificar_gastos_pequeños(self, usuario_id):
        conn = None
        try:
            conn = sqlite3.connect('finanzas.db')
            while True:
                # Consulta de la suma de los gastos pequeños
                consulta = 'SELECT SUM(cantidad) FROM gastos WHERE usuario_id = ? AND es_gasto_pequeño = 1'
                total_gastos_pequeños = conn.execute(consulta, (usuario_id,)).fetchone()[0] or 0

                # Si los gastos pequeños superan el límite, mostrar alerta
                if total_gastos_pequeños > 100:
                    self.mostrar_alerta("¡Cuidado! Los gastos de hormiga superan el límite.")
                time.sleep(60)  # Pausa de 60 segundos entre verificaciones
        except sqlite3.Error as e:
            print(f"Error en la conexión a la base de datos: {e}")
        finally:
            if conn:
                conn.close()  # Asegurarse de cerrar la conexión

    def mostrar_alerta(self, mensaje):
        alerta = QMessageBox()
        alerta.setText(mensaje)
        alerta.setIcon(QMessageBox.Warning)  # Icono de advertencia
        alerta.setWindowTitle("Alerta de Gastos Hormiga")
        alerta.exec_()

    def iniciar_notificaciones(self, usuario_id):
        hilo = threading.Thread(target=self.verificar_gastos_pequeños, args=(usuario_id,))
        hilo.daemon = True  # El hilo se detendrá automáticamente cuando termine el programa
        hilo.start()
