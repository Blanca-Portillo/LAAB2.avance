import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
                             QLineEdit, QDialog, QLabel, QFormLayout, QMessageBox, QProgressBar)
from PyQt5.QtCore import QTimer, Qt
from datetime import datetime
import time  # Simular procesamiento
import re  # Para validar la fecha
from base import BaseDeDatos
from ingreso import IngresosGastos
from graficos import AnalisisCategoria
from alertas import Notificaciones

class ProgresoMensualDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Progreso Mensual")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.progreso_label = QLabel("Preparando datos...")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.progreso_label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)
        self.setFixedSize(400, 200)

    def actualizar_progreso(self, porcentaje):
        self.progress_bar.setValue(porcentaje)

    def mostrar_progreso_final(self, ingresos, gastos):
        self.progreso_label.setText(f"Ingresos: ${ingresos:.2f}\nGastos: ${gastos:.2f}")


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
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 15px;
                font-size: 18px;
                border-radius: 5px;
                margin-bottom: 15px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)

        self.setFixedSize(600, 400)
        self.notifications.iniciar_notificaciones(usuario_id=1)

    def open_income_dialog(self):
        dialog = IngresosGastos("Ingreso", self)
        dialog.exec_()

    def open_expense_dialog(self):
        dialog = IngresosGastos("Gasto", self)
        dialog.exec_()

    def show_analysis(self):
        self.analisis.graficar_distribucion_gastos(usuario_id=1)

    def show_monthly_progress(self):
        dialog = ProgresoMensualDialog(self)

        def proceso_simulado():
            for i in range(0, 101, 10):
                time.sleep(0.1)  # Simula procesamiento
                dialog.actualizar_progreso(i)
            mes_actual = datetime.now().month
            ingresos = self.ingresos_gastos.obtener_ingresos_mes(usuario_id=1, mes=mes_actual)
            gastos = self.ingresos_gastos.obtener_gastos_mes(usuario_id=1, mes=mes_actual)
            dialog.mostrar_progreso_final(ingresos, gastos)

        QTimer.singleShot(100, proceso_simulado)
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = FinanceApp()
    mainWindow.show()
    sys.exit(app.exec_())
