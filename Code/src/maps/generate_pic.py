import os
import asyncio
from pyppeteer import launch


curr_path = os.getcwd()


async def generate_map_screenshot():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('http://localhost:8000/')
    await page.screenshot({'path': curr_path + '/maps/map.png'})
    await browser.close()


def click():
    asyncio.get_event_loop().run_until_complete(generate_map_screenshot())
