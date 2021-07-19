from selenium.webdriver.support.wait import WebDriverWait

from .change_wait_time import change_wait_time
from contextlib import contextmanager

from selenium.webdriver.remote.webdriver import WebDriver


@contextmanager
def wait_options_visibility(driver: WebDriver):
    """下拉选择框，点击之后要等一会儿选项才会出来"""
    with change_wait_time(driver):
        nums = len(driver.find_elements_by_xpath("//div[@role='presentation']"))
        yield
        WebDriverWait(driver, 5).until(
            lambda x: len(driver.find_elements_by_xpath("//div[@role='presentation']")) > nums)
