from fastapi import FastAPI
from playwright.sync_api import sync_playwright

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/scrape")
def scrape(url: str):

    result = {
        "prix": None,
        "surface": None,
        "adresse": None
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, timeout=60000)
        page.wait_for_timeout(4000)

        try:
            result["prix"] = page.locator('[data-testid="price"]').first.inner_text()
        except:
            pass

        try:
            result["adresse"] = page.locator('[data-testid="sl.location"]').first.inner_text()
        except:
            pass

        try:
            items = page.locator('[data-testid="criteria-item"]').all()

            for item in items:
                txt = item.inner_text()

                if "m²" in txt:
                    result["surface"] = txt

        except:
            pass

        browser.close()

    return result
