from .base_input import BaseInput


class TextInput(BaseInput):

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
    @property
    def name(self):
        return None


class NumberInput(BaseInput):

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
    @property
    def value(self):
        """:return input已经输入的值"""
        return self.element.find_element_by_xpath(".//input").get_attribute("value")

    @value.setter
    def value(self, value=None):
        pass
