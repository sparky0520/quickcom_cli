from playwright.async_api import async_playwright

async def fetch_zepto_prices(query: str):
    url = f"https://www.zepto.com/search?query={query}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        # Wait for product cards to load
        await page.wait_for_selector('[data-testid="product-card"]', timeout=15000)
        containers = await page.query_selector_all('[data-testid="product-card"]')
        
        results = []

        for container in containers:
            # 🖼 Image URL
            img_el = await container.query_selector('img[data-testid="product-card-image"]')
            img_url = await img_el.get_attribute('src') if img_el else None

            # 🏷 Title
            title_el = await container.query_selector('h5[data-testid="product-card-name"]')
            title_text = await title_el.inner_text() if title_el else None

            # ⚖ Quantity
            quantity_el = await container.query_selector('p[data-testid="product-card-quantity"] span')
            quantity_text = await quantity_el.inner_text() if quantity_el else None

            # 💸 Price
            price_el = await container.query_selector('h4[data-testid="product-card-price"]')
            price_text = await price_el.inner_text() if price_el else None

            results.append({
                "image": img_url,
                "title": title_text.strip() if title_text else None,
                "quantity": quantity_text.strip() if quantity_text else None,
                "price": price_text.strip() if price_text else None,
            })

        await browser.close()
        return results
