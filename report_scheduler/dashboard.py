import streamlit as st
import pandas as pd

# Load your daily report raw data
df = pd.read_excel('output/daily_sales_report.xlsx', sheet_name='Raw Data')

st.title("Hotel Sales Dashboard")

st.metric("Total Sales", f"RM {df['sales'].sum():,.0f}")
st.metric("Average ADR", f"RM {df['ADR'].mean():.2f}")

# Sales by Brand
st.subheader("Sales by Brand")
st.bar_chart(df.groupby('hotel_name')['sales'].sum())

# Sales by Channel
st.subheader("Sales by Channel")
st.bar_chart(df.groupby('dis_channel')['sales'].sum())

# Optional: Show Data Table
st.subheader("Raw Data Preview")
st.dataframe(df.head())