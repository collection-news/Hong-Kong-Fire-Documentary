import asyncio
from playwright.async_api import async_playwright
import datetime
import re

def parse_date(text):
    """
    Parses date from text which may contain:
    - Relative time (2小時前, 1日前)
    - Absolute date (YYYY-MM-DD, e.g. 2025-11-26)
    - Absolute date Chinese (YYYY年MM月DD日)
    """
    base_date = datetime.date.today()
    clean_text = " ".join(text.split())
    
    # 1. Relative Time (e.g., 2小時前, 1日前)
    time_match = re.search(r'(\d+)(小時|分鐘|日|天)前', clean_text)
    if time_match:
        val = int(time_match.group(1))
        unit = time_match.group(2)
        
        if unit in ['日', '天']:
            calc_date = base_date - datetime.timedelta(days=val)
            return calc_date
        return base_date # Hours/Minutes ago is today

    # 2. Absolute Date YYYY-MM-DD (e.g., 2025-11-22)
    iso_match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', clean_text)
    if iso_match:
        y, m, d = map(int, iso_match.groups())
        return datetime.date(y, m, d)

    # 3. Absolute Date YYYY年MM月DD日
    abs_match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', clean_text)
    if abs_match:
        y, m, d = map(int, abs_match.groups())
        return datetime.date(y, m, d)

    # 4. Absolute Date Short MM月DD日 (Assume current year)
    short_match = re.search(r'(\d{1,2})月(\d{1,2})日', clean_text)
    if short_match:
        m, d = map(int, short_match.groups())
        return datetime.date(base_date.year, m, d)
        
    return base_date

async def _scrape_async():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--disable-dev-shm-usage', '--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        page = await context.new_page()
        
        results = []
        
        topic_url = "https://news.tvb.com/tc/pearlnews"
        print(f"Visiting topic page: {topic_url}")
        
        excluded_terms = [
            "Cookies", "FAQ", "私隱", "條款", "關於我們", "聯絡我們", "下載", 
            "Facebook", "YouTube", "myTV", "TVB Anywhere", "鄰住買", "Music Group",
            "愛心基金", "APP", "App Store", "Google Play", "Huawei", "Samsung",
            "即時新聞", "專題節目", "新聞追蹤" 
        ]
        
        cutoff_date = datetime.date(2025, 11, 26)
        
        try:
            for attempt in range(3):
                try:
                    await page.goto(topic_url, wait_until="networkidle", timeout=60000)
                    break
                except Exception as e:
                    print(f"Attempt {attempt+1} failed: {e}")
                    if attempt == 2:
                        raise e
                    await asyncio.sleep(5)
            
            max_scrolls = 50 
            last_height = await page.evaluate("document.body.scrollHeight")
            
            should_stop = False
            
            for _ in range(max_scrolls):
                if should_stop:
                    break

                last_links_text = await page.evaluate('''() => {
                    const links = Array.from(document.querySelectorAll('a[href*="/tc/pearlnews/"]'));
                    const lastLinks = links.slice(-15);
                    return lastLinks.map(a => a.innerText);
                }''')
                
                found_old_article = False
                for text in last_links_text:
                    if text:
                        date_obj = parse_date(text)
                        if date_obj < cutoff_date:
                            found_old_article = True
                            print(f"Stopping scroll: Found article from {date_obj} (Cutoff: {cutoff_date})")
                            break
                
                if found_old_article:
                    break

                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(2) 
                
                new_height = await page.evaluate("document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            
            elements = await page.query_selector_all('a')
            processed_links = set()
            
            for el in elements:
                try:
                    title_raw = await el.inner_text()
                    link = await el.get_attribute('href')
                    
                    if link and title_raw:
                        title_clean = " ".join(title_raw.split())
                        
                        if not link.startswith("http"):
                            link = "https://news.tvb.com" + link
                        
                        if "/tc/pearlnews/" in link:
                             title_lines = title_raw.split('\n')
                             if title_lines:
                                 headline = title_lines[0].strip()
                             else:
                                 headline = title_clean
                             
                             if len(headline) < 5:
                                 continue
                                 
                             if any(ex in headline for ex in excluded_terms):
                                 continue

                             keywords = ["Tai Po", "Wang Fuk", "Kwong Fuk", "fire", "blaze", "inferno"]
                             if not any(k.lower() in headline.lower() for k in keywords):
                                 continue
                             
                             article_date = parse_date(title_raw)
                             
                             if article_date < cutoff_date:
                                 continue

                             article_id = None
                             id_match = re.search(r'/([a-f0-9]{24})/', link)
                             if id_match:
                                 article_id = id_match.group(1)
                             
                             unique_key = article_id if article_id else link

                             if unique_key not in processed_links:
                                 results.append({
                                     "date": article_date.strftime("%Y-%m-%d"),
                                     "title": headline,
                                     "link": link
                                 })
                                 processed_links.add(unique_key)
                                 
                except Exception:
                    pass
                    
        except Exception as e:
            print(f"Error visiting topic page: {e}")
            
        await browser.close()
        return results

def scrape():
    try:
        raw_results = asyncio.run(_scrape_async())
    except Exception as e:
        print(f"TVB English Scraper failed: {e}")
        raw_results = []
    
    formatted_results = []
    for r in raw_results:
        formatted_results.append((r['date'], r['title'], r['link']))
        
    return ("TVB News (English)", formatted_results)

if __name__ == "__main__":
    name, res = scrape()
    print(f"Source: {name}")
    for date, title, link in res:
        print(f"[{date}] {title} ({link})")
