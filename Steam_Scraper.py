from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import pandas as pd 

url = "https://store.steampowered.com/specials"

if __name__ == "__main__":
    with sync_playwright() as p :
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)

        page.wait_for_load_state("networkidle")
        page.evaluate("() => window.scroll(0 , document.body.scrollHeight)")
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_selector("div[class*='salepreviewwidgets_StoreSaleWidgetOuterContainer']")

        # page.screenshot(path="steam.png",full_page=True)

        html = page.inner_html("body")
        tree = HTMLParser(html)

        divs = tree.css("div[class*='salepreviewwidgets_StoreSaleWidgetOuterContainer']")
        print(len(divs))

        empty_list = []
        for d in divs :
            title= d.css_first("div[class*='salepreviewwidgets_StoreSaleWidgetTitle']").text()
            thumbnail= d.css_first("img[class*='CapsuleImage']").attributes.get("src")
            tags= [a.text() for a in d.css("div[class*='StoreSaleWidgetTags'] > a")[:5]]
            release_date= d.css_first("div[class*='WidgetReleaseDateAndPlatformCtn'] > div[class*='StoreSaleWidgetRelease']").text()
            review_score= d.css_first("div[class*='ReviewScoreValue'] > div").text()
            reviewed_by = d.css_first("div[class*='ReviewScoreCount']").text()
            sale_price = d.css_first("div[class*='StoreSalePriceBox']").text()
            original_price= d.css_first("div[class*='StoreOriginalPrice']").text()

            attrs = {"title":title,
                     "thumbnail" :thumbnail,
                     "tags" : tags,
                     "release_date" : release_date,
                     "review_score" : review_score,
                     "reviewed_by" : reviewed_by,
                     "sale_price" : sale_price,
                     "original_price" : original_price
                    }
            empty_list.append(attrs)     
                       

df = pd.DataFrame.from_dict(empty_list)
df.to_csv("steam_specials.csv", index=False)
df.to_json("steam_specials.json", orient="records")
print(df)

