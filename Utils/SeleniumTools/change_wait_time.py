from contextlib import contextmanager

from selenium.webdriver.remote.webdriver import WebDriver


@contextmanager
def change_wait_time(driver: WebDriver):
    driver.implicitly_wait(0)
    yield
    driver.implicitly_wait(5)
