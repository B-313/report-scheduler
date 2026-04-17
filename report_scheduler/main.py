import pandas as pd

def main():
    data = pd.read_excel('data/sample_data.xlsx')
    # data = pd.read_csv('placeholder.csv')   
    
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
        'resv_status',
        'dis_channel'
    ]

    report_df = data[columns_to_keep]
    
    report_df.to_excel('output/daily_sales_report.xlsx', index=False)
    print("Report saved to output/daily_sales_report.xlsx")
    print(report_df.head())
    
    # OPTIONAL: Filter for today's date if you only want today's bookings
    # from datetime import datetime
    # today = pd.to_datetime('today').date()
    # report_df['arrival_date'] = pd.to_datetime(report_df['arrival_date'])
    # report_df = report_df[report_df['arrival_date'].dt.date == today]

if __name__ == "__main__":
    main()