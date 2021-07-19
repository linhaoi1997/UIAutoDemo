from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from Utils.AssertTools.raise_error import raise_assert_error
from Components.CommonPonents.FormLeftWordComponent.Inputs.base_input import BaseInput
from Elements.CommonElements import OptionsElement
from Utils.SeleniumTools.wait_options_visibility import wait_options_visibility


class NativeSelectInput(BaseInput):
    """单选下拉"""
    select_button = "./div"
    options = OptionsElement()

    def _choice(self, value):
        """选择某个元素后，元素会消失"""
        options = self.options
        for option in options:
            if value in option.text:
                option.click()
                WebDriverWait(self.driver, 5).until(expected_conditions.invisibility_of_element(option.element))
                return
        else:
            raise_assert_error(self.driver, f"没找到从下拉选项{[i.text for i in options]}中想要的下拉选项{value} ")

    def choice(self, value):
        """选择一个下拉选项"""
        with wait_options_visibility(self.driver):
            self.element.find_element_by_xpath(self.select_button).click()
        self._choice(value)

    @property
    def value(self):
        """:return input已经输入的值"""
        return self._value

    @value.setter
    def value(self, value: str):
        self.choice(value)
        self._value = value


class SearchSelectInput(NativeSelectInput):
    select_button = ".//button[@title='Open']"

    def search_and_choice(self, search_str: str, value):
        """搜索框输入之后可能有延迟"""
        with wait_options_visibility(self.driver):
            self.element.find_element_by_xpath(".//input").send_keys(search_str)
        self._choice(value)


class MuiSelectInput(NativeSelectInput):
    @property
    def value(self):
        """:return input已经输入的值"""
        return self._value

    @value.setter
    def value(self, values: list):
        self.choice(*values)
        self._value = values

    def _choice(self, value):
        options = self.options
        for option in options:
            if value in option.text:
                option.select()
                return
        else:
            raise_assert_error(self.driver, f"没找到从下拉选项{[i.text for i in options]}中想要的下拉选项{value} ")

    def choice(self, *values):
        """选择一个下拉选项"""
        with wait_options_visibility(self.driver):
            self.element.find_element_by_xpath(self.select_button).click()
        options = self.options
        # 清空所有的选项
        for option in options:
            option.do_not_select()
        # 选择所有要选择的选项
        for value in values:
            self._choice(value)
        self._make_sure_options_invisibility(options[0])

    def _make_sure_options_invisibility(self, option):
        # 点击label使下拉框收起
        ActionChains(self.driver).click(self.element.find_element_by_xpath(self.LABEL_LOCATOR)).perform()
        WebDriverWait(self.driver, 5).until(expected_conditions.invisibility_of_element(option.element))


class NoLabelMuiSelectInput(MuiSelectInput):
    def __init__(self, element, label_element):
        """
        用于复杂input的子元素，子元素没有label，无法点击自己的label元素来使下拉框收起，使用复杂input的label
        :param element: 整个input元素
        :param label_element: 父节点的复杂input的label元素
        """
        super(NoLabelMuiSelectInput, self).__init__(element)
        self.label_element = label_element

    def _make_sure_options_invisibility(self, option):
        # 点击label使下拉框收起
        ActionChains(self.driver).click(self.label_element).perform()
        WebDriverWait(self.driver, 5).until(expected_conditions.invisibility_of_element(option.element))
