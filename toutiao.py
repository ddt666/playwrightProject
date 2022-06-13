# -*- coding: utf-8 -*-
# @Time    : 2022/6/2 19:20
# @Author  : ML
# @Email   : 450730239@qq.com
# @File    : toutiao.py
from playwright.sync_api import Playwright, sync_playwright, expect
import time
from mysqlhelper import MysqlHelper
from datetime import datetime
from playwright._impl._sync_base import EventInfo

mysql_config = {
    'host': '47.93.119.185',
    'port': 3306,
    'user': 'social',
    'password': 'moonshine**1',
    'charset': 'utf8mb4',
    "database": "dx"

}
import re


def on_response(response):
    if 'pc/list/user/feed' in response.url and response.status == 200:
        resp = response.json()
        articles = []
        data = resp.get("data")
        if not data:
            return
        for d in data:
            article = {}
            a_id = d.get("id")
            group_id = d.get("group_id")
            if group_id:
                url = "https://www.toutiao.com/group/" + str(group_id)
            else:
                url = "https://www.toutiao.com/group/" + str(a_id)

            # try:
            #     if "article_url" in d.keys():
            #         url = d.get("article_url")
            #     elif "item_id" in d.keys():
            #         url = "https://www.ixigua.com/" + a_id
            #     else:
            #         url = "https://www.toutiao.com/w/" + a_id
            # except Exception as e:
            #
            #     # url = "https://www.toutiao.com/group/" + a_id
            #     continue
            #     # print("需甄别", url)
            publish_time_stamp = d.get("publish_time")
            if not publish_time_stamp:
                continue
            title = d.get("title", "")
            read_count = d.get("read_count", 0)
            comment_count = d.get("comment_count", 0)

            publish_time = None
            if publish_time_stamp:
                publish_time = datetime.fromtimestamp(publish_time_stamp).strftime("%Y-%m-%d %H:%M:%S")

            content = d.get("abstract", "")
            if not content:
                content = d.get("content", "")

            digg_count = d.get("digg_count", 0)
            article.update({
                "url": url,
                "title": title,
                "viewed_num": read_count,
                "commented_num": comment_count,
                "content": content,
                "publish_date": publish_time,
                "liked_num": digg_count,
                "site": "头条账号文章",
                "author": "中国电信客服"
            })
            # print(article)
            articles.append(article)
        mysql_helper = MysqlHelper(mysql_config)
        mysql_helper.mysql_insert("topic_0607", articles)
        print("入库成功", len(articles))


def run(playwright: Playwright) -> None:
    # iphone_12_pro_max = playwright.devices['iPhone 12 Pro Max']
    chrome_param = [
        # '--start-maximized',
        '--blink-settings=imagesEnabled=false'
        # "--no-sandbox"

    ]

    browser = playwright.chromium.launch(headless=False, args=chrome_param)
    print(222222222)

    # browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
        # no_viewport=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36")

    # context = browser.new_context(
    #     **iphone_12_pro_max,
    #     locale='zh-CN',
    #     geolocation={'longitude': 116.39014, 'latitude': 39.913904},
    #     permissions=['geolocation']
    # )

    page = context.new_page()
    print(type(page))
    page = context.new_page()
    print(context.pages)
    time.sleep(20000)
    # page.goto("http://httpbin.org/ip")
    #
    # time.sleep(2000)
    page.on('response', on_response)
    # page.goto('https://www.baidu.com', wait_until='networkidle')
    page.goto(
        "https://www.toutiao.com/c/user/token/MS4wLjABAAAATowCvQ005do_GF306BFHrN07NEDb8PpLiisC2pgtIpzLFi_3FmhK-CHOzTthyghW/?")
    # page.goto(
    #     "https://www.toutiao.com/c/user/token/MS4wLjABAAAAJ6XY3vn25w3jesplUmb270Ll2b6kEP9D4HD8L6fOKsfv2cXwFYO8kPU_1LaI4BsX/?")
    page.wait_for_load_state('networkidle')
    # page.screenshot(path='screenshot{}.png'.format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))
    force_wait_count = 0
    while 1:
        # print(_)
        # with page.expect_event('response') as response:
        #     print(response.value)
        # time.sleep(20)
        # time.sleep(10)
        page.evaluate("""let arrToolTips = document.querySelectorAll('.profile-tab-feed>div:not(.profile-feed-no-more)')
      let arrToolTipsLen = arrToolTips.length
      for (let i = arrToolTipsLen - 1; i >= 0; i--) {
        let parent = arrToolTips[i].parentElement
        if (parent && arrToolTips[i]) {
          parent.removeChild(arrToolTips[i])
        }
 }""")
        # time.sleep(200)
        print("下拉")
        page.evaluate('var scrollHeight=document.body.scrollHeight; window.scrollTo(0, scrollHeight)')

        # time.sleep(2)
        #
        loading = None
        try:
            loading = page.wait_for_selector(".feed-m-loading", state="attached", timeout=5 * 1000)
            # print("loading", loading)
        except Exception as e:
            print("上拉")
            page.evaluate('var scrollHeight=document.body.scrollHeight; window.scrollTo(0, 0)')
            print("强制等待")
            time.sleep(2)
            # page.evaluate('var scrollHeight=document.body.scrollHeight; window.scrollTo(0, scrollHeight)')
            # continue


        if loading:
            print("等待加载")
            page.wait_for_selector(".feed-m-loading", state="hidden")
            # print("s",s)
        else:
            try:
                no_more = page.wait_for_selector(".profile-feed-no-more", state="attached", timeout=1 * 1000)
                # print("no_more", no_more)
                print("无更多内容")
                break

            except Exception as e:
                pass
        # try:
        #     if page.is_visible('.profile-feed-no-more'):
        #         print("无更多内容")
        #         break
        #     elif page.is_visible('.feed-m-loading'):
        #         force_wait_count = 0
        #         print("等待加载")
        #         page.wait_for_selector(".feed-m-loading", state="hidden")
        #     else:
        #         force_wait_count += 1
        #         print("强制等待")
        #
        #         # if force_wait_count > 5:
        #         print("上拉")
        #         page.evaluate('var scrollHeight=document.body.scrollHeight; window.scrollTo(0, 0)')
        #         page.wait_for_timeout(1 * 1000)
        #         # page.screenshot(path='screenshot{}.png'.format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))
        #         force_wait_count = 0
        # except Exception as e:
        #     print(e)
        #     # page.screenshot(path='screenshot{}.png'.format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")))
        #     page.wait_for_timeout(5 * 1000)
        #     continue

    # for i, url in enumerate(urls):
    #     print(i)
    #     page.goto(url, wait_until="networkidle")l
    print("抓取完毕")
    # time.sleep(200)

    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
