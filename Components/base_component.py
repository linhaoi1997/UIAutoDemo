from typing import List

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions


class OriginElement(object):

    def __get__(self, instance, owner):
        driver = instance.driver
        locator = instance.locator
        return WebDriverWait(driver, 20).until(
            lambda d: driver.find_elements(*locator)
        )


class BaseComponent(object):
    origin = OriginElement()

    def __init__(self, driver: WebDriver, locator):
        self.driver = driver
        self.locator = locator
        self._handle()

    def refresh(self):
        WebDriverWait(self.driver, 10).until(expected_conditions.invisibility_of_element(self.element))
        self._handle()

    def _handle(self):
        self.elements: List[WebElement] = self.origin
        self.element: WebElement = self.elements[0]
