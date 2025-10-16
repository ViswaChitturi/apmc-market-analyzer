import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import date, timedelta
from districts import STATE_DISTRICTS # <-- IMPORT the district data

# --- CONFIGURATION CONSTANTS ---
DAYS_TO_SCRAPE = 4 # Number of past days to scrape to find data

# --- HELPER & SCRAPING FUNCTIONS ---

def find_best_match(user_input, options_list):
    """
    Finds the correct-casing version of a user's input from a list of options.
    """
    user_input_lower = user_input.lower().strip()
    for option in options_list:
        if option.lower() == user_input_lower:
            return option
    return None

def get_available_options(driver, dropdown_id):
    """Gets a list of all available options from a dropdown menu."""
    try:
        dropdown = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, dropdown_id))
        )
        select = Select(dropdown)
        return [option.text for option in select.options[1:]]
    except TimeoutException:
        print(f"Error: Could not find the dropdown with ID '{dropdown_id}'. The page may have changed.")
        return []

def scrape_data_for_date(driver, wait, commodity, target_date):
    """Scrapes market data for a specific commodity on a specific date."""
    market_data = []
    date_str = target_date.strftime('%d-%b-%Y')
    print(f"\nFetching data for {date_str}...")
    try:
        date_input = wait.until(EC.presence_of_element_located((By.ID, 'txtDate')))
        commodity_dropdown = wait.until(EC.presence_of_element_located((By.ID, 'ddlCommodity')))
        go_button = wait.until(EC.element_to_be_clickable((By.ID, 'btnGo')))

        driver.execute_script(f"arguments[0].value = '{date_str}';", date_input)
        Select(commodity_dropdown).select_by_visible_text(commodity)
        go_button.click()

        table = wait.until(EC.presence_of_element_located((By.ID, 'cphBody_GridPriceData')))
        rows = table.find_elements(By.TAG_NAME, 'tr')[1:]
        
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            if len(cells) > 9:
                market_data.append({
                    'District': cells[1].text.strip(), 'Market': cells[2].text.strip(),
                    'Commodity': cells[3].text.strip(), 'Variety': cells[4].text.strip(),
                    'Grade': cells[5].text.strip(), 'Min_Price_Quintal': cells[6].text.strip(),
                    'Max_Price_Quintal': cells[7].text.strip(), 'Modal_Price_Quintal': cells[8].text.strip(),
                    'Arrival_Date': cells[9].text.strip()
                })
        print(f"Found {len(rows)} market entries.")
    except TimeoutException:
        print(f"No data table found for this combination, skipping.")
    except NoSuchElementException:
        print(f"Could not select a form element, skipping.")
    return market_data

# --- DATA ANALYSIS & REPORTING FUNCTION ---

def analyze_and_report(all_market_data, state, commodity):
    """Takes the raw scraped data, filters it by state, and prints a formatted analysis report."""
    if not all_market_data:
        print("\nNo data was scraped. Cannot generate a report.")
        return

    df = pd.DataFrame(all_market_data)
    price_cols = ['Min_Price_Quintal', 'Max_Price_Quintal', 'Modal_Price_Quintal']
    df[price_cols] = df[price_cols].apply(pd.to_numeric, errors='coerce')
    df['Arrival_Date'] = pd.to_datetime(df['Arrival_Date'], format='%d %b %Y', errors='coerce')
    df.dropna(subset=['Modal_Price_Quintal', 'Arrival_Date'], inplace=True)

    target_districts = STATE_DISTRICTS.get(state)
    if not target_districts:
        print(f"\nWarning: District list for '{state}' is not defined in the script.")
        print("The report will be based on all data scraped, which may include other states.")
        state_df = df.copy()
    else:
        print(f"\nFiltering {len(df)} records for districts in {state}...")
        district_pattern = r'\b(?:' + '|'.join(target_districts) + r')\b'
        state_df = df[df['District'].str.contains(district_pattern, case=False, na=False, regex=True)].copy()

    if state_df.empty:
        print(f"\nNo valid data found for {commodity} in {state} in the recent past.")
        return
    
    unique_dates = sorted(state_df['Arrival_Date'].unique(), reverse=True)
    if not unique_dates:
        print("No valid dates found in the filtered data.")
        return

    most_recent_date = unique_dates[0]
    latest_data = state_df[state_df['Arrival_Date'] == most_recent_date]

    print("\n" + "="*60)
    print(" " * 15 + "LIVE MARKET INTELLIGENCE REPORT")
    print("="*60)
    print(f"INFO: The most recent data for {state} is from {pd.to_datetime(most_recent_date).strftime('%A, %d-%b-%Y')}.")
    print("-"*60)

    print(f"\n--- Market Report for {pd.to_datetime(most_recent_date).strftime('%d-%b-%Y')} ---")
    avg_price_latest = latest_data['Modal_Price_Quintal'].mean()
    highest = latest_data.loc[latest_data['Modal_Price_Quintal'].idxmax()]
    lowest = latest_data.loc[latest_data['Modal_Price_Quintal'].idxmin()]
    
    print(f"Commodity:      {commodity}")
    print(f"State:          {state}")
    print(f"Average Price:  ₹{avg_price_latest:,.2f} per Quintal")
    print(f"Highest Price:  ₹{highest['Modal_Price_Quintal']:,.2f} in {highest['Market']}, {highest['District']}")
    print(f"Lowest Price:   ₹{lowest['Modal_Price_Quintal']:,.2f} in {lowest['Market']}, {lowest['District']}")

    if len(unique_dates) > 1:
        previous_date = unique_dates[1]
        previous_data = state_df[state_df['Arrival_Date'] == previous_date]
        if not previous_data.empty:
            avg_price_previous = previous_data['Modal_Price_Quintal'].mean()
            price_change = avg_price_latest - avg_price_previous
            trend = "UP" if price_change > 0 else "DOWN"
            
            print("\n--- Market Price Trend ---")
            print(f"Comparing the two most recent days with available data:")
            print(f"Previous Day ({pd.to_datetime(previous_date).strftime('%d-%b-%Y')}): ₹{avg_price_previous:,.2f}")
            print(f"Latest Day ({pd.to_datetime(most_recent_date).strftime('%d-%b-%Y')}):   ₹{avg_price_latest:,.2f}")
            print(f"Trend: {trend} by ₹{abs(price_change):,.2f}")
    else:
        print("\nNot enough historical data available to compare trends.")
    print("="*60)

# --- MAIN WORKFLOW ---

def main():
    """Main function to orchestrate the scraper and analysis tool."""
    state_codes = {
        "Andaman and Nicobar": "01", "Andhra Pradesh": "02", "Arunachal Pradesh": "25",
        "Assam": "03", "Bihar": "04", "Chandigarh": "05", "Chattisgarh": "26",
        "Dadra and Nagar Haveli": "27", "Daman and Diu": "28", "NCT of Delhi": "07",
        "Goa": "08", "Gujarat": "09", "Haryana": "10", "Himachal Pradesh": "11",
        "Jammu and Kashmir": "12", "Jharkhand": "29", "Karnataka": "13", "Kerala": "14",
        "Lakshadweep": "15", "Madhya Pradesh": "16", "Maharashtra": "17", "Manipur": "18",
        "Meghalaya": "19", "Mizoram": "20", "Nagaland": "21", "Odisha": "22",
        "Pondicherry": "23", "Punjab": "24", "Rajasthan": "30", "Sikkim": "31",
        "Tamil Nadu": "32", "Telangana": "36", "Tripura": "33", "Uttar Pradesh": "34",
        "Uttarakhand": "35", "West Bengal": "37"
    }
    
    print("--- All-India APMC Market Intelligence Tool ---")
    print("\nAvailable States:")
    for state in state_codes.keys():
        print(f"- {state}")
        
    state_input = input("\nEnter the State you want to analyze (e.g., Andhra Pradesh):\n> ")
    matched_state = find_best_match(state_input, state_codes.keys())
    
    if not matched_state:
        print(f"Error: State '{state_input}' not found. Please check spelling and try again.")
        return
        
    state_code = state_codes[matched_state]
    url = f"https://agmarknet.gov.in/SearchCmmMkt.aspx?st={state_code}"
    
    print(f"\n--- Launching browser to fetch data for {matched_state}... ---")
    options = webdriver.ChromeOptions()
    # --- ENABLED BY DEFAULT ---
    # Comment out the line below to see the browser window for debugging
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    scraped_data = []
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 30)
        
        print("\nDiscovering available commodities from the website...")
        available_commodities = get_available_options(driver, 'ddlCommodity')
        if not available_commodities:
            raise Exception("Could not fetch commodity list. The site may be down or has changed.")
        
        commodity_input = input("Enter the commodity for analysis (e.g., Paddy(Dhan)(Common)):\n> ")
        matched_commodity = find_best_match(commodity_input, available_commodities)
        
        if not matched_commodity:
            print(f"\nError: Commodity '{commodity_input}' not found in the list for {matched_state}.")
            return

        today = date.today()
        dates_to_scrape = [today - timedelta(days=i) for i in range(DAYS_TO_SCRAPE)]
        
        for target_date in dates_to_scrape:
            driver.get(url) 
            daily_data = scrape_data_for_date(driver, wait, matched_commodity, target_date)
            scraped_data.extend(daily_data)
            
    except Exception as e:
        print(f"\nAn unexpected error occurred during scraping: {e}")
    finally:
        print("\nClosing browser...")
        driver.quit()

    analyze_and_report(scraped_data, matched_state, matched_commodity)

if __name__ == "__main__":
    main()

