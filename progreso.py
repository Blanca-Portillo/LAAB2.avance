from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton

class ProgresoMensualDialog(QDialog):
    def __init__(self, usuario_id, mes, ingresos_gastos, parent=None):
        super().__init__(parent)
        self.usuario_id = usuario_id
        self.mes = mes
        self.ingresos_gastos = ingresos_gastos
        self.setWindowTitle("Progreso Mensual")
        self.setFixedSize(400, 200)

        self.layout = QVBoxLayout()

        self.ingresos_label = QLabel("Ingresos: $0")
        self.gastos_label = QLabel("Gastos: $0")
        self.progreso_label = QLabel("Progreso del mes: $0")

        # Obtener los datos de ingresos y gastos
        self.ingresos = self.ingresos_gastos(self.usuario_id, self.mes)
        self.gastos = self.ingresos_gastos(self.usuario_id, self.mes)
        self.progreso = self.ingresos - self.gastos

        # Mostrar los datos en las etiquetas
        self.ingresos_label.setText(f"Ingresos: ${self.ingresos}")
        self.gastos_label.setText(f"Gastos: ${self.gastos}")
        self.progreso_label.setText(f"Progreso del mes: ${self.progreso}")

        self.layout.addWidget(self.ingresos_label)
        self.layout.addWidget(self.gastos_label)
        self.layout.addWidget(self.progreso_label)

        self.close_button = QPushButton("Cerrar")
        self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)
