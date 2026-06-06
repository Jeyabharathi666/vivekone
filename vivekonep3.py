'''from playwright.sync_api import sync_playwright
from datetime import datetime
import google_sheets  # assumes you have this module ready like in your Economic Times script
import time
URL = ["https://chartink.com/screener/copy-bearish-engulifing-see-after-3-15-pm-for-next-day-trade-5168",	
      "https://chartink.com/screener/copy-bearish-maribozu-337",
 	  "https://chartink.com/screener/copy-yesterday-and-today-ema3-without-open-high-bearish-55",
 	  "https://chartink.com/screener/copy-bearish-engulfing-moderate-478",
	  "https://chartink.com/screener/agp-bearong-2",
	  "https://chartink.com/screener/shesha-bearish1",
	  "https://chartink.com/screener/agp-shesha-bearish-2",
	  "https://chartink.com/screener/one-rupee-sidh-f-0-sell",
	  "https://chartink.com/screener/copy-f-o-weak-stocks-2",
	  "https://chartink.com/screener/svp2-closing-3-up-since-3-days",
	  "https://chartink.com/screener/copy-copy-how-to-find-future-and-option-stocks-buy-entry-future-3",
	  "https://chartink.com/screener/copy-stocks-in-downtrend-1959",
	  "https://chartink.com/screener/copy-w6-f-o-2",
	  "https://chartink.com/screener/copy-1week-sell-twist",
	  "https://chartink.com/screener/copy-weekly-bollinger-sell-3",
	  "https://chartink.com/screener/sell-postesttttttttttttttttt",
	  "https://chartink.com/screener/copy-cci-below-100-62",
	  "https://chartink.com/screener/copy-bearish-rsi-stoc-1215".
	  "https://chartink.com/screener/srf-narayana-futures-positional-bearish",
	  "https://chartink.com/screener/sell-bollinger-band-weekly-15
	  "https://chartink.com/screener/copy-bolinger-band-bearish-reversal-aps-401
	  "https://chartink.com/screener/copy-ut-sell-eod-basis-5",
	  "https://chartink.com/screener/copy-sell-f-0",
	  "https://chartink.com/screener/copy-perfect-bearish-3266",
	  "https://chartink.com/screener/50-bearish-engulifing-see-after-3-15-pm-for-next-day-trade",
	  "https://chartink.com/screener/50aaaagp-shesha-bearish-2",
	  "https://chartink.com/screener/50stocks-in-downtrend",
	  "https://chartink.com/screener/copy-perfect-bearish-3537",
	  "https://chartink.com/screener/copy-chanakya-bearish-scanner-working-2803"
	]
       
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
'''

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime
import google_sheets
import time

URLS = [
    
     "https://chartink.com/screener/copy-the-best-btst-193",	
     "https://chartink.com/screener/22-nw-shesha-magic-buy-love",	
     "https://chartink.com/screener/copy-richie-rich-f-0-2",	
     "https://chartink.com/screener/all-u1-nk-sir-s-uptrend-stocks-all-time-uptrend",
     "https://chartink.com/screener/copy-sjbl6ch-shesha-buy-bollinger-band-weekly",
     "https://chartink.com/screener/copy-copy-bb-blaster-2",
     "https://chartink.com/screener/copy-atr-volume-f-o-200-wkly-rsi-70-16"     
]

sheet_id = "1QjvejkKtq0h8trJOAJCPBXGEViD5W_e52HGEvgXmBJg"
worksheet_names = [
    "p1","p2","p3","p4","p5","p6","p7"
]

def scrape_chartink(url, worksheet_name):
    print(f"\n🚀 Starting scrape for '{worksheet_name}'")
    print(f"🌐 Loading URL: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        headers = ["Sr", "Stock Name", "Symbol", "Links", "Change", "Price", "Volume"]

        try:
            page.goto(url, wait_until='networkidle')
            page.screenshot(path=f"{worksheet_name}_page_loaded.png", full_page=True)

            time.sleep(3)  # Allow AJAX content to load

            if page.is_visible("text='No records found'"):
                print(f"⚠️ No records found at {url}. Writing 'No Data'.")
                rows = [[" "]]
            else:
                try:
                   #page.wait_for_selector("div.relative table tbody tr", timeout=60000)
                    #table_rows = page.query_selector_all("div.relative table tbody tr")
                    page.wait_for_selector("div.relative div.overflow-x-auto table tbody tr",timeout=60000)
                    table_rows = page.query_selector_all("div.relative div.overflow-x-auto table tbody tr")
                    print(f"📥 Extracted {len(table_rows)} rows.")

                    rows = []
                    for row in table_rows:
                        cells = row.query_selector_all("td")
                        row_data = [cell.inner_text().strip() for cell in cells]
                        rows.append(row_data)

                    if len(rows) == 0:
                        print(f"⚠️ Table found but no rows present. Writing 'No Data'.")
                        rows = [[" "]]

                except PlaywrightTimeoutError:
                    print(f"❌ Table not found at {url}. Writing 'No Data'.")
                    rows = [[" "]]

            google_sheets.update_google_sheet_by_name(sheet_id, worksheet_name, headers, rows)

        except PlaywrightTimeoutError:
            print(f"❌ Timeout error at {url}. Writing 'No Data'.")
            rows = [[" "]]
            google_sheets.update_google_sheet_by_name(sheet_id, worksheet_name, headers, rows)

        except Exception as e:
            print(f"❌ Unexpected error: {e}. Writing 'No Data'.")
            rows = [[" "]]
            google_sheets.update_google_sheet_by_name(sheet_id, worksheet_name, headers, rows)

        finally:
            page.screenshot(path=f"{worksheet_name}_debug.png", full_page=True)
            browser.close()

        now = datetime.now().strftime("Last updated on: %Y-%m-%d %H:%M:%S")
        google_sheets.append_footer(sheet_id, worksheet_name, [now])

        print(f"✅ Worksheet '{worksheet_name}' update finished.")

for index, url in enumerate(URLS):
    scrape_chartink(url, worksheet_names[index])
    print(f"⏱️ Finished updating '{worksheet_names[index]}'")
