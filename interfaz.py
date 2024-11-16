import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
                             QLineEdit, QDialog, QLabel, QFormLayout, QMessageBox, QTableWidget, QTableWidgetItem)
import re  # Para validar la fecha
from base import BaseDeDatos
from ingreso import IngresosGastos
from graficos import AnalisisCategoria
from alertas import Notificaciones
from datetime import datetime
from PyQt5.QtCore import QTimer  # Importar el temporizador
from PyQt5.QtGui import QPixmap

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

        self.submit_button = QPushButton("Registrar")
        self.cancel_button = QPushButton("Cancelar")
        self.submit_button.clicked.connect(self.submit_data)
        self.cancel_button.clicked.connect(self.reject)

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
        self.setFixedSize(400, 250)  # Establecer un tamaño fijo y no redimensionable

    def submit_data(self):
        try:
            cantidad = float(self.cantidad_input.text())
            fecha = self.fecha_input.text()

            if not self.validar_fecha(fecha):
                QMessageBox.warning(self, "Error", "La fecha no es válida. Debe ser en formato DD/MM/YYYY.")
                return

            if cantidad <= 0:
                QMessageBox.warning(self, "Error", "La cantidad debe ser un número positivo.")
                return

            if self.tipo == "Ingreso":
                self.parent().ingresos_gastos.agregar_ingreso(usuario_id=1, cantidad=cantidad, fecha=fecha)
                QMessageBox.information(self, "Éxito", "Ingreso registrado correctamente.")
            else: 
                categoria = self.categoria_input.text()
                try:
                    es_gasto_pequeño = bool(int(self.es_gasto_pequeño_input.text()))
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
        patron = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
        if re.match(patron, fecha):
            return True
        return False


class ProgresoMensualDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Progreso Mensual")
        self.initUI()

        # Configurar el temporizador
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_progreso)
        self.timer.start(1000)  # Actualización cada 1 segundo

        self.ingresos = 0
        self.gastos = 0

    def initUI(self):
        layout = QVBoxLayout()
        self.progreso_label = QLabel("Cargando progreso mensual...")
        layout.addWidget(self.progreso_label)
        self.setLayout(layout)
        self.setFixedSize(400, 200)  # Establecer un tamaño fijo y no redimensionable

    def mostrar_progreso(self, ingresos, gastos):
        self.ingresos = ingresos
        self.gastos = gastos
        self.progreso_label.setText(f"Ingresos: ${self.ingresos}\nGastos: ${self.gastos}")

    def actualizar_progreso(self):
        mes_actual = datetime.now().month
        self.ingresos = self.parent().ingresos_gastos.obtener_ingresos_mes(usuario_id=1, mes=mes_actual)
        self.gastos = self.parent().ingresos_gastos.obtener_gastos_mes(usuario_id=1, mes=mes_actual)
        self.progreso_label.setText(f"Ingresos: ${self.ingresos}\nGastos: ${self.gastos}")

    def closeEvent(self, event):
        """Detener el temporizador cuando el diálogo se cierre."""
        self.timer.stop()
        super().closeEvent(event)


class AnalisisGastosDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Análisis Detallado de Gastos")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Fecha", "Categoría", "Cantidad", "Gasto Pequeño"])

        # Cargar datos de los gastos
        self.cargar_datos()

        layout.addWidget(self.table)
        self.setLayout(layout)
        self.setFixedSize(600, 400)  # Establecer un tamaño fijo y no redimensionable

    def cargar_datos(self):
        gastos = self.parent().ingresos_gastos.obtener_gastos(usuario_id=1)
        self.table.setRowCount(len(gastos))

        for row, gasto in enumerate(gastos):
            self.table.setItem(row, 0, QTableWidgetItem(gasto["fecha"]))
            self.table.setItem(row, 1, QTableWidgetItem(gasto["categoria"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(gasto["cantidad"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(gasto["es_gasto_pequeno"])))


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
        self.analysis_detail_button = QPushButton("Análisis Detallado de Gastos")
        self.progress_button = QPushButton("Ver Progreso Mensual")

        self.income_button.clicked.connect(self.open_income_dialog)
        self.expense_button.clicked.connect(self.open_expense_dialog)
        self.analysis_button.clicked.connect(self.show_analysis)
        self.analysis_detail_button.clicked.connect(self.show_detailed_analysis)
        self.progress_button.clicked.connect(self.show_monthly_progress)

        layout.addWidget(self.income_button)
        layout.addWidget(self.expense_button)
        layout.addWidget(self.analysis_button)
        layout.addWidget(self.analysis_detail_button)
        layout.addWidget(self.progress_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Establecer imagen de fondo
        background = QPixmap('C:\homero.jpg')  # Ruta de la imagen
        background_label = QLabel(self)
        background_label.setPixmap(background)
        background_label.setGeometry(0, 0, self.width(), self.height())
        background_label.setScaledContents(True)

        self.setStyleSheet("""
            QMainWindow {
                background-color: rgba(255, 255, 255, 150);
            }
            QPushButton {
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
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

        self.setFixedSize(400, 400)  # Establecer un tamaño fijo y no redimensionable

    def open_income_dialog(self):
        dialog = IngresoGastoDialog("Ingreso", self)
        dialog.exec_()

    def open_expense_dialog(self):
        dialog = IngresoGastoDialog("Gasto", self)
        dialog.exec_()

    def show_analysis(self):
        dialog = self.analisis.mostrar_analisis(self)
        dialog.exec_()

    def show_detailed_analysis(self):
        dialog = AnalisisGastosDialog(self)
        dialog.exec_()

    def show_monthly_progress(self):
        dialog = ProgresoMensualDialog(self)
        dialog.mostrar_progreso(self.ingresos_gastos.obtener_ingresos_mes(1, datetime.now().month), 
                                self.ingresos_gastos.obtener_gastos_mes(1, datetime.now().month))
        dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FinanceApp()
    window.show()
    sys.exit(app.exec_())
