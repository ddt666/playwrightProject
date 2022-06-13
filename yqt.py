from loguru import logger
from playwright.sync_api import Playwright, sync_playwright, expect
from playwright.sync_api._generated import Page


class YQTSpider(object):
    def __init__(self, playwright: Playwright):
        self.context = playwright.chromium.launch(headless=False).new_context()
        self.page=None

    @property
    def current_page(self) -> Page:
        # print(len(self.context.pages))
        if not self.page:
            self.page = self.context.new_page()
            return self.page
        else:
            return self.page

    # def init_browser(self):
    #     with sync_playwright() as playwright:
    #         run(playwright)

    def login_by_unm_psd(self, count=1):
        # driver = self.spider_driver

        if count > 10:
            logger.warning("登录次数超过10次,请检查登录流程")
            return False

        logger.info(f"开始登录....{count}")
        self.current_page.goto("http://yuqing.sina.com/staticweb/#/login",wait_until='domcontentloaded')

        # self.current_page.wait_for_load_state('domcontentloaded')
        username = self.current_page.locator("xpath=//input[@formcontrolname='userName']")
        password = self.current_page.locator("xpath=//input[@formcontrolname='password']")
        yqzcode = self.current_page.locator("xpath=//input[@formcontrolname='yqzcode']")
        username.fill("llzsgc")
        print(username,password,yqzcode)
        import time
        time.sleep(2000)
        # username = driver.find_element_by_xpath("//input[@formcontrolname='userName']")
        # password = driver.find_element_by_xpath("//input[@formcontrolname='password']")
        # yqzcode = driver.find_element_by_xpath("//input[@formcontrolname='yqzcode']")
        #
        # submit_buttion = driver.find_element_by_xpath("//button[contains(@class,'login-form-button')]")
        #
        # username.send_keys("llzsgc")
        # password.send_keys("Ad818ad818")
        #
        # logger.info("获取验证码....")
        # try:
        #     code_img = self.wait.until(
        #         EC.presence_of_element_located((By.XPATH, "//img[contains(@src,'validate/image')]")))
        # except TimeoutException:
        #     print("刷新")
        #     driver.refresh()

        # while 1:
        #     code_img = None
        #     try:
        #         code_img = self.wait.until(
        #             EC.presence_of_element_located((By.XPATH, "//img[contains(@src,'validate/image')]")))
        #     except TimeoutException:
        #         pass
        #
        #     if code_img and code_img.size.get("width") > 0:
        #         break
        #     logger.info("验证码图片没加载出来，刷新...")
        #     driver.refresh()
        #
        # # code_img = driver.find_element_by_xpath(
        # #     "//img[contains(@src,'validate/image')]")
        # # print(code_img.size.get("width"))
        # # print(code_img.size.get("width"))
        # # while not code_img or code_img.size.get("width") == 0:
        # #     driver.refresh()
        # code_img_base64 = code_img.screenshot_as_base64
        # # print("code_img_base64", code_img_base64)
        # code = SpiderHelper.recognise_code(code_img_base64)
        # logger.info(f"获取验证码:{code}")
        # if not code:
        #     code = "1234hi"
        #
        # yqzcode.send_keys(code)
        # submit_buttion.click()
        # try:
        #     wait = self.wait.until(
        #         EC.invisibility_of_element_located((By.XPATH, "//input[@formcontrolname='userName']")))
        #     # print(wait)
        #     # print("登录成功")
        #     # return True
        # except Exception as e:
        #     logger.warning(e)
        #
        # try:
        #     mobile_code = driver.find_element_by_css_selector(".ant-modal-content .mt20 input")
        #     # pyautogui.prompt("需要手机验证")
        #     while not driver.is_url_change():
        #         print("还没填写验证码")
        #         time.sleep(1)
        #
        # except NoSuchElementException:
        #     pass
        #
        # if driver.is_url_change():
        #
        #     return True
        # else:
        #     return self.login_by_unm_psd(count=count + 1)


if __name__ == '__main__':
    with sync_playwright() as playwright:
        yqt = YQTSpider(playwright)
        yqt.login_by_unm_psd()
