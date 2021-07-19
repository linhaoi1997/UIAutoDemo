from contextlib import contextmanager

from selenium.webdriver.remote.webdriver import WebDriver


@contextmanager
def change_wait_time(driver: WebDriver):
    """有时找不到元素，但是会因为隐式等待很耗时，使用上下文管理解决这个问题"""
    driver.implicitly_wait(0)
    yield
    driver.implicitly_wait(5)
