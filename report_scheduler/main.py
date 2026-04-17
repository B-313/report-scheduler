import pandas as pd

def main():
    data = pd.read_excel('data/sample_data.xlsx')
    data.columns = data.columns.str.strip()
    columns_to_keep = [
        'hotel_name',
        'arrival_date',
        'departure_date',
        'room_type',
        'cus_seg',
        'sales',
        'gross',
        'disc',
        'ADR',
        'sales_person',
        'dis_channel'
    ]
    
    report_df = data[columns_to_keep]

    # Example insights
    sales_by_hotel = report_df.groupby('hotel_name')['sales'].sum().reset_index().sort_values('sales', ascending=False)
    sales_by_person = report_df.groupby('sales_person')['sales'].sum().reset_index().sort_values('sales', ascending=False)
    
    with pd.ExcelWriter('output/daily_sales_report.xlsx') as writer:
        report_df.to_excel(writer, sheet_name='Raw Data', index=False)
        sales_by_hotel.to_excel(writer, sheet_name='Sales by Hotel', index=False)
        sales_by_person.to_excel(writer, sheet_name='Sales by Person', index=False)

    print("Report saved to output/daily_sales_report.xlsx")
    print("\nHotel Sales:\n", sales_by_hotel.head())
    print("\nSales Person Sales:\n", sales_by_person.head())
    
    # OPTIONAL: Filter for today's date if you only want today's bookings
    # from datetime import datetime
    # today = pd.to_datetime('today').date()
    # report_df['arrival_date'] = pd.to_datetime(report_df['arrival_date'])
    # report_df = report_df[report_df['arrival_date'].dt.date == today]

if __name__ == "__main__":
    main()