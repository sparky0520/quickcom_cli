from playwright.async_api import async_playwright

async def fetch_swiggy_prices(query: str):
    url = f"https://www.swiggy.com/instamart/search?custom_back=true&query={query}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        # Wait until the product cards are available
        await page.wait_for_selector('[data-testid="default_container_ux4"]', timeout=10000)

        containers = await page.query_selector_all('[data-testid="default_container_ux4"]')
        results = []

        for container in containers:
            # 🖼 Image URL
            img_el = await container.query_selector('div[role="button"] img')
            img_url = await img_el.get_attribute('src') if img_el else None

            # 🏷 Title
            title_el = await container.query_selector('div.novMV')
            title_text = await title_el.inner_text() if title_el else None

            # # ⚖ Quantity
            # quantity_el = await container.query_selector('div[aria-label*="L"], .entQHA._3eIPt')
            # quantity_text = await quantity_el.inner_text() if quantity_el else None
            quantity_el = await container.query_selector('.entQHA._3eIPt')
            if not quantity_el:
                # Try a backup strategy
                quantity_el = await container.query_selector('div[aria-label]')
            quantity_text = await quantity_el.inner_text() if quantity_el else None

            # 💸 Price
            price_el = await container.query_selector('[data-testid="item-offer-price"]')
            price_text = await price_el.inner_text() if price_el else None

            # # 🧾 MRP (optional)
            # mrp_el = await container.query_selector('[data-testid="item-mrp-price"]')
            # mrp_text = await mrp_el.inner_text() if mrp_el else None

            # # 🏷 Discount (optional)
            # discount_el = await container.query_selector('[data-testid="item-offer-label-discount-text"]')
            # discount_text = await discount_el.inner_text() if discount_el else None

            results.append({
                "image": img_url,
                "title": title_text.strip() if title_text else None,
                "quantity": quantity_text.strip() if quantity_text else None,
                "price": price_text.strip() if price_text else None,
                # "mrp": mrp_text.strip() if mrp_text else None,
                # "discount": discount_text.strip() if discount_text else None
            })

        await browser.close()
        return results