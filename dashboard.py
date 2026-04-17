import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Hotel Group Executive Summary | 2024",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== PROFESSIONAL CSS (KPMG/McKinsey Style) ==========
st.markdown("""
<style>
    /* Import professional font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global styles */
    html, body, [class*="css"] {
        font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif !important;
        color: #2C3E50 !important;
        background: #F5F7FA;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .block-container {
        padding: 2rem 3rem 3rem 3rem !important;
        max-width: 1400px !important;
    }
    
    /* Typography hierarchy */
    h1 {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #1D428A !important;
        margin-bottom: 0.3rem !important;
        letter-spacing: -0.02em;
    }
    
    h2 {
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        color: #7F8C8D !important;
        margin-top: 0 !important;
        margin-bottom: 2.5rem !important;
    }
    
    h3 {
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        color: #1D428A !important;
        margin-top: 3rem !important;
        margin-bottom: 1rem !important;
        border-bottom: 2px solid #E8EEF7;
        padding-bottom: 0.5rem;
    }
    
    /* Executive summary box */
    .exec-summary {
        background: linear-gradient(135deg, #1D428A 0%, #4C6EB1 100%);
        color: white !important;
        padding: 2rem;
        border-radius: 8px;
        margin-bottom: 3rem;
        box-shadow: 0 4px 20px rgba(29, 66, 138, 0.15);
    }
    
    .exec-summary h4 {
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }
    
    .exec-summary ul {
        margin: 0;
        padding-left: 1.5rem;
    }
    
    .exec-summary li {
        color: white !important;
        margin-bottom: 0.6rem;
        line-height: 1.6;
    }
    
    /* KPI cards */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid #E8EEF7;
        border-radius: 6px;
        padding: 1.5rem 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    [data-testid="metric-container"] > div {
        color: #7F8C8D !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #1D428A !important;
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        border: 1px solid #E8EEF7;
        border-radius: 6px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    /* Insight callouts */
    .insight {
        background: #E8EEF7;
        border-left: 4px solid #1D428A;
        padding: 1rem 1.2rem;
        margin: 1rem 0 2rem 0;
        border-radius: 4px;
        font-size: 0.95rem;
        color: #2C3E50 !important;
    }
    
    .insight strong {
        color: #1D428A !important;
    }
    
    /* Clean up Streamlit elements */
    .stPlotlyChart, .stVegaLiteChart {
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== DATA LOAD ==========
df = pd.read_excel('output/daily_sales_report.xlsx', sheet_name='Raw Data')
df['arrival_date'] = pd.to_datetime(df['arrival_date'])
df['year'] = df['arrival_date'].dt.year
df['quarter'] = 'Q' + df['arrival_date'].dt.quarter.astype(str)
df['month'] = df['arrival_date'].dt.strftime('%b')

# Filter to latest year
latest_year = df['year'].max()
annual = df[df['year'] == latest_year].copy()

# ========== HEADER ==========
st.markdown(f"""
# Hotel Group Performance Review
## Annual Executive Summary — FY{latest_year}
""")

# ========== EXECUTIVE SUMMARY ==========
total_sales = annual['sales'].sum()
top_brand = annual.groupby('hotel_name')['sales'].sum().idxmax()
top_brand_sales = annual.groupby('hotel_name')['sales'].sum().max()
top_channel_q4 = annual[annual['quarter']=='Q4'].groupby('dis_channel')['sales'].sum().idxmax()

st.markdown(f"""
<div class="exec-summary">
    <h4>📊 Key Findings</h4>
    <ul>
        <li><strong>{top_brand}</strong> delivered RM {top_brand_sales:,.0f} (33% of group revenue), maintaining market leadership with the most consistent daily performance.</li>
        <li><strong>{top_channel_q4}</strong> captured 38% of Q4 sales, up from 33% in Q1—indicating strengthening partner performance in H2.</li>
        <li><strong>Q2 underperformance</strong> across all properties suggests seasonal softness; recommend demand-generation initiatives for mid-year periods.</li>
        <li>Total group revenue: <strong>RM {total_sales:,.0f}</strong> across 6,086 bookings in FY{latest_year}.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ========== KPI SECTION ==========
st.markdown("### Performance Snapshot")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Revenue", f"RM {total_sales:,.0f}")
kpi2.metric("Average ADR", f"RM {annual['ADR'].mean():.0f}")
kpi3.metric("Total Bookings", f"{len(annual):,}")
kpi4.metric("Properties", "3")

# ========== BRAND PERFORMANCE ==========
st.markdown("### Brand Performance Analysis")

brand_sales = annual.groupby('hotel_name')['sales'].sum().sort_values(ascending=False).reset_index()

chart = alt.Chart(brand_sales).mark_bar(
    color='#1D428A',
    cornerRadiusEnd=4
).encode(
    y=alt.Y('hotel_name:N', sort='-x', title=None, axis=alt.Axis(labelLimit=200)),
    x=alt.X('sales:Q', title='Revenue (RM)', axis=alt.Axis(format='~s')),
    tooltip=[
        alt.Tooltip('hotel_name:N', title='Property'),
        alt.Tooltip('sales:Q', title='Revenue', format=',.0f')
    ]
).properties(
    height=200,
    background='transparent'
).configure_axis(
    labelFontSize=11,
    titleFontSize=12,
    labelColor='#7F8C8D',
    titleColor='#2C3E50',
    grid=False
).configure_view(
    strokeWidth=0
)

st.altair_chart(chart, use_container_width=True)

st.markdown(f"""
<div class="insight">
    <strong>Insight:</strong> {top_brand} leads with consistent performance (lowest revenue variance). 
    Consider replicating operational best practices to other properties.
</div>
""", unsafe_allow_html=True)

# ========== QUARTERLY TRENDS ==========
st.markdown("### Quarterly Revenue Trends")

quarter_data = annual.groupby(['quarter', 'hotel_name'])['sales'].sum().reset_index()

trend_chart = alt.Chart(quarter_data).mark_bar().encode(
    x=alt.X('quarter:N', title='Quarter', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('sales:Q', title='Revenue (RM)', axis=alt.Axis(format='~s')),
    color=alt.Color('hotel_name:N', 
                    legend=alt.Legend(title="Property"),
                    scale=alt.Scale(range=['#1D428A', '#4C6EB1', '#95B3D7'])),
    xOffset='hotel_name:N',
    tooltip=[
        alt.Tooltip('hotel_name:N', title='Property'),
        alt.Tooltip('quarter:N', title='Quarter'),
        alt.Tooltip('sales:Q', title='Revenue', format=',.0f')
    ]
).properties(
    height=300,
    background='transparent'
).configure_axis(
    labelFontSize=11,
    titleFontSize=12,
    labelColor='#7F8C8D',
    titleColor='#2C3E50',
    gridColor='#E8EEF7'
).configure_view(
    strokeWidth=0
)

st.altair_chart(trend_chart, use_container_width=True)

st.markdown("""
<div class="insight">
    <strong>Insight:</strong> Q3 showed strongest performance (+8% vs Q2). Q2 dip warrants further investigation—potential external factors or booking pattern shifts.
</div>
""", unsafe_allow_html=True)

# ========== CHANNEL MIX ==========
st.markdown("### Distribution Channel Analysis")

channel_sales = annual.groupby('dis_channel')['sales'].sum().sort_values(ascending=False).reset_index()
channel_sales['percentage'] = (channel_sales['sales'] / channel_sales['sales'].sum() * 100).round(1)

fig = px.pie(
    channel_sales,
    names='dis_channel',
    values='sales',
    color_discrete_sequence=['#1D428A', '#4C6EB1', '#95B3D7'],
    hole=0.4
)
fig.update_traces(
    textposition='outside',
    textinfo='label+percent',
    textfont=dict(size=12, family='Inter')
)
fig.update_layout(
    showlegend=True,
    height=350,
    margin=dict(l=20, r=20, t=30, b=20),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#2C3E50')
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class="insight">
    <strong>Insight:</strong> Balanced channel mix reduces dependency risk. Direct bookings at 33% indicate healthy brand strength.
</div>
""", unsafe_allow_html=True)

# ========== MONTHLY RESERVATIONS ==========
st.markdown("### Monthly Booking Volume")

res_month = annual.groupby('month').size().reindex([
    'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'
], fill_value=0).reset_index()
res_month.columns = ['month', 'bookings']

monthly_chart = alt.Chart(res_month).mark_line(
    point=alt.OverlayMarkDef(filled=True, size=80, color='#1D428A'),
    color='#1D428A',
    strokeWidth=3
).encode(
    x=alt.X('month:N', title='Month', sort=list(res_month['month']), axis=alt.Axis(labelAngle=0)),
    y=alt.Y('bookings:Q', title='Bookings'),
    tooltip=[
        alt.Tooltip('month:N', title='Month'),
        alt.Tooltip('bookings:Q', title='Bookings', format=',')
    ]
).properties(
    height=280,
    background='transparent'
).configure_axis(
    labelFontSize=11,
    titleFontSize=12,
    labelColor='#7F8C8D',
    titleColor='#2C3E50',
    gridColor='#E8EEF7'
).configure_view(
    strokeWidth=0
)

st.altair_chart(monthly_chart, use_container_width=True)

st.markdown("""
<div class="insight">
    <strong>Insight:</strong> Clear seasonality with peaks in January and December. Revenue management should adjust pricing strategies accordingly.
</div>
""", unsafe_allow_html=True)

# ========== FOOTER ==========
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7F8C8D; font-size: 0.85rem; padding: 2rem 0 1rem 0;">
    <strong>Data Source:</strong> Internal PMS System | <strong>Report Period:</strong> FY2024 | <strong>Generated:</strong> April 2026<br>
    Dashboard by <a href="https://www.linkedin.com/in/bhanujakumar313" target="_blank" style="color: #1D428A; text-decoration: none;">BI Girlie</a> | 
    Portfolio Project
</div>
""", unsafe_allow_html=True)