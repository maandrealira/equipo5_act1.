"""Activity 1: Sales Explorer.

App de un solo archivo con filtros de región y categoría, tarjetas de KPI,
gráfica de unidades diarias y top 10 de SKUs por ingresos.

Run:   streamlit run app.py
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Ruta para el repo propio: el CSV va junto a app.py
DATA = Path(__file__).parent / "sales_daily.csv"

st.set_page_config(page_title="Sales Explorer", layout="wide")
st.title("Sales Explorer")

df = pd.read_csv(DATA, parse_dates=["date"])

# TODO 1: filtro de región
st.sidebar.header("Filtros")
regiones = sorted(df["region"].unique())
sel_regiones = st.sidebar.multiselect("Región", regiones, default=regiones)

# TODO 2: filtro de categoría
categorias = sorted(df["category"].unique())
sel_categorias = st.sidebar.multiselect("Categoría", categorias, default=categorias)

df = df[df["region"].isin(sel_regiones) & df["category"].isin(sel_categorias)]

if df.empty:
    st.warning("No hay datos con esos filtros. Elige al menos una región y una categoría.")
    st.stop()

# TODO 3: tarjetas de KPI
k1, k2, k3 = st.columns(3)
k1.metric("Unidades totales", f"{int(df['units'].sum()):,}")
k2.metric("Ingresos", f"${df['revenue'].sum():,.0f}")
k3.metric("Número de SKUs", df["sku"].nunique())

daily = df.groupby("date", as_index=False)["units"].sum()
fig = px.line(daily, x="date", y="units", title="Daily units")
st.plotly_chart(fig, width="stretch")

# TODO 4: top 10 SKUs por ingresos
top10 = (
    df.groupby("sku", as_index=False)["revenue"].sum()
    .sort_values("revenue", ascending=False)
    .head(10)
)
fig2 = px.bar(top10, x="sku", y="revenue", title="Top 10 SKUs by revenue")
st.plotly_chart(fig2, width="stretch")

# TODO 5 (stretch): filas filtradas
with st.expander("Ver filas filtradas"):
    st.dataframe(df, width="stretch")
