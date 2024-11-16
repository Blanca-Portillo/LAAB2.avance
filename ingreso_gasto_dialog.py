from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QLabel, QPushButton, QMessageBox

class IngresoGastoDialog(QDialog):
    def __init__(self, tipo, parent=None):
        super().__init__(parent)
        self.tipo = tipo
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Registrar {self.tipo}")
        layout = QFormLayout()

        # Campos comunes para Ingreso y Gasto
        self.cantidad_input = QLineEdit()
        self.fecha_input = QLineEdit()   

        layout.addRow(QLabel("Cantidad:"), self.cantidad_input)
        layout.addRow(QLabel("Fecha:"), self.fecha_input)

        # Campos adicionales para Gasto
        if self.tipo == "Gasto":
            self.categoria_input = QLineEdit()
            self.es_gasto_pequeño_input = QLineEdit()
            layout.addRow(QLabel("Categoría:"), self.categoria_input)
            layout.addRow(QLabel("¿Es gasto pequeño? (1=Sí, 0=No):"), self.es_gasto_pequeño_input)

        # Botón de submit
        self.submit_button = QPushButton("Registrar")
        self.submit_button.clicked.connect(self.submit_data)
        layout.addRow(self.submit_button)

        self.setLayout(layout)

    def submit_data(self):
        try:
            cantidad = float(self.cantidad_input.text())
            fecha = self.fecha_input.text() 
            if self.tipo == "Ingreso":
                self.parent().ingresos_gastos.agregar_ingreso(usuario_id=1, cantidad=cantidad, fecha=fecha)
                QMessageBox.information(self, "Éxito", "Ingreso registrado.")
            else:
                categoria = self.categoria_input.text()
                es_gasto_pequeño = bool(int(self.es_gasto_pequeño_input.text()))  
                self.parent().ingresos_gastos.agregar_gasto(usuario_id=1, cantidad=cantidad, 
                                                           categoria=categoria, es_gasto_pequeño=es_gasto_pequeño, fecha=fecha)
                QMessageBox.information(self, "Éxito", "Gasto registrado.")
            self.close()
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingrese valores válidos.")
