from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from abc import ABCMeta, abstractmethod


class BaseInput(metaclass=ABCMeta):
    FOCUS_LOCATOR = ".."
    LABEL_LOCATOR = ".//label/p"

    def __init__(self, element: WebElement):
        self.element = element
        self.driver: WebDriver = self.element.parent
        self._value = None

    @property
    def is_focus(self):
        """:return input是否被选中的状态"""
        return "focused" in self.element.find_element_by_xpath(self.FOCUS_LOCATOR).get_attribute("class")

    @property
    def name(self):
        """:return input的name"""
        return self.element.find_element_by_xpath(self.LABEL_LOCATOR).text.strip(" :")

    @property
    def value(self):
        """:return input已经输入的值"""
        return self._value

    @value.setter
    @abstractmethod
    def value(self, value):
        self._value = value

    def fake(self):
        """为input随机填写值"""
        self._value = None

    @staticmethod
    def send_keys(element, value):
        element.clear()
        if element.get_attribute("value"):
            element.send_keys(Keys.ARROW_DOWN)
        while element.get_attribute("value"):
            element.send_keys(Keys.BACKSPACE)
        element.send_keys(value)


if __name__ == '__main__':
    from Utils.RunTest.get_driver import get_driver

    d = get_driver()


    class Test(BaseInput):

        @property
        def value(self):
            """:return input已经输入的值"""
            return self._value

        @value.setter
        def value(self, value):
            self._value = value


    t = Test(d.find_element_by_xpath("//div"))
