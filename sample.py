import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

from sqlalchemy import create_engine, inspect
from sqlalchemy import text

st.title("DS3A - Cloud Computing")
st.subheader("Karylle dela Cruz")

warehouse = "postgresql://duckdb_sample_user:i6iKJc6FCs4hVS3AX6yMZngxJvMkzGCs@dpg-d0b2efp5pdvs73c9pi00-a.singapore-postgres.render.com/duckdb_sample"
engine = create_engine(warehouse,  client_encoding='utf8')
connection = engine.connect()

@st.cache_data
def load_data():
    query_ext = """
        SELECT *
        FROM sales_data_duckdb
    """
    result = connection.execute(text(query_ext))
    return pd.DataFrame(result.mappings().all())

df = load_data()

top_products = df.groupby("Product")["Quantity Ordered"].sum().sort_values(ascending=False).reset_index()
fig1 = px.bar(top_products, x='Product', y='Quantity Ordered', title='Top Products by Quantity Ordered')
st.plotly_chart(fig1)

df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Month'] = df['Order Date'].dt.to_period('M').astype(str)

monthly_sales = df.groupby("Month")["Price Each"].sum().reset_index()
fig2 = px.line(monthly_sales, x='Month', y='Price Each', title='Monthly Sales Trend')
st.plotly_chart(fig2)

fig4 = px.pie(top_products, names='Product', values='Quantity Ordered', title='Product Sales Distribution')
st.plotly_chart(fig4)

df['Hour'] = df['Order Date'].dt.hour
hourly_orders = df.groupby('Hour')["Order ID"].count().reset_index()
fig5 = px.bar(hourly_orders, x='Hour', y='Order ID', title='Orders by Hour of Day')
st.plotly_chart(fig5)

