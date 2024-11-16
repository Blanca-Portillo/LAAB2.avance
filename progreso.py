import matplotlib.pyplot as plt
import pandas as pd

class VistaProgresoMensual:
    def __init__(self, bd):
        self.bd = bd

    def graficar_progreso_mensual(self, usuario_id):
        # Realiza la consulta para obtener los ingresos mensuales por usuario
        consulta_ingresos = '''
            SELECT strftime('%Y-%m', fecha) AS mes, SUM(cantidad) 
            FROM ingresos 
            WHERE usuario_id = ? 
            GROUP BY mes
        '''
        datos_ingresos = self.bd.conn.execute(consulta_ingresos, (usuario_id,)).fetchall()
        
        # Realiza la consulta para obtener los gastos mensuales por usuario
        consulta_gastos = '''
            SELECT strftime('%Y-%m', fecha) AS mes, SUM(cantidad) 
            FROM gastos 
            WHERE usuario_id = ? 
            GROUP BY mes
        '''
        datos_gastos = self.bd.conn.execute(consulta_gastos, (usuario_id,)).fetchall()

        # Convertir los datos en DataFrames para trabajar con ellos fácilmente
        df_ingresos = pd.DataFrame(datos_ingresos, columns=['Mes', 'Ingresos'])
        df_gastos = pd.DataFrame(datos_gastos, columns=['Mes', 'Gastos'])

        # Unir ambos DataFrames por la columna 'Mes'
        df = pd.merge(df_ingresos, df_gastos, on='Mes', how='outer').fillna(0)

        # Ordenar los datos por mes
        df['Mes'] = pd.to_datetime(df['Mes'])
        df = df.sort_values(by='Mes')

        # Crear el gráfico de barras
        plt.figure(figsize=(10, 6))

        # Gráfico de barras para Ingresos y Gastos
        plt.bar(df['Mes'] - pd.Timedelta(days=15), df['Ingresos'], width=15, label='Ingresos', color='green', alpha=0.7)
        plt.bar(df['Mes'] + pd.Timedelta(days=15), df['Gastos'], width=15, label='Gastos', color='red', alpha=0.7)

        # Etiquetas y título
        plt.xlabel('Mes')
        plt.ylabel('Monto en $')
        plt.title('Progreso Mensual de Ingresos y Gastos')
        plt.xticks(df['Mes'], df['Mes'].dt.strftime('%b %Y'), rotation=45)
        plt.legend()

        # Mostrar el gráfico
        plt.tight_layout()
        plt.show()
