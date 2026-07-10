import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Starbucks Sales Dashboard",
    page_icon="☕",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("data/starbucks_cleaned.csv")

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    numeric_cols = [
        "quantity",
        "unit_price_inr",
        "discount_percent",
        "total_amount_inr",
        "customer_rating"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


df = load_data()

st.sidebar.title("☕ Starbucks Filters")

city_filter = st.sidebar.multiselect(
    "Select City",
    sorted(df["city"].dropna().unique()),
    default=sorted(df["city"].dropna().unique())
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    sorted(df["category"].dropna().unique()),
    default=sorted(df["category"].dropna().unique())
)

channel_filter = st.sidebar.multiselect(
    "Select Order Channel",
    sorted(df["order_channel"].dropna().unique()),
    default=sorted(df["order_channel"].dropna().unique())
)

payment_filter = st.sidebar.multiselect(
    "Select Payment Method",
    sorted(df["payment_method"].dropna().unique()),
    default=sorted(df["payment_method"].dropna().unique())
)

loyalty_filter = st.sidebar.multiselect(
    "Select Loyalty Member",
    sorted(df["loyalty_member"].dropna().unique()),
    default=sorted(df["loyalty_member"].dropna().unique())
)

filtered_df = df[
    (df["city"].isin(city_filter)) &
    (df["category"].isin(category_filter)) &
    (df["order_channel"].isin(channel_filter)) &
    (df["payment_method"].isin(payment_filter)) &
    (df["loyalty_member"].isin(loyalty_filter))
]

st.title("☕ Starbucks Sales Analytics Dashboard")
st.write(
    "A business analytics dashboard for sales, products, stores, customers, "
    "payment trends, loyalty behavior, and monthly revenue."
)

total_sales = filtered_df["total_amount_inr"].sum()
total_orders = filtered_df["transaction_id"].nunique()
avg_order_value = total_sales / total_orders if total_orders != 0 else 0
avg_rating = filtered_df["customer_rating"].mean()
quantity_sold = filtered_df["quantity"].sum()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Sales", f"₹{total_sales:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Avg Order Value", f"₹{avg_order_value:,.0f}")
col4.metric("Avg Rating", f"{avg_rating:.2f}")
col5.metric("Quantity Sold", f"{int(quantity_sold):,}")

st.divider()

chart_config = {
    "displaylogo": False,
    "responsive": True
}

c1, c2 = st.columns(2)

with c1:
    city_sales = (
        filtered_df.groupby("city")["total_amount_inr"]
        .sum()
        .reset_index()
        .sort_values("total_amount_inr", ascending=False)
    )

    fig = px.bar(
        city_sales,
        x="city",
        y="total_amount_inr",
        title="Sales by City",
        text_auto=".2s"
    )

    st.plotly_chart(fig, config=chart_config)

with c2:
    category_sales = (
        filtered_df.groupby("category")["total_amount_inr"]
        .sum()
        .reset_index()
        .sort_values("total_amount_inr", ascending=False)
    )

    fig = px.pie(
        category_sales,
        names="category",
        values="total_amount_inr",
        hole=0.45,
        title="Sales Share by Category"
    )

    st.plotly_chart(fig, config=chart_config)

c3, c4 = st.columns(2)

with c3:
    top_products = (
        filtered_df.groupby("product_name")["total_amount_inr"]
        .sum()
        .reset_index()
        .sort_values("total_amount_inr", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top_products,
        x="total_amount_inr",
        y="product_name",
        orientation="h",
        title="Top 10 Products by Revenue",
        text_auto=".2s"
    )

    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, config=chart_config)

with c4:
    payment_sales = (
        filtered_df.groupby("payment_method")["total_amount_inr"]
        .sum()
        .reset_index()
        .sort_values("total_amount_inr", ascending=False)
    )

    fig = px.pie(
        payment_sales,
        names="payment_method",
        values="total_amount_inr",
        hole=0.5,
        title="Payment Method Distribution"
    )

    st.plotly_chart(fig, config=chart_config)

st.subheader("📈 Monthly Revenue Trend")

monthly_sales = (
    filtered_df.dropna(subset=["order_date"])
    .groupby(filtered_df["order_date"].dt.to_period("M"))["total_amount_inr"]
    .sum()
    .reset_index()
)

monthly_sales["order_date"] = monthly_sales["order_date"].astype(str)

fig = px.line(
    monthly_sales,
    x="order_date",
    y="total_amount_inr",
    markers=True,
    title="Monthly Revenue Trend"
)

st.plotly_chart(fig, config=chart_config)

c5, c6 = st.columns(2)

with c5:
    store_sales = (
        filtered_df.groupby("store_name")["total_amount_inr"]
        .sum()
        .reset_index()
        .sort_values("total_amount_inr", ascending=False)
        .head(10)
    )

    fig = px.bar(
        store_sales,
        x="total_amount_inr",
        y="store_name",
        orientation="h",
        title="Top 10 Stores by Revenue",
        text_auto=".2s"
    )

    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, config=chart_config)

with c6:
    rating_data = filtered_df.dropna(subset=["customer_rating"])

    fig = px.histogram(
        rating_data,
        x="customer_rating",
        nbins=10,
        title="Customer Rating Distribution"
    )

    st.plotly_chart(fig, config=chart_config)

c7, c8 = st.columns(2)

with c7:
    qty_category = (
        filtered_df.groupby("category")["quantity"]
        .sum()
        .reset_index()
        .sort_values("quantity", ascending=False)
    )

    fig = px.bar(
        qty_category,
        x="category",
        y="quantity",
        title="Quantity Sold by Category",
        text_auto=True
    )

    st.plotly_chart(fig, config=chart_config)

with c8:
    fig = px.scatter(
        filtered_df,
        x="discount_percent",
        y="total_amount_inr",
        color="category",
        title="Discount vs Sales",
        hover_data=["product_name", "city", "payment_method"]
    )

    st.plotly_chart(fig, config=chart_config)

c9, c10 = st.columns(2)

with c9:
    loyalty_sales = (
        filtered_df.groupby("loyalty_member")["total_amount_inr"]
        .sum()
        .reset_index()
        .sort_values("total_amount_inr", ascending=False)
    )

    fig = px.bar(
        loyalty_sales,
        x="loyalty_member",
        y="total_amount_inr",
        title="Sales by Loyalty Members",
        text_auto=".2s"
    )

    st.plotly_chart(fig, config=chart_config)

with c10:
    channel_sales = (
        filtered_df.groupby("order_channel")["total_amount_inr"]
        .sum()
        .reset_index()
        .sort_values("total_amount_inr", ascending=False)
    )

    fig = px.pie(
        channel_sales,
        names="order_channel",
        values="total_amount_inr",
        hole=0.45,
        title="Sales by Order Channel"
    )

    st.plotly_chart(fig, config=chart_config)

st.subheader("🧠 Business Insights")

if not filtered_df.empty:
    best_city = city_sales.iloc[0]["city"]
    best_category = category_sales.iloc[0]["category"]
    best_product = top_products.iloc[0]["product_name"]

    st.info(
        f"""
        **Top Performing City:** {best_city}  
        **Highest Revenue Category:** {best_category}  
        **Best Selling Product:** {best_product}  
        **Average Customer Rating:** {avg_rating:.2f}
        """
    )
else:
    st.warning("No data available for the selected filters.")

st.subheader("📋 Filtered Dataset")

st.dataframe(filtered_df)

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="filtered_starbucks_data.csv",
    mime="text/csv"
)