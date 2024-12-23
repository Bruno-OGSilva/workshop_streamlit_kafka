import streamlit as st
import pandas as pd
import os


st.set_page_config(
    page_title="Workshop Streamlit - Real Time Dashboard",
    page_icon=":material/bar_chart:",
    layout="wide"

)

@st.cache_data
def get_data():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_file = os.path.join(base_dir, "data", "orders.parquet")
    df = pd.read_parquet(data_file)
    df["order_date"] = pd.to_datetime(df["order_date"])

    return df

orders_df = get_data()

st.title("Workshop Streamlit - Real Time Dashboard")

st.dataframe(orders_df)