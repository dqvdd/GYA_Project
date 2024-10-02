import streamlit as st # type: ignore
import pandas as pd # type: ignore
from sqlalchemy import create_engine # type: ignore
import matplotlib.pyplot as plt # type: ignore
import matplotlib.dates as mdates # type: ignore
import plotly.express as px # type: ignore
import time
import seaborn as sns # type: ignore
import matplotlib.ticker as mtick # type: ignore
import warnings # type: ignore

# Configuración de la conexión
user = 'root'
password = '708090' #por defecto es admin
host = 'localhost'
database = 'db_superstore'
connection_string = f'mysql+mysqlconnector://{user}:{password}@{host}/{database}'
engine = create_engine(connection_string)


# Función para cargar datos Orders
def load_data_Orders():
    return pd.read_sql('SELECT * FROM `Orders`', con=engine)

# Función para cargar datos Returns
def load_data_Returns():
    return pd.read_sql('SELECT * FROM `Returns`', con=engine)


# Título de la aplicación
st.title('Análisis de Datos de Global SuperStore')

# Cargar datos
df_Orders = load_data_Orders()
df_Returns = load_data_Returns()

# Convertir la columna de fecha a datetime
df_Orders['Order_Date'] = pd.to_datetime(df_Orders['Order_Date'])
# Extraer año y mes
df_Orders['Year'] = df_Orders['Order_Date'].dt.year
df_Orders['Month'] = df_Orders['Order_Date'].dt.strftime('%Y-%m')

#### SEGMENTADORES ####
# Segmentador de años
years = df_Orders['Year'].unique().tolist()
years.insert(0, "Todos")  # Añadir "Todos" como opción al inicio
year_to_filter = st.sidebar.selectbox('Selecciona el año', options=years)

# Segmentador para Category, SubCategory, Market, Segment, Region
categories = df_Orders['Category'].unique().tolist()
categories.insert(0, "Todos")
category = st.sidebar.selectbox('Selecciona la Categoría', options=categories)

subcategories = df_Orders['SubCategory'].unique().tolist()
subcategories.insert(0, "Todos")
subcategory = st.sidebar.selectbox('Selecciona la SubCategoría', options=subcategories)

markets = df_Orders['Market'].unique().tolist()
markets.insert(0, "Todos")
market = st.sidebar.selectbox('Selecciona el Mercado', options=markets)

segments = df_Orders['Segment'].unique().tolist()
segments.insert(0, "Todos")
segment = st.sidebar.selectbox('Selecciona el Segmento', options=segments)

regions = df_Orders['Region'].unique().tolist()
regions.insert(0, "Todos")
region = st.sidebar.selectbox('Selecciona la Región', options=regions)

# Filtrar los datos según las selecciones, teniendo en cuenta la opción "Todos"
filtered_data = df_Orders.copy()

if year_to_filter != "Todos":
    filtered_data = filtered_data[filtered_data['Year'] == year_to_filter]

if category != "Todos":
    filtered_data = filtered_data[filtered_data['Category'] == category]

if subcategory != "Todos":
    filtered_data = filtered_data[filtered_data['SubCategory'] == subcategory]

if market != "Todos":
    filtered_data = filtered_data[filtered_data['Market'] == market]

if segment != "Todos":
    filtered_data = filtered_data[filtered_data['Segment'] == segment]

if region != "Todos":
    filtered_data = filtered_data[filtered_data['Region'] == region]

#### FIN SEGMENTADORES ####

# Contenedor para la tabla y gráficos
table_placeholder = st.empty()
chart_placeholder_1 = st.empty()
chart_placeholder_2 = st.empty()
chart_placeholder_3 = st.empty()
chart_placeholder_4 = st.empty()
chart_placeholder_5 = st.empty()
chart_placeholder_6 = st.empty()
chart_placeholder_7 = st.empty()
chart_placeholder_8 = st.empty()
chart_placeholder_9 = st.empty()
chart_placeholder_10 = st.empty()
chart_placeholder_11 = st.empty()
chart_placeholder_12 = st.empty()
chart_placeholder_13 = st.empty()
chart_placeholder_14 = st.empty()
chart_placeholder_15 = st.empty()


def suppress_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning)

# Función para mostrar la tabla
def show_table(df_Orders):
    table_placeholder.empty()  # Limpiar el contenedor de la tabla
    with table_placeholder.container():
        st.subheader('Datos de la Tabla Orders')
        st.write(f'Cantidad de registros: {len(filtered_data)}')  # Mostrar cantidad de datos
        st.write(filtered_data.head())  # Mostrar los primeros registros


def show_sales_chart(df_Orders):
    suppress_warnings()
    chart_placeholder_1.empty()  # Limpiar el contenedor de la gráfica

    with chart_placeholder_1.container():
        st.title('Ventas Mensuales por año')

        # Asegurarse que 'Order_Date' es tipo datetime
        filtered_data['Order_Date'] = pd.to_datetime(filtered_data['Order_Date'])

        # Extraer año y mes de la fecha
        filtered_data['Month'] = filtered_data['Order_Date'].dt.to_period('M')

        # Agrupar por mes y sumar las ventas
        monthly_sales = filtered_data.groupby(filtered_data['Month'])['Sales'].sum().reset_index()
        monthly_sales['Month'] = monthly_sales['Month'].dt.to_timestamp()  # Convertir PeriodIndex a Timestamp

        # Crear una gráfica de línea de las ventas mensuales
        plt.figure(figsize=(15, 8))
        plt.plot(monthly_sales['Month'], monthly_sales['Sales'], marker='o', linestyle='-')
        plt.title('Ventas Mensuales por Año')
        plt.xlabel('Mes')
        plt.ylabel('Ventas')
        plt.grid(True)

        # Asegurarse de que se muestren todas las etiquetas de los meses
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Mostrar todos los meses
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Formato de las etiquetas: Año-Mes

        plt.xticks(rotation=50)
        plt.tight_layout()

        st.pyplot(plt)
        plt.close()

def show_quantity_frequency_chart(df):
    suppress_warnings()
    chart_placeholder_2.empty()  # Limpiar el contenedor de la gráfica

    with chart_placeholder_2.container():
        st.title('Frecuencia de ventas por Cantidades')

        # Crear el gráfico de barras
        plt.figure(figsize=(12, 8))
        ax = sns.countplot(x='Quantity', data=df, palette='viridis', hue='Quantity', legend=False)

        # Añadir etiquetas de datos en cada barra
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.0f'),  # Formato sin decimales
                        (p.get_x() + p.get_width() / 2., p.get_height()),  # Posición de las etiquetas
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points')

        # Añadiendo títulos y etiquetas
        plt.title('Frecuencia de ventas por Cantidades')
        plt.xlabel('Cantidades')
        plt.ylabel('Frecuencia')
        plt.xticks(rotation=45)

        # Mostrar la gráfica
        st.pyplot(plt)
        plt.close()

def show_profit_margin_chart(df_Orders):
    suppress_warnings()
    chart_placeholder_3.empty()  # Limpiar el contenedor de la gráfica

    with chart_placeholder_3.container():
        st.title('Margen de Ganancias por Nivel de Descuento')
        # Calcular el margen de ganancias como porcentaje
        df_Orders['Profit_Margin'] = (df_Orders['Profit'] / df_Orders['Sales']) * 100

        # Agrupar por nivel de descuento y calcular el margen promedio
        profit_margin_by_discount = df_Orders.groupby('Discount')['Profit_Margin'].mean().reset_index()

        # Crear una gráfica de líneas de margen de ganancias por nivel de descuento
        plt.figure(figsize=(10, 5))
        plt.plot(profit_margin_by_discount['Discount'], profit_margin_by_discount['Profit_Margin'], marker='o', linestyle='-')
        plt.title(f'Margen de Ganancias por Nivel de Descuento en {year_to_filter}')
        plt.xlabel('Descuento')
        plt.ylabel('Margen de Ganancias (%)')
        plt.grid(True)
        plt.tight_layout()

        st.pyplot(plt)
        plt.close()

############################################## SUBCATEGORIA ##############################################

def show_sales_by_subcategory(df):
    suppress_warnings()
    chart_placeholder_4.empty()  # Limpiar el contenedor de la gráfica

    with chart_placeholder_4.container():
        st.title('Ventas por SubCategoría')
        # Agrupar por SubCategory y sumar las ventas (Sales)
        sales_by_subcategory = df.groupby('SubCategory')['Sales'].sum().reset_index()

        # Ordenar de mayor a menor las ventas
        sales_by_subcategory = sales_by_subcategory.sort_values(by='Sales', ascending=False)

        # Crear la gráfica de barras para las ventas por SubCategory
        plt.figure(figsize=(12, 8))
        ax = sns.barplot(x='Sales', y='SubCategory', data=sales_by_subcategory, palette='viridis')

        # Cambiar el formato del eje X para mostrar separadores de miles y el signo de dólar
        plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))

        # Añadir etiquetas de datos
        for index, value in enumerate(sales_by_subcategory['Sales']):
            ax.text(value, index, f'${value:,.0f}', color='black', ha="left")

        # Añadir títulos y etiquetas
        plt.title('Ventas por SubCategoría')
        plt.xlabel('Ventas Totales ($)')
        plt.ylabel('SubCategoría')

        # Mostrar la gráfica
        st.pyplot(plt)
        plt.close()

def show_net_sales_by_subcategory(df):
    suppress_warnings()
    chart_placeholder_5.empty()  # Limpiar el contenedor de la gráfica

    with chart_placeholder_5.container():
        st.title('Ventas Netas por SubCategoría')
        
        # Calcular la venta neta (restando descuento y costo de envío)
        df['Net_Sales'] = df['Sales'] - (df['Discount']*df['Sales']) - df['Shipping_Cost']

        # Agrupar por SubCategory y sumar las ventas netas
        net_sales_by_subcategory = df.groupby('SubCategory')['Net_Sales'].sum().reset_index()

        # Ordenar de mayor a menor las ventas netas
        net_sales_by_subcategory = net_sales_by_subcategory.sort_values(by='Net_Sales', ascending=False)

        # Crear la gráfica de barras para las ventas netas por SubCategory
        plt.figure(figsize=(12, 8))
        ax = sns.barplot(x='Net_Sales', y='SubCategory', data=net_sales_by_subcategory, palette='viridis')

        # Cambiar el formato del eje X para mostrar separadores de miles y el signo de dólar
        plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))

        # Añadir etiquetas de datos en cada barra
        for index, value in enumerate(net_sales_by_subcategory['Net_Sales']):
            ax.text(value, index, f'${value:,.0f}', color='black', ha="left")

        # Añadir títulos y etiquetas
        plt.title('Ventas Netas por SubCategoría')
        plt.xlabel('Ventas Netas Totales ($)')
        plt.ylabel('SubCategoría')

        # Mostrar la gráfica
        st.pyplot(plt)
        plt.close()


def show_profit_by_subcategory(df):
    suppress_warnings()
    chart_placeholder_6.empty()  # Limpiar el contenedor de la gráfica

    with chart_placeholder_6.container():
        st.title('Ganancias por SubCategoría')

        # Agrupar por SubCategory y sumar las ganancias (Profit)
        profit_by_subcategory = df.groupby('SubCategory')['Profit'].sum().reset_index()

        # Ordenar de mayor a menor las ganancias
        profit_by_subcategory = profit_by_subcategory.sort_values(by='Profit', ascending=False)

        # Crear la gráfica de barras para las ganancias por SubCategory
        plt.figure(figsize=(12, 8))
        ax = sns.barplot(x='Profit', y='SubCategory', data=profit_by_subcategory, palette='viridis')

        # Cambiar el formato del eje X para mostrar separadores de miles y el signo de dólar
        plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))

        # Añadir etiquetas de datos
        for index, value in enumerate(profit_by_subcategory['Profit']):
            ax.text(value, index, f'${value:,.0f}', color='black', ha="left")

        # Añadir títulos y etiquetas
        plt.title('Ganancias por SubCategoría')
        plt.xlabel('Ganancias Totales ($)')
        plt.ylabel('SubCategoría')

        # Mostrar la gráfica
        st.pyplot(plt)
        plt.close()

def show_shipping_cost_by_subcategory(df):
    suppress_warnings()
    chart_placeholder_7.empty()  # Limpiar el contenedor de la gráfica

    with chart_placeholder_7.container():
        st.title('Costo de Envío por SubCategoría')

        # Agrupar por Subcategoria y sumar los costos de envío (Shipping_Cost)
        shipping_cost_by_subcategory = df.groupby('SubCategory')['Shipping_Cost'].sum().reset_index()

        # Ordenar de mayor a menor los costos de envío
        shipping_cost_by_subcategory = shipping_cost_by_subcategory.sort_values(by='Shipping_Cost', ascending=False)

        # Crear la gráfica de barras para las ganancias por SubCategory
        plt.figure(figsize=(12, 8))
        ax = sns.barplot(x='Shipping_Cost', y='SubCategory', data=shipping_cost_by_subcategory, palette='viridis')

        # Cambiar el formato del eje X para mostrar separadores de miles y el signo de dólar
        plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))

        # Añadir etiquetas de datos
        for index, value in enumerate(shipping_cost_by_subcategory['Shipping_Cost']):
            ax.text(value, index, f'${value:,.0f}', color='black', ha="left")

        # Añadir títulos y etiquetas
        plt.title('Costo de Envío por SubCategoría')
        plt.xlabel('Costo de Envío ($)')
        plt.ylabel('SubCategoría')

        # Mostrar la gráfica
        st.pyplot(plt)
        plt.close()

def show_discounts_by_subcategory(df):
    suppress_warnings()
    chart_placeholder_8.empty()  # Limpiar el contenedor de la gráfica

    with chart_placeholder_8.container():
        st.title('Descuentos Totales por SubCategoría')

        # Calcular el valor total del descuento (Discount * Sales)
        df['Total_Discount'] = df['Discount'] * df['Sales']

        # Agrupar por SubCategory y sumar los descuentos totales
        discounts_by_subcategory = df.groupby('SubCategory')['Total_Discount'].sum().reset_index()

        # Ordenar de mayor a menor los descuentos totales
        discounts_by_subcategory = discounts_by_subcategory.sort_values(by='Total_Discount', ascending=False)

        # Crear la gráfica de barras para los descuentos por SubCategoría
        plt.figure(figsize=(12, 8))
        ax = sns.barplot(x='Total_Discount', y='SubCategory', data=discounts_by_subcategory, palette='viridis')

        # Añadir etiquetas de datos en cada barra
        for i, value in enumerate(discounts_by_subcategory['Total_Discount']):
            ax.text(value, i, f'${value:,.0f}', va='center', ha='left', color='black')

        # Cambiar el formato del eje X para mostrar separadores de miles y el signo de dólar
        plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))

        # Añadir títulos y etiquetas
        plt.title('Descuentos Totales por SubCategoría')
        plt.xlabel('Descuentos Totales ($)')
        plt.ylabel('SubCategoría')

        # Mostrar la gráfica
        st.pyplot(plt)
        plt.close()

def show_cost_by_subcategory(df):
    suppress_warnings()
    chart_placeholder_9.empty()  # Limpiar el contenedor de la gráfica

    with chart_placeholder_9.container():
        st.title('Costos Totales por SubCategoría')

         # Calcular la venta neta (restando descuento y costo de envío)
        df['Net_Sales'] = df['Sales'] - (df['Discount']*df['Sales']) - df['Shipping_Cost']

        # Calcular el costo total de la venta
        df['Cost'] = (df['Net_Sales'] - df['Profit'] )

        # Agrupar por SubCategory y sumar los costos totales
        cost_by_subcategory = df.groupby('SubCategory')['Cost'].sum().reset_index()

        # Ordenar de mayor a menor los costos totales
        cost_by_subcategory = cost_by_subcategory.sort_values(by='Cost', ascending=False)

        # Crear la gráfica de barras para los costos por SubCategoría
        plt.figure(figsize=(12, 8))
        ax = sns.barplot(x='Cost', y='SubCategory', data=cost_by_subcategory, palette='viridis')

        # Añadir etiquetas de datos en cada barra
        for i, value in enumerate(cost_by_subcategory['Cost']):
            ax.text(value, i, f'${value:,.0f}', va='center', ha='left', color='black')

        # Cambiar el formato del eje X para mostrar separadores de miles y el signo de dólar
        plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))

        # Añadir títulos y etiquetas
        plt.title('Costos Totales por SubCategoría')
        plt.xlabel('Costos Totales ($)')
        plt.ylabel('SubCategoría')

        # Mostrar la gráfica
        st.pyplot(plt)
        plt.close()

############################################## REGION ##############################################

def show_sales_by_region(df):
    suppress_warnings()
    chart_placeholder_10.empty()  # Limpiar el contenedor de la gráfica

    with chart_placeholder_10.container():
        st.title('Ventas por Región')
        # Agrupar por Region y sumar las ventas (Sales)
        sales_by_region = df.groupby('Region')['Sales'].sum().reset_index()

        # Ordenar de mayor a menor las ventas
        sales_by_region = sales_by_region.sort_values(by='Sales', ascending=False)

        # Crear la gráfica de barras para las ventas por Region
        plt.figure(figsize=(12, 8))
        ax = sns.barplot(x='Sales', y='Region', data=sales_by_region, palette='viridis')

        # Cambiar el formato del eje X para mostrar separadores de miles y el signo de dólar
        plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))

        # Añadir etiquetas de datos
        for index, value in enumerate(sales_by_region['Sales']):
            ax.text(value, index, f'${value:,.0f}', color='black', ha="left")

        # Añadir títulos y etiquetas
        plt.title('Ventas por Región')
        plt.xlabel('Ventas Totales ($)')
        plt.ylabel('Región')

        # Mostrar la gráfica
        st.pyplot(plt)
        plt.close()

def show_net_sales_by_region(df):
    suppress_warnings()
    chart_placeholder_11.empty()  # Limpiar el contenedor de la gráfica

    with chart_placeholder_11.container():
        st.title('Ventas Netas por Región')
        
        # Calcular la venta neta (restando descuento y costo de envío)
        df['Net_Sales'] = df['Sales'] - (df['Discount']*df['Sales']) - df['Shipping_Cost']

        # Agrupar por Region y sumar las ventas netas
        net_sales_by_region = df.groupby('Region')['Net_Sales'].sum().reset_index()

        # Ordenar de mayor a menor las ventas netas
        net_sales_by_region = net_sales_by_region.sort_values(by='Net_Sales', ascending=False)

        # Crear la gráfica de barras para las ventas netas por SubCategory
        plt.figure(figsize=(12, 8))
        ax = sns.barplot(x='Net_Sales', y='Region', data=net_sales_by_region, palette='viridis')

        # Cambiar el formato del eje X para mostrar separadores de miles y el signo de dólar
        plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))

        # Añadir etiquetas de datos en cada barra
        for index, value in enumerate(net_sales_by_region['Net_Sales']):
            ax.text(value, index, f'${value:,.0f}', color='black', ha="left")

        # Añadir títulos y etiquetas
        plt.title('Ventas Netas por Region')
        plt.xlabel('Ventas Netas Totales ($)')
        plt.ylabel('Region')

        # Mostrar la gráfica
        st.pyplot(plt)
        plt.close()

def show_profit_by_region(df):
    suppress_warnings()
    chart_placeholder_12.empty()  # Limpiar el contenedor de la gráfica

    with chart_placeholder_12.container():
        st.title('Ganancias por Región')

        # Agrupar por Region y sumar las ganancias (Profit)
        profit_by_region = df.groupby('Region')['Profit'].sum().reset_index()

        # Ordenar de mayor a menor las ganancias
        profit_by_region = profit_by_region.sort_values(by='Profit', ascending=False)

        # Crear la gráfica de barras para las ganancias por Region
        plt.figure(figsize=(12, 8))
        ax = sns.barplot(x='Profit', y='Region', data=profit_by_region, palette='viridis')

        # Cambiar el formato del eje X para mostrar separadores de miles y el signo de dólar
        plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))

        # Añadir etiquetas de datos
        for index, value in enumerate(profit_by_region['Profit']):
            ax.text(value, index, f'${value:,.0f}', color='black', ha="left")

        # Añadir títulos y etiquetas
        plt.title('Ganancias por Región')
        plt.xlabel('Ganancias Totales ($)')
        plt.ylabel('Región')

        # Mostrar la gráfica
        st.pyplot(plt)
        plt.close()



def show_shipping_cost_by_region(df):
    suppress_warnings()
    chart_placeholder_13.empty()  # Limpiar el contenedor de la gráfica

    with chart_placeholder_13.container():
        st.title('Costo de Envío por Región')

        # Agrupar por Region y sumar los costos de envío (Shipping_Cost)
        shipping_cost_by_region = df.groupby('Region')['Shipping_Cost'].sum().reset_index()

        # Ordenar de mayor a menor los costos de envío
        shipping_cost_by_region = shipping_cost_by_region.sort_values(by='Shipping_Cost', ascending=False)

        # Crear la gráfica de barras para las ganancias por Region
        plt.figure(figsize=(12, 8))
        ax = sns.barplot(x='Shipping_Cost', y='Region', data=shipping_cost_by_region, palette='viridis')

        # Cambiar el formato del eje X para mostrar separadores de miles y el signo de dólar
        plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))

        # Añadir etiquetas de datos
        for index, value in enumerate(shipping_cost_by_region['Shipping_Cost']):
            ax.text(value, index, f'${value:,.0f}', color='black', ha="left")

        # Añadir títulos y etiquetas
        plt.title('Costo de Envío por Región')
        plt.xlabel('Costo de Envío ($)')
        plt.ylabel('Región')

        # Mostrar la gráfica
        st.pyplot(plt)
        plt.close()

def show_discounts_by_region(df):
    suppress_warnings()
    chart_placeholder_14.empty()  # Limpiar el contenedor de la gráfica

    with chart_placeholder_14.container():
        st.title('Descuentos Totales por Región')

        # Calcular el valor total del descuento (Discount * Sales)
        df['Total_Discount'] = df['Discount'] * df['Sales']

        # Agrupar por Region y sumar los descuentos totales
        discounts_by_region = df.groupby('Region')['Total_Discount'].sum().reset_index()

        # Ordenar de mayor a menor los descuentos totales
        discounts_by_region = discounts_by_region.sort_values(by='Total_Discount', ascending=False)

        # Crear la gráfica de barras para los descuentos por SubCategoría
        plt.figure(figsize=(12, 8))
        ax = sns.barplot(x='Total_Discount', y='Region', data=discounts_by_region, palette='viridis')

        # Añadir etiquetas de datos en cada barra
        for i, value in enumerate(discounts_by_region['Total_Discount']):
            ax.text(value, i, f'${value:,.0f}', va='center', ha='left', color='black')

        # Cambiar el formato del eje X para mostrar separadores de miles y el signo de dólar
        plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))

        # Añadir títulos y etiquetas
        plt.title('Descuentos Totales por Region')
        plt.xlabel('Descuentos Totales ($)')
        plt.ylabel('Region')

        # Mostrar la gráfica
        st.pyplot(plt)
        plt.close()

def show_cost_by_region(df):
    suppress_warnings()
    chart_placeholder_15.empty()  # Limpiar el contenedor de la gráfica

    with chart_placeholder_15.container():
        st.title('Costos Totales por Región')

         # Calcular la venta neta (restando descuento y costo de envío)
        df['Net_Sales'] = df['Sales'] - (df['Discount']*df['Sales']) - df['Shipping_Cost']

        # Calcular el costo total de la venta
        df['Cost'] = (df['Net_Sales'] - df['Profit'] )

        # Agrupar por Region y sumar los costos totales
        cost_by_region = df.groupby('Region')['Cost'].sum().reset_index()

        # Ordenar de mayor a menor los costos totales
        cost_by_region = cost_by_region.sort_values(by='Cost', ascending=False)

        # Crear la gráfica de barras para los costos por SubCategoría
        plt.figure(figsize=(12, 8))
        ax = sns.barplot(x='Cost', y='Region', data=cost_by_region, palette='viridis')

        # Añadir etiquetas de datos en cada barra
        for i, value in enumerate(cost_by_region['Cost']):
            ax.text(value, i, f'${value:,.0f}', va='center', ha='left', color='black')

        # Cambiar el formato del eje X para mostrar separadores de miles y el signo de dólar
        plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))

        # Añadir títulos y etiquetas
        plt.title('Costos Totales por Region')
        plt.xlabel('Costos Totales ($)')
        plt.ylabel('Region')

        # Mostrar la gráfica
        st.pyplot(plt)
        plt.close()


# Botón para actualizar los datos
if st.button('Actualizar gráficos y tabla'):
    df_Orders = load_data_Orders()  # Cargar los datos actualizados
    df_Returns = load_data_Returns()
    show_table(filtered_data)  # Mostrar la tabla actualizada

    show_sales_chart(filtered_data)
    show_quantity_frequency_chart(filtered_data)
    show_profit_margin_chart(filtered_data)

    show_sales_by_subcategory(filtered_data)
    show_net_sales_by_subcategory(filtered_data)
    show_profit_by_subcategory(filtered_data)
    show_shipping_cost_by_subcategory(filtered_data)
    show_discounts_by_subcategory(filtered_data)
    show_cost_by_subcategory(filtered_data)

    show_sales_by_region(filtered_data)
    show_net_sales_by_region(filtered_data)
    show_profit_by_region(filtered_data)
    show_shipping_cost_by_region(filtered_data)
    show_discounts_by_region(filtered_data)
    show_cost_by_region(filtered_data)



# Refresco automático
while True:
    df_Orders = load_data_Orders()
    df_Returns = load_data_Returns()
    show_table(filtered_data)  # Mostrar la tabla actualizada

    show_sales_chart(filtered_data)
    show_quantity_frequency_chart(filtered_data)
    show_profit_margin_chart(filtered_data)

    show_sales_by_subcategory(filtered_data)
    show_net_sales_by_subcategory(filtered_data)
    show_profit_by_subcategory(filtered_data)
    show_shipping_cost_by_subcategory(filtered_data)
    show_discounts_by_subcategory(filtered_data)
    show_cost_by_subcategory(filtered_data)

    show_sales_by_region(filtered_data)
    show_net_sales_by_region(filtered_data)
    show_profit_by_region(filtered_data)
    show_shipping_cost_by_region(filtered_data)
    show_discounts_by_region(filtered_data)
    show_cost_by_region(filtered_data)
    time.sleep(10)  # Esperar 10 segundos antes de actualizar