from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime
import google_sheets
import time

URLS = [
      "https://chartink.com/screener/bl3-average-directional-index-adx",
  	  "https://chartink.com/screener/bl2-buyrank2-monthly-ichimoku-cloud-cross-2",
	  "https://chartink.com/screener/custom-buyrank2-2",
	  "https://chartink.com/screener/snl6",
	  "https://chartink.com/screener/bl1buyrank1-monthly-weekly-daily-rsi-above-60",
	  "https://chartink.com/screener/s10bullish-for-next-day",
	  "https://chartink.com/screener/copy-stocks-for-f-0",
	  "https://chartink.com/screener/1-longtrend-ve",
	  "https://chartink.com/screener/1a-longtrend-ve-2"
]
 

sheet_id = "1QjvejkKtq0h8trJOAJCPBXGEViD5W_e52HGEvgXmBJg"
worksheet_names = ["p1","p2","p3","p4","p5","p6","p7","p8","p9","p10","p11","p12","p13","p14","p15","p16","p17","p18","p19","p20","p21","p22","p23","p24","p25"]

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
            page.goto(url, wait_until="networkidle")
            time.sleep(3)

            if page.is_visible("text='No records found'"):
                print(f"⚠️ No records found at {url}. Writing 'No Data'.")
                rows = [[""]]
            else:
                try:
                    page.wait_for_selector("div.relative table tbody tr", timeout=60000)
                    table_rows = page.query_selector_all("div.relative table tbody tr")

                    print(f"📥 Extracted {len(table_rows)} rows.")

                    rows = []
                    for row in table_rows:
                        cells = row.query_selector_all("td")
                        row_data = [cell.inner_text().strip() for cell in cells]
                        rows.append(row_data)

                    if len(rows) == 0:
                        print("⚠️ Table found but no rows present. Writing 'No Data'.")
                        rows = [[""]]

                except PlaywrightTimeoutError:
                    print(f"❌ Table not found at {url}. Writing 'No Data'.")
                    rows = [[""]]

            google_sheets.update_google_sheet_by_name(
                sheet_id, worksheet_name, headers, rows
            )

        except PlaywrightTimeoutError:
            print(f"❌ Timeout error at {url}. Writing 'No Data'.")
            google_sheets.update_google_sheet_by_name(
                sheet_id, worksheet_name, headers, [[""]]
            )

        except Exception as e:
            print(f"❌ Unexpected error: {e}. Writing 'No Data'.")
            google_sheets.update_google_sheet_by_name(
                sheet_id, worksheet_name, headers, [[""]]
            )

        finally:
            page.screenshot(path=f"{worksheet_name}_debug.png", full_page=True)
            browser.close()

        now = datetime.now().strftime("Last updated on: %Y-%m-%d %H:%M:%S")
        google_sheets.append_footer(sheet_id, worksheet_name, [now])

        print(f"✅ Worksheet '{worksheet_name}' update finished.")

for index, url in enumerate(URLS):
    scrape_chartink(url, worksheet_names[index])
    print(f"⏱️ Finished updating '{worksheet_names[index]}'")
