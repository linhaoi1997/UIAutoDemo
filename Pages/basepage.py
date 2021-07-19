import time
from urllib.parse import urljoin

import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from seletools.actions import drag_and_drop
from Elements.base_actions import scroll_view, Clear

from load_config import config

BASE_URL = config.url


class BasePage(object):
    """ path: 每个页面有对应的路径，使用正则表达式写，在跳转中会以path作为依据，如果不匹配报错 """
    path = '/'

    def __init__(self, selenium_driver, base_url=BASE_URL, auto_jump=True):
        self.url = urljoin(base_url, self.path)
        self.driver: WebDriver = selenium_driver if isinstance(selenium_driver, WebDriver) else selenium_driver.driver
        self.driver.implicitly_wait(5)
        self.message_ = None
        if auto_jump:
            if not expected_conditions.url_matches(self.path)(self.driver):
                self.driver.get(self.url)
            if not self.on_page():
                raise AssertionError("页面jump失败，预期url为%s，实际上url为%s" % (self.path, self.driver.current_url))

    def on_page(self):
        """ 判断driver是否在当前页面 """
        return WebDriverWait(self.driver, 20).until(expected_conditions.url_matches(self.path))

    # 对浏览器进行截图
    @allure.step("进行截图")
    def screen_shot(self, name=None):
        allure.attach(self.driver.get_screenshot_as_png(), "可能出现问题了，截个图", allure.attachment_type.PNG)

    @allure.step("关闭浏览器")
    def close(self):
        self.driver.close()
        self.driver.quit()

    def ac_click(self, element):
        """鼠标点击某个元素，不推荐使用"""
        ac = ActionChains(self.driver)
        ac.click(element).perform()

    def drag_and_drop(self, element1, element2):
        """通过js拖转元素，因为ActionChains提供的方法拖拽不可用"""
        drag_and_drop(self.driver, element1, element2)

    def refresh(self):
        """ 刷新页面"""
        self.driver.refresh()
        time.sleep(2)

    def safe_click(self, element):
        """在点击某个元素时，可能元素不在窗口，这时不可以点击，先滚动元素再等待元素可点击"""
        scroll_view(element)
        WebDriverWait(self.driver, 10).until(lambda x: element.enabled())

    @staticmethod
    def clear(element):
        """清除输入框内容，这里有时使用clear方法没用，所以会判断，如果有值就调用element.send_keys(Keys.BACKSPACE)，一个一个删除"""
        Clear(element)

    def send_keys(self, element, value):
        """先清空输入框内容再输入"""
        self.clear(element)
        element.send_keys(value)
