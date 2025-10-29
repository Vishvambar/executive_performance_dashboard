import pandas as pd
import plotly.express as px
import streamlit as st

# SET PAGE CONFIG
st.set_page_config(
    page_title="Executive Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- LOAD DATA ---
@st.cache_data  # Cache the data to improve performance
def load_data():
    data = pd.read_csv("executive_data.csv")
    return data

data = load_data()

# --- PAGE TITLE ---
st.title("📊 Executive Performance Metrics Dashboard")
st.markdown("---")

# --- SIDEBAR FILTERS ---
st.sidebar.header("Dashboard Filters")

# Department Filter
st.sidebar.subheader("Filter by Department")
dept_options = ["All"] + list(data["Department"].unique())
selected_dept = st.sidebar.selectbox("Select Department", dept_options)

# Month Filter
st.sidebar.subheader("Filter by Month")
month_options = ["All"] + list(data["Month"].unique())
selected_month = st.sidebar.selectbox("Select Month", month_options)

# --- FILTER DATASET ---
if selected_dept == "All" and selected_month == "All":
    filtered_data = data
elif selected_dept == "All":
    filtered_data = data[data["Month"] == selected_month]
elif selected_month == "All":
    filtered_data = data[data["Department"] == selected_dept]
else:
    filtered_data = data[
        (data["Department"] == selected_dept) &
        (data["Month"] == selected_month)
    ]

# --- MAINPAGE ---

# 1. KEY METRICS (KPIs)
st.subheader("Key Performance Indicators")

total_sales = filtered_data["Sales"].sum()
avg_performance = filtered_data["Performance"].mean()
total_target = filtered_data["Target"].sum()

# Calculate Sales vs Target in percentage
if total_target > 0:
    sales_vs_target_pct = (total_sales / total_target) * 100
else:
    sales_vs_target_pct = 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,}")
col2.metric("Average Performance", f"{avg_performance:.1f}%")
col3.metric("Sales vs Target", f"{sales_vs_target_pct:.1f}%")

st.markdown("---")

# 2. CHARTS
col1, col2 = st.columns(2)

with col1:
    st.subheader("Employee Performance")
    # Bar Chart: Employee Performance
    fig_bar = px.bar(
        filtered_data,
        x="Employee",
        y="Performance",
        color="Employee",
        title="Employee Performance (%)"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("Sales vs Target")
    # Grouped Bar Chart: Sales vs Target
    sales_target_df = filtered_data.melt(
        id_vars=["Employee"],
        value_vars=["Sales", "Target"],
        var_name="Metric",
        value_name="Amount"
    )
    fig_grouped_bar = px.bar(
        sales_target_df,
        x="Employee",
        y="Amount",
        color="Metric",
        barmode="group",
        title="Employee Sales vs. Target"
    )
    st.plotly_chart(fig_grouped_bar, use_container_width=True)


# 3. FULL DATASET (Optional: as a table)
st.subheader("Raw Data")
st.dataframe(filtered_data)