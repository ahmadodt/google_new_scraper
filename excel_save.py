import pandas as pd
def save_to_excel_company(data):
    """Saves scraped data into an Excel file named companies_investment_info.xlsx"""
    formatted_data = []
    
    for entry in data:
        company = entry['title']  # Example: Use title as company name
        url = entry['link']
        blog_url = "N/A"  # Assuming no blog URL is directly extracted

        if 'investment_info' in entry:
            investment_info = entry['investment_info']
            equity_checks = ', '.join(map(str, investment_info.get('equity_checks', ['No data found'])))
            megawatts = ', '.join(map(str, investment_info.get('megawatts', ['No data found'])))
            invest_in_solar = investment_info.get('investing_in_solar_parks', False)
        else:
            equity_checks = 'No data found'
            megawatts = 'No data found'
            invest_in_solar = False
        
        formatted_data.append({
            "Company": company,
            "URL": url,
            "Blog URL": blog_url,
            "Investing in Solar Parks": invest_in_solar,
            "Equity Checks": equity_checks,
            "Megawatts": megawatts
        })

    df = pd.DataFrame(formatted_data)
    df.to_excel("output/companies_investment_info.xlsx", index=False)

    print("Results saved to companies_investment_info.xlsx")
