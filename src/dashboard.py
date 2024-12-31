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

order_col, items_col, ticket_col, total_col = st.columns(4)

with order_col:
    quantity = len(orders_df["quantity"])
    quantity = f"{quantity:,}"
    st.metric(label="Orders", value=quantity)

with items_col:
    itens = orders_df["quantity"].sum()
    itens = f"{itens:,}"
    st.metric(label="Itens", value=itens)

with ticket_col:
    ticket = orders_df["total_price"].mean()
    ticket = f"R$ {ticket:,.2f}"
    st.metric(label="Ticket", value=ticket)

with total_col:
    total = orders_df["total_price"].sum()
    total = f"R$ {total:,.2f}"
    st.metric(label="Total", value=total)


st.header("📊 Charts")
order_barchat, region_barchart = st.columns(2)
with order_barchat:
     st.bar_chart(orders_df, x="region", y="total_price")

with region_barchart:
    st.bar_chart(orders_df, x="vendor", y="total_price")

st.header("📈 sales By date")

orders_df = orders_df.sort_values(by="order_date")
line_df = (
    orders_df.groupby(orders_df["order_date"].dt.date)["total_price"]
    .sum()
    .reset_index()
)
st.line_chart(line_df, x="order_date", y="total_price")


st.header("Orders Dashboard")
st.dataframe(orders_df.iloc[::-1])