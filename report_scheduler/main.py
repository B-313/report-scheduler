import streamlit as st
import pandas as pd

def main():
    data = pd.read_excel('data/sample_data.xlsx')
    data.columns = data.columns.str.strip()

    # === 2. Select Relevant Columns ===

    columns_to_keep = [
        'hotel_name', 'arrival_date', 'departure_date', 'room_type', 'cus_seg',
        'sales', 'gross', 'disc', 'ADR', 'sales_person', 'dis_channel'
    ]
    report_df = data[columns_to_keep].copy()

    # Clean date columns: strip the time info from arrival_date and departure_date
    report_df['arrival_date'] = pd.to_datetime(report_df['arrival_date']).dt.date
    report_df['departure_date'] = pd.to_datetime(report_df['departure_date']).dt.date


    # === 3. KPIs and Summaries ===
    total_sales = report_df['sales'].sum()
    avg_adr = report_df['ADR'].mean()

    # a) Sales by Brand (Hotel)
    sales_by_brand = report_df.groupby('hotel_name', as_index=False)['sales'].sum().sort_values('sales', ascending=False)

    # b) Sales by Channel
    sales_by_channel = report_df.groupby('dis_channel', as_index=False)['sales'].sum().sort_values('sales', ascending=False)

    # c) Bookings by Channel (count)
    bookings_by_channel = report_df['dis_channel'].value_counts().reset_index()
    bookings_by_channel.columns = ['Channel', 'Bookings']

    # d) Sales by Segment
    sales_by_segment = report_df.groupby('cus_seg', as_index=False)['sales'].sum().sort_values('sales', ascending=False)

    # e) Sales by Sales Person
    sales_by_person = report_df.groupby('sales_person', as_index=False)['sales'].sum().sort_values('sales', ascending=False)

    # f) Sales Trend Over Time
    trend_by_date = report_df.groupby('arrival_date', as_index=False)['sales'].sum()

    # === 4. Write to Multi-Sheet Excel Report ===
    with pd.ExcelWriter('output/daily_sales_report.xlsx') as writer:
        report_df.to_excel(writer, sheet_name='Raw Data', index=False)
        sales_by_brand.to_excel(writer, sheet_name='Sales by Brand', index=False)
        sales_by_channel.to_excel(writer, sheet_name='Sales by Channel', index=False)
        bookings_by_channel.to_excel(writer, sheet_name='Bookings by Channel', index=False)
        sales_by_segment.to_excel(writer, sheet_name='Segment Sales', index=False)
        sales_by_person.to_excel(writer, sheet_name='Sales by Person', index=False)
        trend_by_date.to_excel(writer, sheet_name='Sales Trend', index=False)

    # === 5. Print Key Insights to Console ===
    print("="*40)
    print("    DAILY SALES REPORT SUMMARY")
    print("="*40)
    print(f"Total Sales:        RM {total_sales:,.2f}")
    print(f"Average ADR:        RM {avg_adr:,.2f}")
    print("\nSales by Brand (Top 5):")
    print(sales_by_brand.head().to_string(index=False))
    print("\nSales by Channel (Top 5):")
    print(sales_by_channel.head().to_string(index=False))
    print("\nBookings by Channel (Top 5):")
    print(bookings_by_channel.head().to_string(index=False))
    print("\nReport saved to output/daily_sales_report.xlsx")

if __name__ == "__main__":
    main()