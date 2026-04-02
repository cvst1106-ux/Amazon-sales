'''Dashboard interactivo del analisis de ventas de amazon sales'''

# se exportan las librerias necesarias
import streamlit as st
import pandas as pd
import plotly.express as px

Amazon = ["#D46A07", "#1D2B44", "#3A5285", "#AFAFB3"]

st.set_page_config(
    page_title = "Dashboard Amazon",
    page_icon = ":incoming_envelope:")

st.title("Analisis de precios y descuentos de Amazon", text_alignment = "center")
st.write("**Dashboard interactivo** del análisis del catálogo de Amazon, acerca de la relación entre precios originales, descuentos y categorías.")
st.markdown("---")

@st.cache_data
def cargar_datos():
    df = pd.read_csv("amazon_limpio.csv")
    return df
df = cargar_datos()


st.sidebar.header("filtro por categoria")