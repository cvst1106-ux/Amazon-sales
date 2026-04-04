'''Dashboard interactivo del analisis de ventas de amazon sales'''

# se exportan las librerias necesarias
import streamlit as st
import pandas as pd
import plotly.express as px
# Se elige la paleta de colores que se van a usar en los graficos
Amazon = ["#D46A07", "#1D2B44", "#3A5285", "#AFAFB3"]
# se configura como se ve la pestaña
st.set_page_config(
    page_title = "Dashboard Amazon",
    page_icon = "📊")
# Se configura el titulo de la pagina
st.title("Analisis de precios y descuentos de Amazon", text_alignment = "center")
st.write("**Dashboard interactivo** del análisis del catálogo de Amazon," \
" acerca de la relación entre precios originales, descuentos y categorías.")
st.markdown("---")
# Se carga el archivo
@st.cache_data
def cargar_datos():
    df = pd.read_csv("amazon_limpio.csv")
    return df
df = cargar_datos()
# Se manipula la variable categoria para poder trabajar con su primer elemento de la lista
df['subcategoria'] = df['categoria'].str.split('|').str[0]
# Se configura la barra lateral
with st.sidebar:
 # Se coloca un filtrado por categoria
    st.sidebar.header("filtro por categoria 🔎")
    categoria = st.multiselect(
    "Selecciona las categorias:",
    options=df["subcategoria"].unique())
    st.markdown("---")
# Se coloca un filtrado por precio y uno por descuento
    precio_min = int(df["precio_original"].min())
    precio_max = int(df["precio_original"].max())
    rango_precio = st.slider(
        "Rango de precio (₹):",
        min_value=precio_min,
        max_value=precio_max,
        value=(precio_min, precio_max),
        step=100,
        format="₹%d")
    
    precio_min = int(df["precio_descuento"].min())
    precio_max = int(df["precio_descuento"].max())
    rango_precio = st.slider(
        "porcentaje de descuento (%):",
        min_value=0,
        max_value=100,
        value=(0,100),
        format="%d%%")
# se añaden columnas con informacion relevante
st.header("")

col1, col2 = st.columns(2)

with col1:
    st.metric("📦 Total de productos", f"{len(df):,}", border= True)

with col2:
    st.metric(" Categorías", df["subcategoria"].nunique(), border= True)


