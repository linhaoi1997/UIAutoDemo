from typing import List

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from .base_actions import Clear
from Utils.SeleniumTools.change_wait_time import change_wait_time


class BaseElement(object):
    def __init__(self, *args, wait_time=10):
        self.wait_time = wait_time
        if len(args) == 1:
            args = [By.XPATH, args[0]]
        assert len(args) == 2
        self.locator = args

    def _handle(self, instance):
        driver = instance.driver
        return WebDriverWait(driver, self.wait_time).until(
            lambda d: driver.find_element(*self.locator)
        )

    def __set__(self, instance, value):
        element = self._handle(instance)
        Clear(element)
        element.send_keys(value)

    def __get__(self, instance, owner) -> WebElement:
        return self._handle(instance)


class Element(BaseElement):
    pass


class Elements(BaseElement):
    def _handle(self, instance):
        driver = instance.driver
        return WebDriverWait(driver, self.wait_time).until(
            lambda d: driver.find_elements(*self.locator)
        )


class OptionsElement(object):

    def __get__(self, instance, owner) -> List[WebElement]:
        driver = instance.driver
        option: WebElement = driver.find_elements(By.XPATH, "//div[@role='presentation']")[-1]
        with change_wait_time(driver):
            options = option.find_elements_by_xpath(".//ul/li")
            return options
