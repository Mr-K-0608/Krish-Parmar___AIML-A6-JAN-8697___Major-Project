import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Customer Churn Intelligence",
    layout="wide"
)

st.title("E-Commerce Customer Churn & Retention Dashboard")

# Load data

@st.cache_data
def load_data():
    return pd.read_csv("customer_churn_dashboard.csv")

df = load_data()

# KPIs

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Customers Scored",
    len(df)
)

col2.metric(
    "High Risk Customers",
    (df["risk_segment"] == "High Risk").sum()
)

col3.metric(
    "Expected Revenue Saved",
    f"${df['expected_revenue_saved'].sum():,.0f}"
)

st.divider()

# Churn Risk Chart

st.subheader("Churn Risk Distribution")

fig_risk = px.pie(
    df,
    names="risk_segment",
    title="Customer Risk Segments"
)

st.plotly_chart(fig_risk, use_container_width=True)

# Retention Actions

st.subheader("Retention Strategy Breakdown")

fig_action = px.bar(
    df["retention_action"].value_counts().reset_index(),
    x="count",
    y="retention_action",
    orientation="h",
    title="Recommended Actions"
)

st.plotly_chart(fig_action, use_container_width=True)

# Customer Explorer

st.subheader("Customer Explorer")

risk_filter = st.selectbox(
    "Filter by Risk Segment",
    ["All"] + sorted(df["risk_segment"].unique().tolist())
)

view_df = df.copy()

if risk_filter != "All":
    view_df = view_df[view_df["risk_segment"] == risk_filter]

st.dataframe(view_df.head(50), use_container_width=True)
