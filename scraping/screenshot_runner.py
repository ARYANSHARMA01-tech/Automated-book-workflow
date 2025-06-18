import asyncio
from playwright.async_api import async_playwright

async def async_take_screenshot(url, save_path="screenshots/screenshot.png"):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.screenshot(path=save_path)
        await browser.close()

def take_screenshot(url, save_path="screenshots/screenshot.png"):
    asyncio.run(async_take_screenshot(url, save_path))
