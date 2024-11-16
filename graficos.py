

import matplotlib.pyplot as plt
import pandas as pd

class AnalisisCategoria:
    def __init__(self, bd):
        self.bd = bd

    def graficar_distribucion_gastos(self, usuario_id):
        consulta = 'SELECT categoria, SUM(cantidad) FROM gastos WHERE usuario_id = ? GROUP BY categoria'
        datos = self.bd.conn.execute(consulta, (usuario_id,)).fetchall()
        df = pd.DataFrame(datos, columns=['Categoria', 'Total'])
        
        plt.figure(figsize=(8,6))
        plt.pie(df['Total'], labels=df['Categoria'], autopct='%1.1f%%')
        plt.title("Distribución de Gastos por Categoría")
        plt.show()
