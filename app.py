'''Dashboard interactivo del analisis de ventas de amazon sales'''

# se exportan las librerias necesarias
import streamlit as st
import pandas as pd
import plotly.express as px
# Se elige la paleta de colores que se van a usar en los graficos
Amazon = ["#E26F00",  
    "#EEEADF",
    "#000000", 
    "#959086",
    "#10436A",
    "#668779", 
    "#A35139",
    "#5472D5",
    "#F5C856" ]
# se configura como se ve la pestaña
st.set_page_config(
    page_title = "Dashboard Amazon",
    page_icon = "amazon-icon-seeklogo.png",
    layout= "wide")
# Diseño de la pagina
st.markdown("""
<style>
/* columnas con stMetric */
        [data-testid="stMetric"] {
    border-left: 4px solid #FF9900;
    border-radius: 10px;
    background-color: #0A1931 ;
}
/* Botones */
        .stTabs [role="tab"][aria-selected="true"] {
    background-color: #FF9900;
    color: #232F3E;
    border-radius: 8px 8px 0 0;
}
/* Celdas de la tabla */
.stDataFrame td {
    background-color: #0A1931 !important;
    color: #FFFFFF !important;
}

/* Borde de la tabla */
.stDataFrame {
    border: 2px solid #FF9900 !important;
    border-radius: 10px;
}
</style>

""", unsafe_allow_html=True)


# Se configura el titulo de la pagina y el logoo
#main?
col1,col2 = st.columns([0.2,0.8])
with col1:
    st.image("Amazon_dashboard__3_-removebg-preview.png", width=400)
with col2:
    st.title("Analisis de precios y descuentos de Amazon",text_alignment = "center" )
st.write("#### Dashboard interactivo del análisis del catálogo de Amazon," \
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
económico = df["precio_original"].quantile(0.25)
lujo = df["precio_original"].quantile(0.75)
def clasificar_producto(precio):
    if precio <= económico:
        return "Económico"
    elif precio >= lujo:
        return "Lujo"
    else:
        return "Estandar"
df["categoria_de_precio"]  = df["precio_original"].apply(clasificar_producto)
        
# Se configura la barra lateral
with st.sidebar:
# Se coloca un filtro por categoria
    st.header("categoría por producto 🔎")
    filtro1 = st.multiselect(
    "selecciona las categoria:",
    options=df["subcategoria"].unique(),
    default=df["subcategoria"].unique())
    st.markdown("---")
# Se agrega un filtro por categoria de precio
    st.header("🏷️categoría por precio")
    filtro2 =  st.multiselect("Selecciona las categorías:",
    options=df["categoria_de_precio"].unique(),
    default=df["categoria_de_precio"].unique())
    st.markdown("***")
# Se coloca un filtrado por precio y uno por descuento 
    descuento_min = int(df["porcentaje_descuento"].min())
    descuento_max = int(df["porcentaje_descuento"].max())
    filtro3 = st.slider(
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
    f_categoria = df["subcategoria"] == df["subcategoria"]
if filtro2:
    f_cprecio = df["categoria_de_precio"].isin(filtro2)
else:
    f_cprecio = df["categoria_de_precio"] == df["categoria_de_precio"]
f_porcentaje =(df["porcentaje_descuento"].between(filtro3[0], filtro3[1]))

df_filtrado = df[f_categoria & f_cprecio & f_porcentaje]

df_cat = df[f_categoria]

if len(df_filtrado) == 0: 
    st.warning(" No hay productos con esos filtros. Intenta con otros rangos.")
   

# se añaden columnas interactivas con informacion relevante
st.header("Resumen del catalogo de Amazon")

col1, col2, col3,col4 = st.columns(4)

with col1:
    st.metric("📦 Total de productos", f"{len(df_filtrado):,}", border= True)
with col2:
    st.metric("📚 Categorías", df_filtrado["subcategoria"].nunique(), border= True)
with col3:
    st.metric("💸 Precio promedio",f'₹{df_filtrado["precio_original"].mean():,.0f}', border= True)
with col4:
    st.metric("✂️ Descuento promedio", f'{df_filtrado["porcentaje_descuento"].mean():.2f}%', border= True)

# Se crean pestañas para organizar mejor el dashboard
tab1, tab2, tab3, tab4 = st.tabs(["🔍Resumen del catalogo", "📊Distribucion por categoría", "📈Analisis de precios y descuentos","📋Dataframe"])
with tab1:
    col1, col2 = st.columns([0.2 , 0.8])
    with col1:
        with st.container(border = True):
            st.markdown("### 🔝Top 10 productos con precios mas altos")
    with col2:
        st.dataframe(df_cat.nlargest(10, "precio_original")[["nombre_producto","precio_original","precio_descuento","porcentaje_descuento","categoria"]])
    st.divider()
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.dataframe(df_cat.nlargest(10, "porcentaje_descuento")[["nombre_producto","porcentaje_descuento","precio_original","precio_descuento","categoria"]])
    with col2:
        with st.container(border = True):
            st.subheader("🔝Top 10 productos con mayor descuento")
    st.divider()
    st.subheader("estadisticas generales de los productos", text_alignment= "center")
    st.write(df_filtrado[["precio_original", "precio_descuento", "porcentaje_descuento"]].describe())

with tab2:
    st.write("### Distribucion de productos")
#primer grafico : cantidad de productos por categoria
    cantidad_productos = df_filtrado["subcategoria"].value_counts().reset_index()
    fig1 =px.bar(cantidad_productos,
        x= "subcategoria",
        y="count",
        title="📦 Cantidad de productos por categoría",
        labels= {"subcategoria": "Categoría", "count":"Cantidad de productos"},
        color_discrete_sequence= Amazon
        )
    st.plotly_chart(fig1, use_container_width=True)
    st.divider()
#grafico 2 : distribucion de precios
    st.write("### Distribución de precios")

    fig2 = px.box(
        df_filtrado,
        x="categoria_de_precio",
        y =  "precio_original",
        color="categoria_de_precio",
        title="📊 Distribución de precios por categoría (Economico/Estandar/Lujo)",
        labels= {"precio_original" : "Precio original (₹)", "categoria_de_precio" : "Categoría de precio"},
        color_discrete_sequence= Amazon
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    #grafico de dispersion
    st.write("### Relacion entre precios y descuento")
    fig4 = px.scatter(df_filtrado,
        x = "porcentaje_descuento",
        y = "precio_original",
        color = "subcategoria",
        title = "🔄 Relación: Descuento vs Precio original por categoría",
        labels={"porcentaje_descuento": "Descuento (%)", "precio_original": "Precio original (₹)"},
        color_discrete_sequence= Amazon,
        opacity=0.6)
    st.plotly_chart(fig4, use_container_width=True)

    st.divider()
    st.write("### Mapa de calor")
    correlacion = df_filtrado[["precio_original", "precio_descuento", "porcentaje_descuento"]].corr()
    fig5 = px.imshow(
    correlacion,
    text_auto=True,
    color_continuous_scale="RdBu",
    title="🌡️ Correlaciones entre variables")
    st.plotly_chart(fig5, use_container_width=True)
    
    fig6 = px.box(
    df_filtrado,
    x="subcategoria",
    y="precio_original",
    color="subcategoria",
    title="🎚️ Distribución de precios por categoría",
    color_discrete_sequence= Amazon)
    st.plotly_chart(fig6, use_container_width=True)
   

with tab4:
    st.write("")
    st.dataframe(df_filtrado.style.highlight_max(axis=0))

