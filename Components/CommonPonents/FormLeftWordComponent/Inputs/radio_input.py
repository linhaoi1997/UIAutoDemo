from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from Utils.AssertTools.raise_error import raise_assert_error
from .base_input import BaseInput


class Radio(BaseInput):
    name_locator = "./span[last()]"
    input_locator = ".//input"

    @property
    def is_selected(self):
        return "checked" in self.element.find_element_by_xpath("./span").get_attribute("class")

    @property
    def name(self):
        return self.element.find_element_by_xpath(self.name_locator).text

    def select(self):
        if not self.is_selected:
            self.element.find_element_by_xpath(self.input_locator).click()
            WebDriverWait(self.driver, 5).until(lambda x: self.is_selected)

    @property
    def value(self):
        """:return input已经输入的值"""
        return self.is_selected

    @value.setter
    def value(self, value: bool):
        if value:
            self.select()
        self._value = value


class RadioGroupInput(BaseInput):
    radio_group_locator = ".//div[@role='radiogroup']"
    radio_locator = "./label"

    def __init__(self, element: WebElement):
        super(RadioGroupInput, self).__init__(element)
        self.radios = [Radio(i) for i in
                       self.element.find_element_by_xpath(self.radio_group_locator).find_elements_by_xpath(
                           self.radio_locator)]

    @property
    def value(self):
        """:return input已经输入的值"""
        return self._value

    @value.setter
    def value(self, value):
        for radio in self.radios:
            if radio.name == value:
                radio.select()
                break
        else:
            raise_assert_error(self.driver, f"没找到从radios{[i.name for i in self.radios]}中想要的下拉选项{value} ")
        self._value = value
