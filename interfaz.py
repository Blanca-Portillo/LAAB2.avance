import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QDateEdit, QFormLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QDate
from base import BaseDeDatos  # Asegúrate de que BaseDeDatos está correctamente implementada

class FinanzasApp(QWidget):
    def __init__(self):
        super().__init__()

        self.db = BaseDeDatos()
        self.setWindowTitle('Gestión de Finanzas Personales')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.iniciar_interfaz()

    def iniciar_interfaz(self):
        # Título
        self.titulo = QLabel('Bienvenido a la Gestión de Finanzas Personales')
        self.layout.addWidget(self.titulo)

        # Formulario de ingresos
        self.form_ingresos = QFormLayout()
        self.campo_cantidad_ingreso = QLineEdit()
        self.campo_fecha_ingreso = QDateEdit(calendarPopup=True)
        self.campo_fecha_ingreso.setDate(QDate.currentDate())
        self.form_ingresos.addRow('Cantidad de Ingreso:', self.campo_cantidad_ingreso)
        self.form_ingresos.addRow('Fecha del Ingreso:', self.campo_fecha_ingreso)

        self.boton_agregar_ingreso = QPushButton('Agregar Ingreso')
        self.boton_agregar_ingreso.clicked.connect(self.agregar_ingreso)
        self.layout.addLayout(self.form_ingresos)
        self.layout.addWidget(self.boton_agregar_ingreso)

        # Formulario de gastos
        self.form_gastos = QFormLayout()
        self.campo_cantidad_gasto = QLineEdit()
        self.campo_categoria_gasto = QLineEdit()
        self.campo_fecha_gasto = QDateEdit(calendarPopup=True)
        self.campo_fecha_gasto.setDate(QDate.currentDate())
        self.campo_gasto_pequeño = QLineEdit()  # Es un campo booleano simple para ejemplo
        self.form_gastos.addRow('Cantidad de Gasto:', self.campo_cantidad_gasto)
        self.form_gastos.addRow('Categoría de Gasto:', self.campo_categoria_gasto)
        self.form_gastos.addRow('Fecha de Gasto:', self.campo_fecha_gasto)
        self.form_gastos.addRow('¿Es Gasto Pequeño? (True/False):', self.campo_gasto_pequeño)

        self.boton_agregar_gasto = QPushButton('Agregar Gasto')
        self.boton_agregar_gasto.clicked.connect(self.agregar_gasto)
        self.layout.addLayout(self.form_gastos)
        self.layout.addWidget(self.boton_agregar_gasto)

        # Tabla de registros
        self.tabla = QTableWidget()
        self.layout.addWidget(self.tabla)

    def agregar_ingreso(self):
        try:
            cantidad = float(self.campo_cantidad_ingreso.text())
            fecha = self.campo_fecha_ingreso.date().toString('yyyy-MM-dd')
            self.db.agregar_ingreso(1, cantidad, fecha)  # 1 es el id del usuario
            self.mostrar_datos()
        except ValueError:
            print("Por favor ingresa una cantidad válida.")

    def agregar_gasto(self):
        try:
            cantidad = float(self.campo_cantidad_gasto.text())
            categoria = self.campo_categoria_gasto.text()
            fecha = self.campo_fecha_gasto.date().toString('yyyy-MM-dd')
            es_pequeño = self.campo_gasto_pequeño.text() == 'True'
            self.db.agregar_gasto(1, cantidad, categoria, es_pequeño, fecha)  # 1 es el id del usuario
            self.mostrar_datos()
        except ValueError:
            print("Por favor ingresa datos válidos para el gasto.")

    def mostrar_datos(self):
        self.tabla.clear()
        self.tabla.setRowCount(0)
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(['Tipo', 'Cantidad', 'Fecha', 'Categoría'])

        # Obtener datos de la base de datos
        ingresos = self.db.obtener_ingresos(1)  # Método que debes implementar
        gastos = self.db.obtener_gastos(1)  # Método que debes implementar

        # Mostrar los datos de ingresos
        for ingreso in ingresos:
            row_position = self.tabla.rowCount()
            self.tabla.insertRow(row_position)
            self.tabla.setItem(row_position, 0, QTableWidgetItem("Ingreso"))
            self.tabla.setItem(row_position, 1, QTableWidgetItem(str(ingreso['cantidad'])))
            self.tabla.setItem(row_position, 2, QTableWidgetItem(ingreso['fecha']))
            self.tabla.setItem(row_position, 3, QTableWidgetItem("N/A"))

        # Mostrar los datos de gastos
        for gasto in gastos:
            row_position = self.tabla.rowCount()
            self.tabla.insertRow(row_position)
            self.tabla.setItem(row_position, 0, QTableWidgetItem("Gasto"))
            self.tabla.setItem(row_position, 1, QTableWidgetItem(str(gasto['cantidad'])))
            self.tabla.setItem(row_position, 2, QTableWidgetItem(gasto['fecha']))
            self.tabla.setItem(row_position, 3, QTableWidgetItem(gasto['categoria']))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = FinanzasApp()
    ventana.show()
    sys.exit(app.exec_())
