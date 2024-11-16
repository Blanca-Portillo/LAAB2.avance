import matplotlib.pyplot as plt
import pandas as pd

class AnalisisCategoria:
    def __init__(self, bd):
        self.bd = bd

    def graficar_distribucion_gastos(self, usuario_id):
        # Realiza la consulta para obtener la distribución de gastos por categoría
        consulta_gastos = 'SELECT categoria, SUM(cantidad) FROM gastos WHERE usuario_id = ? GROUP BY categoria'
        datos_gastos = self.bd.conn.execute(consulta_gastos, (usuario_id,)).fetchall()
        df_gastos = pd.DataFrame(datos_gastos, columns=['Categoria', 'Total'])
        
        # Calcular el total de dinero gastado
        total_gastos = df_gastos['Total'].sum()

        # Realiza la consulta para obtener los ingresos totales
        consulta_ingresos = 'SELECT SUM(cantidad) FROM ingresos WHERE usuario_id = ?'
        total_ingresos = self.bd.conn.execute(consulta_ingresos, (usuario_id,)).fetchone()[0] or 0

        # Calcular el ahorro (ingresos - gastos)
        ahorro = total_ingresos - total_gastos

        # Crear una figura con dos subgráficos (uno para el gráfico de torta y otro para el gráfico de barras)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))  # 1 fila, 2 columnas

        # Gráfico de torta (pie chart) para la distribución de gastos
        ax1.pie(df_gastos['Total'], labels=df_gastos['Categoria'], autopct='%1.1f%%', startangle=90)
        ax1.set_title(f"Distribución de Gastos\nTotal Gastado: ${total_gastos:,.2f}")

        # Gráfico de barras para mostrar Ingresos, Gastos y Ahorro
        categorias = ['Ingresos', 'Gastos', 'Ahorro']
        valores = [total_ingresos, total_gastos, ahorro]
        
        ax2.bar(categorias, valores, color=['green', 'red', 'blue'])
        ax2.set_title("Resumen Financiero")
        ax2.set_ylabel("Monto en $")
        ax2.set_xlabel("Categorías")

        # Ajustar el espacio entre los gráficos
        plt.tight_layout()

        # Mostrar los gráficos
        plt.show()
