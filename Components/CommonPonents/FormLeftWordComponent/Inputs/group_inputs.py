"""复合表单，这里面实现了所有的自定义表单声明的字段"""
from .base_input import BaseInput
from .text_input import TextInput, NoLabelTextInput
from .select_input import NativeSelectInput, MuiSelectInput, NoLabelMuiSelectInput
from .date_input import DateInput
from .check_box_input import CheckBoxGroupInput


class TextGroupInput(BaseInput):
    INPUTS_LOCATOR = ".//div[@variant='outlined']/div"

    def __init__(self, element):
        super(TextGroupInput, self).__init__(element)
        self.inputs = [TextInput(i) for i in self.element.find_elements_by_xpath(self.INPUTS_LOCATOR)]

    @property
    def value(self):
        """:return input已经输入的值"""
        return self._value

    @value.setter
    def value(self, value: dict):
        for key, value in value.items():
            for i in self.inputs:
                if key in i.name:
                    i.value = value
        self._value = value

    @property
    def inputs_fields(self):
        return [i.name for i in self.inputs]


class SelectAndTextGroupInput(BaseInput):
    INPUTS_LOCATOR = ".//div[@variant='outlined']/div"

    def __init__(self, element):
        super(SelectAndTextGroupInput, self).__init__(element)
        tmp = self.element.find_elements_by_xpath(self.INPUTS_LOCATOR)
        self.select_input = NativeSelectInput(tmp[0])
        self.text_input = NoLabelTextInput(tmp[1])

    @property
    def value(self):
        """:return input已经输入的值"""
        return self._value

    @value.setter
    def value(self, value):
        self.select_input.value = value[0]
        self.text_input.value = value[1]
        self._value = value


class MuiSelectAndTextGroupInput(SelectAndTextGroupInput):
    def __init__(self, element):
        super(MuiSelectAndTextGroupInput, self).__init__(element)
        tmp = self.element.find_elements_by_xpath(self.INPUTS_LOCATOR)
        self.select_input = NoLabelMuiSelectInput(tmp[0], self.element.find_element_by_xpath(self.LABEL_LOCATOR))
        self.text_input = NoLabelTextInput(tmp[1])


class SelectAndDateInput(BaseInput):
    INPUTS_LOCATOR = ".//div[@variant='outlined']/div"

    def __init__(self, element):
        super(SelectAndDateInput, self).__init__(element)
        tmp = self.element.find_elements_by_xpath(self.INPUTS_LOCATOR)
        self.select_input = NativeSelectInput(tmp[0])
        self.date_input = DateInput(tmp[1])

    @property
    def value(self):
        """:return input已经输入的值"""
        return self._value

    @value.setter
    def value(self, value):
        self.select_input.value = value[0]
        self.date_input.value = value[1]
        self._value = value


class MuiSelectAndDateInput(SelectAndDateInput):

    def __init__(self, element):
        super(MuiSelectAndDateInput, self).__init__(element)
        tmp = self.element.find_elements_by_xpath(self.INPUTS_LOCATOR)
        self.select_input = NoLabelMuiSelectInput(tmp[0], self.element.find_element_by_xpath(self.LABEL_LOCATOR))
        self.date_input = DateInput(tmp[1])


class CheckBoxGroupAndTextInput(BaseInput):
    INPUTS_LOCATOR = ".//div[@variant='outlined']/div"

    def __init__(self, element):
        super(CheckBoxGroupAndTextInput, self).__init__(element)
        tmp = self.element.find_elements_by_xpath(self.INPUTS_LOCATOR)
        self.checkbox_group_input = CheckBoxGroupInput(tmp[0])
        self.text_input = NoLabelTextInput(tmp[1])

    @property
    def value(self):
        """:return input已经输入的值"""
        return self._value

    @value.setter
    def value(self, value):
        self.checkbox_group_input.value = value[0]
        self.text_input.value = value[1]
        self._value = value
