import streamlit as st
import pandas as pd
import altair as alt

st.markdown("""
<style>
.stApp { background: linear-gradient(120deg, #cfe2f3 0%, #fceabb 100%) !important; background-attachment: fixed;}
html, body, [class*="css"]  { font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;}
[data-testid="metric-container"] { background: #ffffff80; border-radius: 16px; padding: 1.5em 0.5em; margin: 0 0.8em 1.2em 0; box-shadow: 0 2px 12px 0 #b6bbc833; text-align: center;}
[data-testid="metric-container"] > div { font-size: 30px; color: #2e4057; font-weight: 600;}
.block-container { padding-top: 2rem; padding-bottom: 2rem;}
h1, h2, h3, h4 {color: #073763; font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Hotel Sales BI Dashboard", page_icon="🏨", layout="wide")
col1, col2 = st.columns([1, 8])
with col1:
    st.image('your_logo.png', width=80)  # If you have a logo
with col2:
    st.markdown("""# **Hotel Group Sales Dashboard**
_Automated, analytics-rich BI for everyone._  
Made by BI Girlie | [LinkedIn](https://www.linkedin.com/in/bhanujakumar313)
""")
st.markdown("---")

# Data loading
df = pd.read_excel('output/daily_sales_report.xlsx', sheet_name='Raw Data')
df['arrival_date'] = pd.to_datetime(df['arrival_date'])

with st.sidebar:
    st.header("Filters")
    brands = st.multiselect("Hotel Brand", sorted(df['hotel_name'].unique()), default=list(df['hotel_name'].unique()))
    channels = st.multiselect("Sales Channel", sorted(df['dis_channel'].unique()), default=list(df['dis_channel'].unique()))
    dates = st.date_input("Arrival Date", [df['arrival_date'].min(), df['arrival_date'].max()])

filtered = df[
    df['hotel_name'].isin(brands) & 
    df['dis_channel'].isin(channels) & 
    (df['arrival_date'] >= pd.to_datetime(dates[0])) & 
    (df['arrival_date'] <= pd.to_datetime(dates[1]))
]

a, b, c = st.columns(3)
a.metric("Total Sales", f"RM {filtered['sales'].sum():,.0f}")
b.metric("Average ADR", f"RM {filtered['ADR'].mean():,.2f}")
c.metric("Total Bookings", f"{filtered.shape[0]:,}")

st.markdown("### Sales by Brand")
sales_brand = filtered.groupby('hotel_name')['sales'].sum().sort_values(ascending=False).reset_index()
chart_brand = alt.Chart(sales_brand).mark_bar(
    cornerRadiusTopLeft=12,
    cornerRadiusTopRight=12
).encode(
    x=alt.X('sales:Q', title='Total Sales (RM)'),
    y=alt.Y('hotel_name:N', sort='-x', title='Hotel Brand'),
    color=alt.value('#06beb6'),
    tooltip=['hotel_name', 'sales']
).properties(height=400, width=700, title="Top Brands by Sales")
st.altair_chart(chart_brand, use_container_width=True)

st.markdown("### Sales by Channel")
sales_channel = filtered.groupby('dis_channel')['sales'].sum().sort_values(ascending=False).reset_index()
chart_channel = alt.Chart(sales_channel).mark_bar(
    cornerRadiusTopLeft=10,
    cornerRadiusTopRight=10
).encode(
    x=alt.X('sales:Q', title='Total Sales (RM)'),
    y=alt.Y('dis_channel:N', sort='-x', title='Channel'),
    color=alt.value('#fc5185'),
    tooltip=['dis_channel', 'sales']
).properties(height=320, width=520, title="Sales by Channel")
st.altair_chart(chart_channel, use_container_width=True)

st.markdown("### Sales Trend Over Time")
trend = filtered.groupby('arrival_date')['sales'].sum().reset_index()
chart_trend = alt.Chart(trend).mark_line(
    interpolate='monotone', point=True, color='#3081d0'
).encode(
    x=alt.X('arrival_date:T', title='Date'),
    y=alt.Y('sales:Q', title='Daily Sales (RM)'),
    tooltip=['arrival_date', 'sales']
).properties(height=320, width=800, title="Sales Trend Over Time")
st.altair_chart(chart_trend, use_container_width=True)

with st.expander("Show Data Table"):
    st.dataframe(filtered, use_container_width=True)

st.markdown("""
---
Made with ❤️ by BI Girlie who loves turning data into insights.
Hire me please!
[LinkedIn](https://www.linkedin.com/in/bhanujakumar313)
""")