from .base_input import BaseInput


class TextInput(BaseInput):
    """文本输入框"""
    @property
    def value(self):
        """:return input已经输入的值"""
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value
        input_ = self.element.find_element_by_xpath(".//input")
        self.send_keys(input_, value)


class NoLabelTextInput(TextInput):
    """有些输入框没有标题label"""
    @property
    def name(self):
        return None


class NumberInput(BaseInput):
    """数字输入框"""

    @property
    def value(self):
        """:return input已经输入的值"""
        return self._value

    @value.setter
    def value(self, value: float):
        self._value = value
        input_ = self.element.find_element_by_xpath(".//input")
        self.send_keys(input_, value)


class TextAreaInput(BaseInput):
    """textarea标签的输入框"""
    @property
    def value(self):
        """:return input已经输入的值"""
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value
        input_ = self.element.find_element_by_xpath(".//textarea")
        self.send_keys(input_, value)


class DisableTextInput(BaseInput):
    """不可输入的输入框，文本字段就是这样实现的"""
    @property
    def value(self):
        """:return input已经输入的值"""
        return self.element.find_element_by_xpath(".//input").get_attribute("value")

    @value.setter
    def value(self, value=None):
        pass
