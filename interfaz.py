

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from ingreso_gasto_dialog import IngresoGastoDialog
from base import BaseDeDatos
from ingreso_gastos import IngresosGastos
from graficos import AnalisisCategoria
from alertas import Notificaciones

class FinanceApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Inicializar la base de datos y clases asociadas
        self.bd = BaseDeDatos()
        self.ingresos_gastos = IngresosGastos(self.bd)
        self.analisis = AnalisisCategoria(self.bd)
        self.notifications = Notificaciones(self.bd, self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sistema de Administración y Ahorro de Dinero")
        layout = QVBoxLayout()

        # Botones para registrar ingresos, gastos y mostrar análisis
        self.income_button = QPushButton("Registrar Ingreso")
        self.expense_button = QPushButton("Registrar Gasto")
        self.analysis_button = QPushButton("Análisis de Gastos")

        # Conectar botones con las funciones correspondientes
        self.income_button.clicked.connect(self.open_income_dialog)
        self.expense_button.clicked.connect(self.open_expense_dialog)
        self.analysis_button.clicked.connect(self.show_analysis)

        # Agregar los botones al layout
        layout.addWidget(self.income_button)
        layout.addWidget(self.expense_button)
        layout.addWidget(self.analysis_button)

        # Configuración de la ventana principal
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Iniciar las notificaciones para el usuario
        self.notifications.iniciar_notificaciones(usuario_id=1)

    def open_income_dialog(self):
        dialog = IngresoGastoDialog("Ingreso", self)
        dialog.exec_()

    def open_expense_dialog(self):
        dialog = IngresoGastoDialog("Gasto", self)
        dialog.exec_()

    def show_analysis(self):
        # Mostrar análisis gráfico de los gastos por categorías
        self.analisis.graficar_distribucion_gastos(usuario_id=1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = FinanceApp()
    mainWindow.show()
    sys.exit(app.exec_())
