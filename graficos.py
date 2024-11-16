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

        # Generar el gráfico de pastel
        wedges, texts, autotexts = ax.pie(df_gastos['Total'], 
                                          labels=df_gastos['Categoria'], 
                                          autopct='%1.1f%%', 
                                          startangle=40, 
                                          colors=plt.cm.Paired.colors,
                                          wedgeprops={"edgecolor": "black"})  # Borde para cada segmento

        # Ajustar las propiedades de las etiquetas y los porcentajes
        for text in texts:
            text.set_fontsize(11)  # Tamaño de la fuente de las etiquetas
            text.set_fontweight('bold')  # Fuente en negrita

        for autotext in autotexts:
            autotext.set_fontsize(11)  # Tamaño de la fuente de los porcentajes
            autotext.set_color('white')  # Color blanco para que se vea bien sobre el pastel

        # Añadir título
        ax.set_title(f"Distribución de Gastos\nTotal Gastado: ${total_gastos:,.2f}")

        # Mostrar el gráfico de pastel
        plt.axis('equal')  # Asegura que el gráfico sea circular
        plt.show()
