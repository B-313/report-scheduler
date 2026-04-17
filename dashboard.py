import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Hotel Group Monthly Sales Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== PROFESSIONAL CSS ==========
st.markdown("""
<style>
    /* Font & Global */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Background */
    .stApp {
        background: #FFFFFF;
    }
    
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px !important;
    }
    
    /* Typography */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #1D428A !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.03em !important;
    }
    
    h2 {
        font-size: 1rem !important;
        font-weight: 500 !important;
        color: #7F8C8D !important;
        margin-top: 0 !important;
        margin-bottom: 2.5rem !important;
    }
    
    h3 {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #2C3E50 !important;
        margin-top: 2.5rem !important;
        margin-bottom: 1.2rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Month Toggle Buttons */
    .stButton button {
        background: white !important;
        color: #2C3E50 !important;
        border: 1.5px solid #E8EEF7 !important;
        border-radius: 6px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    
    .stButton button:hover {
        background: #F8F9FA !important;
        border-color: #1D428A !important;
        color: #1D428A !important;
    }
    
    /* Active month button (custom class) */
    .month-active button {
        background: #1D428A !important;
        color: white !important;
        border-color: #1D428A !important;
    }
    
    /* KPI Cards */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid #E8EEF7;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    
    [data-testid="metric-container"] > div {
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        color: #7F8C8D !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #1D428A !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    
    /* Chart containers */
    .chart-section {
        background: white;
        border: 1px solid #E8EEF7;
        border-radius: 8px;
        padding: 1.8rem 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    
    /* Insight boxes */
    .insight-box {
        background: #F8F9FA;
        border-left: 4px solid #1D428A;
        padding: 1rem 1.2rem;
        margin: 1.5rem 0;
        border-radius: 4px;
        font-size: 0.9rem;
        line-height: 1.6;
        color: #2C3E50;
    }
    
    .insight-box strong {
        color: #1D428A;
        font-weight: 600;
    }
    
    /* Remove Plotly watermarks */
    .modebar {
        display: none !important;
    }
    
    /* Dividers */
    hr {
        margin: 3rem 0 2rem 0;
        border: none;
        border-top: 1px solid #E8EEF7;
    }
</style>
""", unsafe_allow_html=True)

# ========== DATA LOADING ==========
@st.cache_data
def load_data():
    """Load and preprocess hotel sales data"""
    df = pd.read_excel('data/sample_data.xlsx')
    df.columns = df.columns.str.strip()
    
    # Date processing
    df['arrival_date'] = pd.to_datetime(df['arrival_date'])
    df['departure_date'] = pd.to_datetime(df['departure_date'])
    
    # Calculations
    df['nights'] = (df['departure_date'] - df['arrival_date']).dt.days
    df['nights'] = df['nights'].replace(0, 1)  # Min 1 night
    df['revenue'] = df['price'] * df['nights']
    
    # Time dimensions
    df['month'] = df['arrival_date'].dt.to_period('M')
    df['month_name'] = df['arrival_date'].dt.strftime('%B')
    df['month_year'] = df['arrival_date'].dt.strftime('%B %Y')
    df['year'] = df['arrival_date'].dt.year
    
    # Guest metrics
    df['adult'] = pd.to_numeric(df['adult'], errors='coerce').fillna(0).astype(int)
    df['(child)'] = pd.to_numeric(df['(child)'], errors='coerce').fillna(0).astype(int)
    df['total_guests'] = df['adult'] + df['(child)']
    
    return df

# ========== ANALYTICS FUNCTIONS ==========
def get_month_metrics(df, selected_month):
    """Calculate key metrics for selected month"""
    month_data = df[df['month_year'] == selected_month].copy()
    
    if len(month_data) == 0:
        return None
    
    metrics = {
        'total_revenue': month_data['revenue'].sum(),
        'total_bookings': len(month_data),
        'avg_revenue_per_stay': month_data['revenue'].mean(),
        'total_nights': month_data['nights'].sum(),
        'avg_length_of_stay': month_data['nights'].mean(),
        'total_guests': month_data['total_guests'].sum(),
        'avg_party_size': month_data['total_guests'].mean(),
    }
    
    # Breakdown by dimension
    by_hotel = month_data.groupby('hotel_name')['revenue'].sum().sort_values(ascending=False)
    by_channel = month_data.groupby('dis_channel')['revenue'].sum().sort_values(ascending=False)
    by_segment = month_data.groupby('cus_seg')['revenue'].sum().sort_values(ascending=False)
    by_room = month_data.groupby('room_type')['revenue'].sum().sort_values(ascending=False)
    
    return {
        'metrics': metrics,
        'by_hotel': by_hotel,
        'by_channel': by_channel,
        'by_segment': by_segment,
        'by_room': by_room,
        'raw': month_data
    }

# ========== CHART FUNCTIONS ==========
def create_bar_chart(data, title, x_label, y_label):
    """Create professional horizontal bar chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=data.index,
        x=data.values,
        orientation='h',
        marker=dict(
            color='#1D428A',
            line=dict(color='#1D428A', width=0)
        ),
        text=[f'RM {val:,.0f}' for val in data.values],
        textposition='outside',
        textfont=dict(size=11, color='#2C3E50', family='Inter'),
        hovertemplate='<b>%{y}</b><br>Revenue: RM %{x:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=14, color='#2C3E50', family='Inter', weight=600),
            x=0,
            xanchor='left'
        ),
        xaxis=dict(
            title=None,
            showgrid=True,
            gridcolor='#F0F0F0',
            zeroline=False,
            showticklabels=False
        ),
        yaxis=dict(
            title=None,
            showgrid=False,
            categoryorder='total ascending'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=max(300, len(data) * 50),
        margin=dict(l=20, r=100, t=50, b=20),
        font=dict(family='Inter', color='#2C3E50', size=11),
        hoverlabel=dict(
            bgcolor='white',
            font_size=12,
            font_family='Inter'
        )
    )
    
    return fig

def create_donut_chart(data, title):
    """Create professional donut chart for proportions"""
    fig = go.Figure()
    
    colors = ['#1D428A', '#4C6EB1', '#7A9BC4', '#A8C5D7']
    
    fig.add_trace(go.Pie(
        labels=data.index,
        values=data.values,
        hole=0.5,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(size=12, color='#2C3E50', family='Inter'),
        hovertemplate='<b>%{label}</b><br>Revenue: RM %{value:,.0f}<br>Share: %{percent}<extra></extra>'
    ))
    
    # Add center text
    total = data.sum()
    fig.add_annotation(
        text=f'<b>RM {total/1000:.0f}K</b><br><span style="font-size:11px; color:#7F8C8D;">Total</span>',
        x=0.5, y=0.5,
        font=dict(size=18, color='#1D428A', family='Inter'),
        showarrow=False
    )
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=14, color='#2C3E50', family='Inter', weight=600),
            x=0.5,
            xanchor='center'
        ),
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(family='Inter', color='#2C3E50')
    )
    
    return fig

# ========== MAIN DASHBOARD ==========
def main():
    # Load data
    df = load_data()
    
    # Get available months (sorted chronologically)
    available_months = sorted(df['month_year'].unique(), 
                             key=lambda x: pd.to_datetime(x, format='%B %Y'))
    
    # Initialize session state for selected month
    if 'selected_month' not in st.session_state:
        st.session_state.selected_month = available_months[-1]  # Default to latest month
    
    # ========== HEADER ==========
    st.markdown("# Hotel Group Sales Analytics")
    st.markdown("## Monthly Performance Dashboard")
    
    # ========== MONTH SELECTOR ==========
    st.markdown("### SELECT REPORTING PERIOD")
    
    # Create month buttons in a grid
    cols = st.columns(6)
    for idx, month in enumerate(available_months):
        col = cols[idx % 6]
        with col:
            if st.button(month, key=f'btn_{month}', use_container_width=True):
                st.session_state.selected_month = month
                st.rerun()
    
    st.markdown("---")
    
    # Get selected month data
    selected_month = st.session_state.selected_month
    month_data = get_month_metrics(df, selected_month)
    
    if month_data is None:
        st.error(f"No data available for {selected_month}")
        return
    
    metrics = month_data['metrics']
    
    # ========== SELECTED MONTH HEADER ==========
    st.markdown(f"<h1 style='font-size: 2rem; margin-bottom: 0.3rem;'>{selected_month}</h1>", 
                unsafe_allow_html=True)
    st.markdown(f"<p style='color: #7F8C8D; font-size: 0.95rem; margin-bottom: 2rem;'>"
                f"Analysis of {metrics['total_bookings']:,} bookings across "
                f"{month_data['by_hotel'].count()} properties</p>", 
                unsafe_allow_html=True)
    
    # ========== PRIMARY KPIs ==========
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    kpi1.metric(
        "Total Revenue",
        f"RM {metrics['total_revenue']:,.0f}",
        help="Sum of all booking revenue for the month"
    )
    
    kpi2.metric(
        "Avg Revenue per Stay",
        f"RM {metrics['avg_revenue_per_stay']:,.0f}",
        help="Average revenue generated per booking"
    )
    
    kpi3.metric(
        "Total Bookings",
        f"{metrics['total_bookings']:,}",
        help="Number of reservations in this period"
    )
    
    kpi4.metric(
        "Avg Length of Stay",
        f"{metrics['avg_length_of_stay']:.1f} nights",
        help="Average duration of guest stays"
    )
    
    # ========== PROPERTY PERFORMANCE ==========
    st.markdown("### PROPERTY PERFORMANCE")
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown('<div class="chart-section">', unsafe_allow_html=True)
        fig_hotel = create_bar_chart(
            month_data['by_hotel'],
            "Revenue by Property",
            "Revenue (RM)",
            "Property"
        )
        st.plotly_chart(fig_hotel, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Top property insight
        top_property = month_data['by_hotel'].index[0]
        top_revenue = month_data['by_hotel'].iloc[0]
        top_pct = (top_revenue / metrics['total_revenue']) * 100
        
        st.markdown('<div class="chart-section">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style='padding: 1rem 0;'>
            <h4 style='color: #1D428A; font-size: 1rem; margin-bottom: 1rem; font-weight: 600;'>
                Top Performer
            </h4>
            <p style='font-size: 1.5rem; color: #2C3E50; font-weight: 600; margin-bottom: 0.5rem;'>
                {top_property}
            </p>
            <p style='font-size: 2rem; color: #1D428A; font-weight: 700; margin-bottom: 0.5rem;'>
                RM {top_revenue:,.0f}
            </p>
            <p style='color: #7F8C8D; font-size: 0.9rem;'>
                {top_pct:.1f}% of total revenue
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== CHANNEL & SEGMENT ANALYSIS ==========
    st.markdown("### REVENUE DISTRIBUTION")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-section">', unsafe_allow_html=True)
        fig_channel = create_donut_chart(
            month_data['by_channel'],
            "Distribution Channel Contribution"
        )
        st.plotly_chart(fig_channel, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-section">', unsafe_allow_html=True)
        fig_segment = create_donut_chart(
            month_data['by_segment'],
            "Customer Segment Breakdown"
        )
        st.plotly_chart(fig_segment, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== KEY INSIGHTS ==========
    st.markdown("### KEY INSIGHTS")
    
    # Channel insight
    top_channel = month_data['by_channel'].index[0]
    channel_pct = (month_data['by_channel'].iloc[0] / metrics['total_revenue']) * 100
    
    # Segment insight
    top_segment = month_data['by_segment'].index[0]
    segment_pct = (month_data['by_segment'].iloc[0] / metrics['total_revenue']) * 100
    
    st.markdown(f"""
    <div class="insight-box">
        <strong>Channel Strategy:</strong> {top_channel} accounts for {channel_pct:.1f}% of revenue. 
        {'Consider negotiating improved commission rates given strong performance.' if channel_pct > 40 else 
         'Balanced channel mix reduces dependency risk.'}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="insight-box">
        <strong>Customer Profile:</strong> {top_segment} segment drives {segment_pct:.1f}% of bookings. 
        Average party size is {metrics['avg_party_size']:.1f} guests with {metrics['avg_length_of_stay']:.1f} night stays.
    </div>
    """, unsafe_allow_html=True)
    
    # ========== FOOTER ==========
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #7F8C8D; font-size: 0.85rem; padding: 1.5rem 0 1rem 0;'>
        <strong>Data Source:</strong> Internal Reservation System | 
        <strong>Report Generated:</strong> """ + datetime.now().strftime('%B %d, %Y') + """<br>
        Dashboard by <a href="https://www.linkedin.com/in/bhanujakumar313" target="_blank" 
        style="color: #1D428A; text-decoration: none;">BI Analytics Team</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()