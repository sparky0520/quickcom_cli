from playwright.async_api import async_playwright

async def fetch_blinkit_prices(query: str):
    url = f"https://blinkit.com/s/?q={query}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        
        # 🌍 Set geolocation and allow permission
        context = await browser.new_context(
            geolocation={"latitude": 28.546586, "longitude": 77.254190},
            permissions=["geolocation"]
        )
        page = await context.new_page()

        await page.goto(url)

        # 💥 Click "Detect my location" if visible
        try:
            await page.get_by_text("Detect my location", exact=True).click(timeout=5000)
            print("✅ Blinkit: Clicked on 'Detect my location'")
        except Exception:
            print("⚠️ 'Blinkit: Detect my location' not found or already set")

        # ⏳ Wait for location-based results to load
        await page.wait_for_timeout(3000)

        # 🔍 Extract all products
        await page.wait_for_selector("div[class*=tw-relative][role='button']", timeout=15000)
        items = await page.query_selector_all("div[class*=tw-relative][role='button']")

        results = []
        for item in items:
            # 🖼 Image URL
            img_el = await item.query_selector("img.tw-h-full")
            img_url = await img_el.get_attribute("src") if img_el else None

            # 🏷 Title
            title_el = await item.query_selector("div.tw-text-300.tw-font-semibold.tw-line-clamp-2")
            title_text = await title_el.inner_text() if title_el else None

            # ⚖ Quantity
            quantity_el = await item.query_selector("div.tw-text-200.tw-font-medium.tw-line-clamp-1.tw-text-base-green")
            quantity_text = await quantity_el.inner_text() if quantity_el else None

            # 💸 Price
            price_el = await item.query_selector("div.tw-text-200.tw-font-semibold")
            price_text = await price_el.inner_text() if price_el else None

            results.append({
                "image": img_url,
                "title": title_text.strip() if title_text else None,
                "quantity": quantity_text.strip() if quantity_text else None,
                "price": price_text.strip() if price_text else None,
            })

        await browser.close()
        return results
