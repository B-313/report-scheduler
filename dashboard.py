import streamlit as st
import pandas as pd
from PIL import Image

# --- Branding/hero banner ---
st.set_page_config(page_title="Hotel Sales Insight Dashboard", page_icon="📊", layout="wide")

col1, col2 = st.columns([1,5])
with col1:
    logo = Image.open("your_logo.png")  # Optional: Place a PNG in the same folder
    st.image(logo, width=80)
with col2:
    st.title("Hotel Sales Insight Dashboard")
    st.write("_Automated Daily Insights for Multi-Brand Hotels in Malaysia_")
    st.write("**By: Your Name | [LinkedIn](https://www.linkedin.com/in/yourprofile/)**")

st.markdown("---")

# --- Data loading ---
df = pd.read_excel('output/daily_sales_report.xlsx', sheet_name='Raw Data')
df['arrival_date'] = pd.to_datetime(df['arrival_date'])

# --- Filters ---
brands = st.multiselect("Select Brand(s):", options=sorted(df['hotel_name'].unique()), default=list(df['hotel_name'].unique()))
channels = st.multiselect("Select Channel(s):", options=sorted(df['dis_channel'].unique()), default=list(df['dis_channel'].unique()))
date_range = st.date_input("Arrival Date Range", [df['arrival_date'].min(), df['arrival_date'].max()])

# Filter logic
filtered_df = df[
    df['hotel_name'].isin(brands) & 
    df['dis_channel'].isin(channels) & 
    (df['arrival_date'] >= pd.to_datetime(date_range[0])) & (df['arrival_date'] <= pd.to_datetime(date_range[1]))
]

# --- KPIs ---
st.markdown("### Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"RM {filtered_df['sales'].sum():,.0f}")
col2.metric("Average ADR", f"RM {filtered_df['ADR'].mean():.2f}")
col3.metric("Bookings", f"{filtered_df.shape[0]:,.0f}")

# --- Charts ---
st.markdown("### Sales Breakdown")
st.bar_chart(filtered_df.groupby("hotel_name")["sales"].sum())
st.bar_chart(filtered_df.groupby("dis_channel")["sales"].sum())

st.line_chart(filtered_df.groupby("arrival_date")["sales"].sum())

# --- Data Table (toggle) ---
with st.expander("Show Raw Data Table"):
    st.dataframe(filtered_df)

# --- About/Contact ---
st.markdown("""
---
**About:**  
Automated BI dashboard for multi-brand hotel group in Malaysia.  
Features: Daily data refresh, actionable sales KPIs, channel/brand/period drilldown, and auto-generated reporting.

_Designed & developed by Your Name_  
[View the source code on GitHub](https://github.com/YourUsername/report-scheduler)
""")