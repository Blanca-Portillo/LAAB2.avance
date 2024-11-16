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

        # Crear el gráfico de pastel (pie chart) para la distribución de gastos
        fig, ax = plt.subplots(figsize=(10, 10))

        ax.pie(df_gastos['Total'], labels=df_gastos['Categoria'], autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        ax.set_title(f"Distribución de Gastos\nTotal Gastado: ${total_gastos:,.2f}")

        # Mostrar el gráfico de pastel
        plt.axis('equal')  # Asegura que el gráfico sea circular
        plt.show()
