import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# --- Styling: Font, layout, bold headers, metric cards, background
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Avenir:wght@400;700&family=Helvetica:wght@400;700&display=swap');
html, body, [class*="css"] {
    font-family: 'Avenir', 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
    color: #111 !important;
}
h1, h2, h3, h4, h5, h6 {
    font-weight: bold !important;
    color: #111 !important;
    letter-spacing: -1px;
}
.stApp {
    background: linear-gradient(120deg, #eaffd0 0%, #baff93 100%) !important;
}
[data-testid="metric-container"] {
    background: #fff !important;
    border-radius: 18px;
    box-shadow: 0 2px 16px 0 #baff93aa;
    border: 2px solid #39FF14;
}
.element-container, .stDataFrame {
    background: #fff !important;
    border-radius: 16px;
    box-shadow: 0 4px 24px #39FF1420;
    padding: 1.25em 1.1em !important;
}
</style>
""", unsafe_allow_html=True)

# --- Streamlit config for wide layout and favicon
st.set_page_config(page_title="Hotel Sales BI Dashboard", page_icon="🏨", layout="wide")

# --- Load your data
df = pd.read_excel('output/daily_sales_report.xlsx', sheet_name='Raw Data')
df['arrival_date'] = pd.to_datetime(df['arrival_date'])

# --- Sidebar filters
with st.sidebar:
    st.header("Filters")
    brands = st.multiselect("Hotel Brand", sorted(df['hotel_name'].unique()), default=list(df['hotel_name'].unique()))
    channels = st.multiselect("Sales Channel", sorted(df['dis_channel'].unique()), default=list(df['dis_channel'].unique()))
    date_range = st.date_input("Arrival Date", [df['arrival_date'].min(), df['arrival_date'].max()])
    # For map: choose region/column if available (optional)

# --- Data filter
filtered = df[
    df['hotel_name'].isin(brands) &
    df['dis_channel'].isin(channels) &
    (df['arrival_date'] >= pd.to_datetime(date_range[0])) &
    (df['arrival_date'] <= pd.to_datetime(date_range[1]))
]

# --- Dashboard title/header
st.markdown("""
# 🏨 Hotel Sales Dashboard
_Business Intelligence at a Glance 🚦_
""")
st.markdown("---")

# --- KPIs up top
a, b, c = st.columns(3)
a.metric("Total Sales", f"RM {filtered['sales'].sum():,.0f}")
b.metric("Average ADR", f"RM {filtered['ADR'].mean():,.2f}")
c.metric("Total Bookings", f"{filtered.shape[0]:,}")

# --- Altair: Sales Trend (black line on white card)
st.markdown("#### Sales Trend Over Time")
sales_trend = filtered.groupby('arrival_date')['sales'].sum().reset_index()
trend_chart = alt.Chart(sales_trend).mark_line(color='black', strokeWidth=4).encode(
    x=alt.X('arrival_date:T', title='Date'),
    y=alt.Y('sales:Q', title='Sales')
).properties(
    width=700,
    height=300,
    background='#fff'
).configure_axis(
    labelColor='#111', titleColor='#111'
).configure_title(
    fontSize=20, font='Avenir', color='#111'
)
st.altair_chart(trend_chart, use_container_width=True)

# --- Altair: Sales by Brand (lime bars, black font)
st.markdown("#### Top Brands by Sales")
sales_brand = filtered.groupby('hotel_name')['sales'].sum().sort_values(ascending=False).reset_index()
brand_chart = alt.Chart(sales_brand).mark_bar(
    color="#39FF14",
    cornerRadiusTopLeft=10,
    cornerRadiusTopRight=10
).encode(
    x=alt.X('sales:Q', title='Total Sales (RM)'),
    y=alt.Y('hotel_name:N', sort='-x', title='Brand'),
    tooltip=['hotel_name', 'sales']
).properties(height=340, width=600, background='#fff',
              title="Sales by Brand"
).configure_axis(
    labelColor='#111', titleColor='#111'
).configure_title(
    fontSize=18, font='Avenir', color='#111'
)
st.altair_chart(brand_chart, use_container_width=True)

# --- Altair: Sales by Channel (black bars, white card)
st.markdown("#### Sales by Channel")
sales_channel = filtered.groupby('dis_channel')['sales'].sum().sort_values(ascending=False).reset_index()
channel_chart = alt.Chart(sales_channel).mark_bar(
    color='black',
    cornerRadiusTopLeft=10,
    cornerRadiusTopRight=10
).encode(
    x=alt.X('sales:Q', title='Total Sales (RM)'),
    y=alt.Y('dis_channel:N', sort='-x', title='Channel'),
    tooltip=['dis_channel', 'sales']
).properties(height=260, width=480, background='#fff',
              title="Sales by Channel"
).configure_axis(
    labelColor='#111', titleColor='#111'
).configure_title(
    fontSize=18, font='Avenir', color='#111'
)
st.altair_chart(channel_chart, use_container_width=True)

# --- Plotly: Map Visualization (customize for your data/country)
st.markdown("#### Geographical Sales Indicator")
if 'state_code' in filtered.columns:
    fig = px.choropleth(
        filtered,
        locations='state_code', # e.g. "MY-01", "MY-10"; adapt to your data
        locationmode='ISO-3',   # Change to "USA-states" for US, etc.
        color='sales',
        color_continuous_scale=["#baff93", "#39FF14", "#111"],
        labels={'sales': 'Total Sales'},
        title='Total Sales by Region'
    )
    fig.update_layout(
        geo=dict(bgcolor='rgba(0,0,0,0)', showframe=False, showcoastlines=False),
        margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor='#eaffd0',
        plot_bgcolor='#fff',
        font=dict(family='Avenir, Helvetica, Arial', color='#111')
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Add a region/state/country code column (e.g. 'state_code') for geo sales map!")

# --- Data table expander
with st.expander("Show Raw Data Table"):
    st.dataframe(filtered, use_container_width=True)

# --- About credit expander
with st.expander("About / Data Source"):
    st.markdown("""
    **Data Source:**  
    [Kaggle: Hotel Revenue Dataset](https://www.kaggle.com/datasets/tianrongsim/hotel-sales-2024)

    _This dashboard was designed and built by **BI Girlie** as a modern, portfolio-ready BI showcase.<br>
    **Font:** Avenir/Helvetica · **Theme:** Lime & Black · **Design:** Streamlit, Altair, Plotly._

    [LinkedIn: bhanujakumar313](https://www.linkedin.com/in/bhanujakumar313)
    """, unsafe_allow_html=True)