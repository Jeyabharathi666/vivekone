from playwright.sync_api import sync_playwright
from datetime import datetime
import google_sheets  # assumes you have this module ready like in your Economic Times script
import time
URL = ["https://chartink.com/screener/copy-atp-above-long-fut1",
       "https://chartink.com/screener/copy-nr-f-0",
       "https://chartink.com/screener/copy-f-0-6",
       "https://chartink.com/screener/positional-f-0-at-3-00",
       "https://chartink.com/screener/copy-stocks-for-f-0",
       "https://chartink.com/screener/copy-nr7-atfinallynitin-f-0",
       "https://chartink.com/screener/copy-f-o-rsi-84",
       "https://chartink.com/screener/copy-copy-daily-min-f-0-trade-2",
       "https://chartink.com/screener/rk-position-f-0",
       "https://chartink.com/screener/copy-richie-rich-f-0-2",
       "https://chartink.com/screener/copy-f-0-future",
       "https://chartink.com/screener/copy-13579-swing-trading-by-trading-executive-2338",
       "https://chartink.com/screener/copy-atr-volume-f-o-200-577",
       "https://chartink.com/screener/mms-rb",
       "https://chartink.com/screener/w6-wsma20",
       "https://chartink.com/screener/vikram-rocket-up-nr7",
       "https://chartink.com/screener/copy-copy-copy-rocket-booster-1-4",
       "https://chartink.com/screener/atr-volume-f-o-200-wkly-rsi",
       "https://chartink.com/screener/copy-stocks-in-downtrend-1959",
       "https://chartink.com/screener/copy-super-bearish-f-0-rsp-114",
       "https://chartink.com/screener/f-0-sell",
       "https://chartink.com/screener/copy-bearish-f-0",
       "https://chartink.com/screener/copy-sell-f-0",
       "https://chartink.com/screener/gfs-rsi-scan-8",
       "https://chartink.com/screener/2-day-range-bound-f-o",
       "https://chartink.com/screener/copy-copy-rsi-macd-f-o-sell-scan",
       "https://chartink.com/screener/copy-strong-stocks-3419", 
       "https://chartink.com/screener/copy-w6-f-o-2",
       "https://chartink.com/screener/down-1273"]
       
sheet_id = "1QjvejkKtq0h8trJOAJCPBXGEViD5W_e52HGEvgXmBJg"
worksheet_name = ["p1","p2","p3","p4","p5","p6","p7","p8","p9","p10","p11","p12","p13","p14","p15","p16","p17","p18","p19","p20","p21","p22","p23","p24","p25","p26","p27","p28","p29"]
       
def scrape_chartink(URL, worksheet_name):
    print(f"🚀 Starting Chartink scrape for {worksheet_name}...")
    print(f"🌐 Loading: {URL}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
        page = context.new_page()
        page.goto(URL)

        print("📊 Waiting for table to load...")
        page.wait_for_selector("table.table-striped.scan_results_table tbody tr", timeout=15000)
        time.sleep(3)  # allow time for AJAX rows to load

        page.screenshot(path=f"{worksheet_name}_debug.png", full_page=True)

        table_rows = page.query_selector_all("table.table-striped.scan_results_table tbody tr")
        print(f"📥 Extracted {len(table_rows)} rows. Updating Google Sheet...")

        headers = ["Sr", "Stock Name", "Symbol", "Links", "Change", "Price", "Volume"]
        rows = []
        for row in table_rows:
            cells = row.query_selector_all("td")
            row_data = [cell.inner_text().strip() for cell in cells]
            rows.append(row_data)

        # Update Sheet
        google_sheets.update_google_sheet_by_name(sheet_id, worksheet_name, headers, rows)

        # Add Timestamp
        now = datetime.now().strftime("Last updated on: %Y-%m-%d %H:%M:%S")
        google_sheets.append_footer(sheet_id, worksheet_name, [now])

        browser.close()
        print(f"✅ Google Sheet '{worksheet_name}' updated.")


for i in URL:
    scrape_chartink(i,worksheet_name[URL.index(i)])
    print(worksheet_name[URL.index(i)]," updated")
