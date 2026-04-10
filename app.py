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
    #logo amazon?
    page_icon = "amazon-icon-seeklogo.png",
    layout= "wide")

# Se configura el titulo de la pagina y el logoo
#main?
col1,col2 = st.columns([0.2,0.8])
with col1:
    st.image("Amazon_dashboard__1_-removebg-preview.png", width=400)
with col2:
    st.title("Analisis de precios y descuentos de Amazon",text_alignment = "center" )
st.write("#### **Dashboard interactivo** del análisis del catálogo de Amazon," \
" acerca de la relación entre precios originales, descuentos y categorías.")
st.markdown("---")
# Se carga el archivo con el cache
@st.cache_data
def cargar_datos():
    df = pd.read_csv("amazon_limpio.csv")
    return df
df = cargar_datos()
# Se manipula la variable categoria para poder trabajar con su primer elemento de la lista
df['subcategoria'] = df['categoria'].str.split('|').str[0]

# se agrupan precios por categorias con cuartiles
economico = df["precio_original"].quantile(0.25)
lujo = df["precio_original"].quantile(0.75)
def clasificar_producto(precio):
    if precio <= economico:
        return "Económico"
    elif precio >= lujo:
        return "Lujo"
    else:
        return "Estandar"
df["categoria_de_precio"]  = df["precio_original"].apply(clasificar_producto)
        
# Se configura la barra lateral
with st.sidebar:
# Se coloca un filtro por categoria
    st.header("categoria por producto 🔎")
    filtro1 = st.multiselect(
    "Selecciona las categorias:",
    options=df["subcategoria"].unique(),
    default=df["subcategoria"].unique())
    st.markdown("---")
# Se agrega un filtro por categoria de precio
    st.header("🏷️categoria por precio")
    filtro2 =  st.multiselect("Selecciona las categorias:",
    options=df["categoria_de_precio"].unique(),
    default=df["categoria_de_precio"].unique())
    st.markdown("***")
# Se coloca un filtrado por precio y uno por descuento 
    precio_min = int(df["precio_original"].min())
    precio_max = int(df["precio_original"].max())
    filtro3 = st.slider(
        "Rango de precio (₹):",
        min_value=precio_min,
        max_value=precio_max,
        value=(precio_min, precio_max),
        step=100,
        format="₹%d")

    descuento_min = int(df["porcentaje_descuento"].min())
    descuento_max = int(df["porcentaje_descuento"].max())
    filtro4 = st.slider(
        "porcentaje de descuento (%):",
        min_value=0,
        max_value=100,
        value=(0,100),
        format="%d%%")
    st.markdown("***")


# Se conecta los filtros con los graficos y columnas para que sea interactivo

if filtro1:
    f_categoria = df["subcategoria"].isin(filtro1)
else:
    f_categoria = True
if filtro2:
    f_cprecio = (df["categoria_de_precio"].isin(filtro2)) 
else:
    f_cprecio = True
f_porcentaje =(df["porcentaje_descuento"]>= descuento_min) & (df["porcentaje_descuento"]<= descuento_max)
f_precio = (df["precio_original"]>= precio_min) & (df["precio_original"]<= precio_max)

df_filtrado = df[f_categoria & f_cprecio & f_porcentaje & f_precio]

# se añaden columnas con informacion relevante
st.header("Resumen del catalogo de Amazon")

col1, col2, col3,col4 = st.columns(4)

with col1:
    st.metric("📦 Total de productos", f"{len(df_filtrado):,}", border= True)
with col2:
    st.metric(" Categorías", df_filtrado["subcategoria"].nunique(), border= True)
with col3:
    st.metric("precio promedio",f'₹{df_filtrado["precio_original"].mean():,.0f}', border= True)
with col4:
    st.metric("descuento promedio", f'{df_filtrado["porcentaje_descuento"].mean().round(1)}%', border= True)

st.dataframe(df.style.highlight_max(axis=0))

