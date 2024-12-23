import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Workshop Streamlit - Real Time Dashboard",
    page_icon=":material/bar_chart:",
    layout="wide"

)

@st.cache_data
def get_data():
    df = pd.read_parquet("data/orders.parquet")
    df["order_date"] = pd.to_datetime(df["order_date"])

    return df

orders_df = get_data()

st.title("Workshop Streamlit - Real Time Dashboard")

st.dataframe(orders_df)