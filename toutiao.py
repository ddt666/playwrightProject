# -*- coding: utf-8 -*-
# @Time    : 2022/6/2 19:20
# @Author  : ML
# @Email   : 450730239@qq.com
# @File    : toutiao.py
from playwright.sync_api import Playwright, sync_playwright, expect
import time

urls = []


def on_response(response):
    if 'pc/list/user/feed' in response.url and response.status == 200:
        resp = response.json()
        articles = resp.get("data")
        for a in articles:
            try:
                if "article_url" in a.keys():
                    url = a.get("article_url")
                elif "item_id" in a.keys():
                    url = "https://www.ixigua.com/" + a.get("item_id")
                else:
                    url = "https://www.toutiao.com/w/" + a.get("id")
            except Exception as e:

                url = "https://www.toutiao.com/group/" + str(a.get("id"))
                print("需甄别", url)

            urls.append(url)


def run(playwright: Playwright) -> None:
    # iphone_12_pro_max = playwright.devices['iPhone 12 Pro Max']
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    # context = browser.new_context(
    #     **iphone_12_pro_max,
    #     locale='zh-CN',
    #     geolocation={'longitude': 116.39014, 'latitude': 39.913904},
    #     permissions=['geolocation']
    # )

    page = context.new_page()

    # page.goto("http://httpbin.org/ip")
    #
    # time.sleep(2000)
    page.on('response', on_response)
    page.goto(
        "https://www.toutiao.com/c/user/token/MS4wLjABAAAAO4z1s60H3TVOisBlqdpKsyncRZD5xHklrwmyHEH34tk/??tab=article?tab=all")
    page.wait_for_load_state('networkidle')
    for _ in range(0, 100):
        print(_)
        with page.expect_event('requestfinished') as response:
            pass
        page.evaluate('var scrollHeight=document.body.scrollHeight; window.scrollTo(0, scrollHeight)')
        time.sleep(1)

    for i ,url in enumerate(urls):
        print(i)
        page.goto(url, wait_until="networkidle")
    print("加载完毕")
    time.sleep(200)

    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
