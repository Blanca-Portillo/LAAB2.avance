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

        # Crear el gráfico de torta para la distribución de los gastos
        plt.figure(figsize=(8,6))
        plt.pie(df_gastos['Total'], labels=df_gastos['Categoria'], autopct='%1.1f%%')
        
        # Agregar título con el total de dinero gastado y el ahorro
        plt.title(f"Distribución de Gastos por Categoría\nTotal Gastado: ${total_gastos:,.2f} | Ahorro: ${ahorro:,.2f}")
        
        # Mostrar la gráfica
        plt.show()
