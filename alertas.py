

import threading
import time
import sqlite3
from PyQt5.QtWidgets import QMessageBox

class Notificaciones:
    def __init__(self, bd, ventana_principal):
        self.bd = bd
        self.ventana_principal = ventana_principal

    def verificar_gastos_pequeños(self, usuario_id):
       
        conn = sqlite3.connect('finanzas.db')
        while True:
            consulta = 'SELECT SUM(cantidad) FROM gastos WHERE usuario_id = ? AND es_gasto_pequeño = 1'
            total_gastos_pequeños = conn.execute(consulta, (usuario_id,)).fetchone()[0] or 0
            if total_gastos_pequeños > 100:
                self.mostrar_alerta("¡Cuidado! Los gastos de hormiga superan el límite.")
            time.sleep(60)
        conn.close()  

    def mostrar_alerta(self, mensaje):
        alerta = QMessageBox()
        alerta.setText(mensaje)
        alerta.exec_()

    def iniciar_notificaciones(self, usuario_id):
        hilo = threading.Thread(target=self.verificar_gastos_pequeños, args=(usuario_id,))
        hilo.daemon = True  
        hilo.start()
