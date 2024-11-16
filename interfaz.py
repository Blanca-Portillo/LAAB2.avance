import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
                             QLineEdit, QDialog, QLabel, QFormLayout, QMessageBox)
import re  # Para validar la fecha
from base import BaseDeDatos
from ingreso import IngresosGastos
from graficos import AnalisisCategoria
from alertas import Notificaciones
from datetime import datetime

class IngresoGastoDialog(QDialog):
    def __init__(self, tipo, parent=None):
        super().__init__(parent)
        self.tipo = tipo
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Registrar {self.tipo}")
        layout = QFormLayout()

        self.cantidad_input = QLineEdit()
        self.fecha_input = QLineEdit()   

        layout.addRow(QLabel("Cantidad:"), self.cantidad_input)
        layout.addRow(QLabel("Fecha (DD/MM/YYYY):"), self.fecha_input)

        if self.tipo == "Gasto":
            self.categoria_input = QLineEdit()
            self.es_gasto_pequeño_input = QLineEdit()
            layout.addRow(QLabel("Categoría:"), self.categoria_input)
            layout.addRow(QLabel("¿Es gasto pequeño? (1=Sí, 0=No):"), self.es_gasto_pequeño_input)

        # Botones de acción
        self.submit_button = QPushButton("Registrar")
        self.cancel_button = QPushButton("Cancelar")
        self.submit_button.clicked.connect(self.submit_data)
        self.cancel_button.clicked.connect(self.reject)  # Cancelar acción

        layout.addRow(self.submit_button, self.cancel_button)

        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background-color: rgba(255, 255, 255, 200);
                border-radius: 10px;
                padding: 10px;
            }
            QLabel {
                font-size: 16px;
                color: #333;
            }
            QLineEdit {
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)
        self.setFixedSize(400, 250)

    def submit_data(self):
        try:
            cantidad = float(self.cantidad_input.text())
            fecha = self.fecha_input.text()

            # Validar la fecha
            if not self.validar_fecha(fecha):
                QMessageBox.warning(self, "Error", "La fecha no es válida. Debe ser en formato DD/MM/YYYY.")
                return  # No guardar los datos si la fecha es incorrecta

            # Validar que la cantidad sea un número positivo
            if cantidad <= 0:
                QMessageBox.warning(self, "Error", "La cantidad debe ser un número positivo.")
                return

            if self.tipo == "Ingreso":
                self.parent().ingresos_gastos.agregar_ingreso(usuario_id=1, cantidad=cantidad, fecha=fecha)
                QMessageBox.information(self, "Éxito", "Ingreso registrado correctamente.")
            else: 
                categoria = self.categoria_input.text()
                try:
                    es_gasto_pequeño = bool(int(self.es_gasto_pequeño_input.text()))  # Validar 1 o 0
                except ValueError:
                    QMessageBox.warning(self, "Error", "Por favor, ingrese 1 o 0 para el campo de gasto pequeño.")
                    return
                self.parent().ingresos_gastos.agregar_gasto(usuario_id=1, cantidad=cantidad, 
                                                             categoria=categoria, es_gasto_pequeño=es_gasto_pequeño, fecha=fecha)
                QMessageBox.information(self, "Éxito", "Gasto registrado correctamente.")
            self.close()
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingrese valores válidos para cantidad.")

    def validar_fecha(self, fecha):
        # Validar fecha en formato DD/MM/YYYY
        patron = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
        if re.match(patron, fecha):
            return True
        return False


class ProgresoMensualDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Progreso Mensual")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Aquí es donde mostrarás el progreso mensual (ingresos y gastos)
        self.progreso_label = QLabel("Cargando progreso mensual...")
        layout.addWidget(self.progreso_label)

        self.setLayout(layout)
        self.setFixedSize(400, 200)

    def mostrar_progreso(self, ingresos, gastos):
        self.progreso_label.setText(f"Ingresos: ${ingresos}\nGastos: ${gastos}")


class FinanceApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.bd = BaseDeDatos()
        self.ingresos_gastos = IngresosGastos(self.bd)
        self.analisis = AnalisisCategoria(self.bd)
        self.notifications = Notificaciones(self.bd, self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sistema de Administración y Ahorro de Dinero")
        layout = QVBoxLayout()

        # Botones para registrar ingresos, gastos, ver análisis y progreso mensual
        self.income_button = QPushButton("Registrar Ingreso")
        self.expense_button = QPushButton("Registrar Gasto")
        self.analysis_button = QPushButton("Análisis de Gastos")
        self.progress_button = QPushButton("Ver Progreso Mensual")

        self.income_button.clicked.connect(self.open_income_dialog)
        self.expense_button.clicked.connect(self.open_expense_dialog)
        self.analysis_button.clicked.connect(self.show_analysis)
        self.progress_button.clicked.connect(self.show_monthly_progress)

        layout.addWidget(self.income_button)
        layout.addWidget(self.expense_button)
        layout.addWidget(self.analysis_button)
        layout.addWidget(self.progress_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setStyleSheet("""
            QMainWindow {
                background-image: url('C:\homero.jpg');  
                background-position: center;
                background-repeat: no-repeat;
                background-size: cover;
            }
            QPushButton {
                background-color: rgba(98, 0, 234, 0.8);
                color: white;
                border: none;
                padding: 15px;
                font-size: 18px;
                border-radius: 5px;
                margin-bottom: 15px;
            }
            QPushButton:hover {
                background-color: rgba(55, 0, 179, 0.8);
            }
            QPushButton:pressed {
                background-color: rgba(3, 218, 197, 0.8);
            }
        """)

        self.setFixedSize(600, 400)

        # Iniciar las notificaciones
        self.notifications.iniciar_notificaciones(usuario_id=1)

    def open_income_dialog(self):
        dialog = IngresoGastoDialog("Ingreso", self)
        dialog.exec_()

    def open_expense_dialog(self):
        dialog = IngresoGastoDialog("Gasto", self)
        dialog.exec_()

    def show_analysis(self):
        self.analisis.graficar_distribucion_gastos(usuario_id=1)

    def show_monthly_progress(self):
        dialog = ProgresoMensualDialog(self)
        
        # Aquí obtenemos los ingresos y gastos del mes actual
        mes_actual = datetime.now().month
        ingresos = self.ingresos_gastos(usuario_id=1, mes=mes_actual)
        gastos = self.ingresos_gastos(usuario_id=1, mes=mes_actual)
        
        dialog.mostrar_progreso(ingresos, gastos)
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = FinanceApp()
    mainWindow.show()
    sys.exit(app.exec_())
