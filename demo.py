# -*- coding: utf-8 -*-
# @Time    : 2022/5/18 0:37
# @Author  : ML
# @Email   : 450730239@qq.com
# @File    : demo.py
from playwright.sync_api import sync_playwright
import time
with sync_playwright() as p:
    p.chromium.launch()
    for browser_type in [p.chromium]:
        browser = browser_type.launch(headless=False)
        page = browser.new_page()
        page.goto('https://www.baidu.com',wait_until='networkidle')
        # page.screenshot(path=f'screenshot-{browser_type.name}.png')
        # print(page.title())

        page.click('#s-top-left>a:first-child')

        time.sleep(20000)
        browser.close()

from playwright.sync_api import sync_playwright
#
# with sync_playwright() as p:
#     import os
#
#     user_home = os.path.expanduser('~')
#     user_data_dir = f'{user_home}\\AppData\\Local\\Google\\Chrome\\playwrightDemo'
#     browser = p.chromium.launch_persistent_context(user_data_dir=user_data_dir, headless=False)
#
#     page = browser.new_page()
#     page.goto("https://www.kanzhun.com/firm/review/1nRy0tW1EA~~/p1.html?ka=com-review-module-expose")
#     # context = browser.new_context()
#     # context.new_page()
#     # iphone_11 = p.devices['iPhone 11 Pro']
#     # browser = p.webkit.launch(headless=False)
#     # context = browser.new_context(
#     #     **iphone_11,
#     #     locale='de-DE',
#     #     geolocation={'longitude': 12.492507, 'latitude': 41.889938},
#     #     permissions=['geolocation']
#     # )
#     # page = context.new_page()
#     import time
#
#     time.sleep(600)
#     browser.close()
