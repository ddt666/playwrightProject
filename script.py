from playwright.sync_api import Playwright, sync_playwright, expect
import time
from playwright._impl._api_types import TimeoutError
from pyquery import PyQuery as pq


def run(playwright: Playwright) -> None:
    # browser = playwright.chromium.launch(headless=False)
    # context = browser.new_context()
    chrome_param = [
        '--start-maximized'
        # "--no-sandbox"

    ]
    import os

    user_home = os.path.expanduser('~')
    user_data_dir = f'{user_home}\\AppData\\Local\\Google\\Chrome\\playwrightDemo'
    browser = playwright.chromium.launch_persistent_context(user_data_dir=user_data_dir,
                                                            headless=False,
                                                            args=chrome_param,
                                                            no_viewport=True,
                                                            ignore_default_args=['--enable-automation', "--no-sandbox"])

    # Open new page
    page = browser.pages[0]

    # Go to https://www.kanzhun.com/firm/review/1nRy0tW1EA~~/p1.html?ka=com-review-module-expose
    page.goto("https://www.kanzhun.com")
    # page.goto("https://www.kanzhun.com/firm/review/1nRy0tW1EA~~/p1.html?ka=com-review-module-expose")
    # page.wait_for_load_state('networkidle')

    try:
        page.wait_for_selector('.userinfo', state='attached', timeout=10 * 1000)
    except Exception as e:
        print(e)
        if isinstance(e, TimeoutError):
            var = input("需登录，登录成功输入1继续")
            if var == 1:
                pass
    page.goto("https://www.kanzhun.com/firm/review/1nRy0tW1EA~~/p1.html?ka=com-review-module-expose")
    # print(element.inner_html())
    element_handle = page.query_selector('.userinfo')
    # print(
    # element_handle.is_disabled(),
    # element_handle.is_editable(),
    # element_handle.is_enabled(),
    # element_handle.is_hidden(),
    # element_handle.is_visible())
    # print(userinfo_e)

    # Click span:has-text("最新")
    page.locator("span:has-text(\"最新\")").click()
    # expect(page).to_have_url("https://www.kanzhun.com/firm/review/1nRy0tW1EA~~/p1.html?ka=com-review-module-expose")
    while 1:
        # page.wait_for_timeout(2000)
        # page.expect_event('requestfinished')
        with page.expect_event('requestfinished') as response:
            print('')
        print(response.value)
        html = page.content()
        # print(html)
        doc = pq(html)
        data_list = doc.find('div.bala').items()
        for data in data_list:
            rate_text = data.find('a.kz-rate-text').text()
            items = data.find(".kz-rate-star.kz-rate-star-full").items()
            stars = 0
            if items:
                stars = len(list(items))
            author = data.find('.user>span').text()
            job = data.find('.job>span').text()

            status = data.find('span.tag').text()
            content = data.find('.text-content').text()
            publish_date = data.find('.publish>span:first-child').text()
            comment = data.find('.operation_tIrYy>.icon:first-child>span').text()
            comment_num = int(comment) if comment else 0

            like = data.find('.operation_tIrYy>.icon:last-child>span').text()
            like_num = int(like) if like else 0
            print(status, publish_date, comment_num, like_num)

        next_page = page.locator('.rc-pagination-next')
        attr = next_page.get_attribute('aria-disabled')
        has_next = False if 'true' in attr else True
        if has_next:
            print('有下一页')
            next_page.click()

        else:
            print("没有下一页")
            break

    # Click #list a:has-text("2")
    # page.locator("#list a:has-text(\"2\")").click()
    # expect(page).to_have_url("https://www.kanzhun.com/firm/review/1nRy0tW1EA~~/p2.html?ka=com-review-module-expose")

    # ---------------------
    # browser.close()
    # browser.close()
    time.sleep(500)


with sync_playwright() as playwright:
    run(playwright)
