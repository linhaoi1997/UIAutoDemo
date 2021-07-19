from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from Utils.SeleniumTools.change_wait_time import change_wait_time


class Option(object):

    def __init__(self, element: WebElement):
        self.element = element
        self.driver = self.element.parent

    @property
    def text(self):
        return self.element.text

    @property
    def is_selected(self):
        return "selected" in self.element.get_attribute("class")

    def click(self):
        self.element.click()

    def select(self):
        if not self.is_selected:
            self.element.click()
            WebDriverWait(self.driver, 5).until(lambda x: self.is_selected)

    def do_not_select(self):
        if self.is_selected:
            self.element.click()
            WebDriverWait(self.driver, 5).until(lambda x: not self.is_selected)


class OptionsElement(object):

    def __get__(self, instance, owner) -> List[Option]:
        driver = instance.driver
        option: WebElement = driver.find_elements(By.XPATH, "//div[@role='presentation']")[-1]
        with change_wait_time(driver):
            options = option.find_elements_by_xpath(".//ul/li")
            return [Option(i) for i in options]
