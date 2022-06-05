from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.kanzhun.com/firm/review/1nRy0tW1EA~~/p1.html?ka=com-review-module-expose
    page.goto("https://www.kanzhun.com/firm/review/1nRy0tW1EA~~/p1.html?ka=com-review-module-expose")

    # Click text=212020-02-13发布 >> span >> nth=0
    with page.expect_popup() as popup_info:
        page.locator("text=212020-02-13发布 >> span").first.click()
    page1 = popup_info.value

    # Click .number.min >> nth=0
    page.locator(".number.min").first.click()

    # Click text=222020-02-13发布 >> span >> nth=0
    page.locator("text=222020-02-13发布 >> span").first.click(button="right")

    # Click p:has-text("刚毕业的学生会比较有发展，公司经营品牌也多 有一定的上升空间，薪资待遇也比较不错。")
    with page.expect_popup() as popup_info:
        page.locator("p:has-text(\"刚毕业的学生会比较有发展，公司经营品牌也多 有一定的上升空间，薪资待遇也比较不错。\")").click()
    page2 = popup_info.value

    # Click text=全部点评83精选最新状 态：在职离职岗 位：其他运营管理培训生网页设计师运营经理/主管Java视觉设计师商家运营电商运营网络销售HRBP产品经理平面设计设计经理 >> i >> nth=1
    page.locator("text=全部点评83精选最新状 态：在职离职岗 位：其他运营管理培训生网页设计师运营经理/主管Java视觉设计师商家运营电商运营网络销售HRBP产品经理平面设计设计经理 >> i").nth(1).click()
    # expect(page).to_have_url("https://www.kanzhun.com/firm/review/1nRy0tW1EA~~/p2.html?ka=com-review-module-expose")

    # Click text=完美！匿名用户任职：网络推广在职登录后可以解锁查看当前内容登录/注册暂不登录，去小程序看2019-02-12发布很棒匿名用户任职：其他职位工作过登录后可以解锁查 >> i >> nth=1
    page.locator("text=完美！匿名用户任职：网络推广在职登录后可以解锁查看当前内容登录/注册暂不登录，去小程序看2019-02-12发布很棒匿名用户任职：其他职位工作过登录后可以解锁查 >> i").nth(1).click(button="right")

    # Click text=完美！匿名用户任职：网络推广在职登录后可以解锁查看当前内容登录/注册暂不登录，去小程序看2019-02-12发布很棒匿名用户任职：其他职位工作过登录后可以解锁查 >> i >> nth=1
    page.locator("text=完美！匿名用户任职：网络推广在职登录后可以解锁查看当前内容登录/注册暂不登录，去小程序看2019-02-12发布很棒匿名用户任职：其他职位工作过登录后可以解锁查 >> i").nth(1).click(button="right")

    # Click text=完美！匿名用户任职：网络推广在职登录后可以解锁查看当前内容登录/注册暂不登录，去小程序看2019-02-12发布很棒匿名用户任职：其他职位工作过登录后可以解锁查 >> i >> nth=1
    page.locator("text=完美！匿名用户任职：网络推广在职登录后可以解锁查看当前内容登录/注册暂不登录，去小程序看2019-02-12发布很棒匿名用户任职：其他职位工作过登录后可以解锁查 >> i").nth(1).click(button="right")

    # Click .rc-pagination-next > a > .rc-pagination-item-link
    page.locator(".rc-pagination-next > a > .rc-pagination-item-link").click()

    # Close page
    page1.close()

    # Close page
    page2.close()

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
