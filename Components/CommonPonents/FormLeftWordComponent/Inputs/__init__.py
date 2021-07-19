from typing import Any

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from .base_input import BaseInput
from .check_box_input import CheckBoxGroupInput
from .date_input import DateInput
from .radio_input import RadioGroupInput
from .select_input import NativeSelectInput, MuiSelectInput, SearchSelectInput
from .text_input import TextInput, NumberInput, TextAreaInput, DisableTextInput, NoLabelTextInput
from .group_inputs import TextGroupInput, SelectAndTextGroupInput, MuiSelectAndTextGroupInput, SelectAndDateInput, \
    MuiSelectAndDateInput, CheckBoxGroupAndTextInput
from Utils.SeleniumTools.change_wait_time import change_wait_time


class BaseInputComponent(object):
    OBJ = BaseInput

    def __init__(self, name):
        """
        :param name: input的名称
        """
        self.name = name

    def _match_input(self, element):
        with change_wait_time(element.parent):
            for i in element.find_elements_by_xpath("./div"):
                try:
                    if i.find_element_by_xpath(".//label/p").text.strip(" :") == self.name:
                        return i
                except NoSuchElementException:
                    pass

    def __get__(self, instance, owner) -> Any:
        """
        :param instance: instance应该是存在element，调用get时会根据相对定位找到匹配name的input
        :param owner:
        :return: input
        """
        element: WebElement = instance.element
        input_ = self._match_input(element)
        return self.OBJ(input_)

    def __set__(self, instance, value):
        element: WebElement = instance.element
        input_ = self._match_input(element)
        self.OBJ(input_).value = value


class CheckBoxGroupComponent(BaseInputComponent):
    """复选框组"""
    OBJ = CheckBoxGroupInput

    def __get__(self, instance, owner) -> CheckBoxGroupInput:
        return super(CheckBoxGroupComponent, self).__get__(instance, owner)


class DateInputComponent(BaseInputComponent):
    """日期"""
    OBJ = DateInput

    def __get__(self, instance, owner) -> DateInput:
        return super(DateInputComponent, self).__get__(instance, owner)


class RadioGroupComponent(BaseInputComponent):
    """单选按钮组"""
    OBJ = RadioGroupInput

    def __get__(self, instance, owner) -> RadioGroupInput:
        return super(RadioGroupComponent, self).__get__(instance, owner)


class NativeSelectComponent(BaseInputComponent):
    """下拉单选框"""
    OBJ = NativeSelectInput

    def __get__(self, instance, owner) -> NativeSelectInput:
        return super(NativeSelectComponent, self).__get__(instance, owner)


class MuiSelectInputComponent(BaseInputComponent):
    """多选下拉框"""
    OBJ = MuiSelectInput

    def __get__(self, instance, owner) -> MuiSelectInput:
        return super(MuiSelectInputComponent, self).__get__(instance, owner)


class SearchSelectInputComponent(BaseInputComponent):
    """搜索下拉框"""
    OBJ = MuiSelectInput

    def __get__(self, instance, owner) -> SearchSelectInput:
        return super(SearchSelectInputComponent, self).__get__(instance, owner)


class TextInputComponent(BaseInputComponent):
    """文本输入框"""
    OBJ = TextInput

    def __get__(self, instance, owner) -> TextInput:
        return super(TextInputComponent, self).__get__(instance, owner)


class TextAreaInputComponent(BaseInputComponent):
    """文本输入框"""
    OBJ = TextAreaInput

    def __get__(self, instance, owner) -> TextAreaInput:
        return super(TextAreaInputComponent, self).__get__(instance, owner)


class NumberInputComponent(BaseInputComponent):
    """数字输入框"""
    OBJ = TextInput

    def __get__(self, instance, owner) -> NumberInput:
        return super(NumberInputComponent, self).__get__(instance, owner)


class TitleInputComponent(BaseInputComponent):
    """文本字段，无输入"""
    OBJ = DisableTextInput

    def __get__(self, instance, owner) -> DisableTextInput:
        return super(TitleInputComponent, self).__get__(instance, owner)


class NoLabelTextInputComponent(BaseInputComponent):
    """输入框"""
    OBJ = NoLabelTextInput

    def __get__(self, instance, owner) -> NoLabelTextInput:
        return super(NoLabelTextInputComponent, self).__get__(instance, owner)


class TextGroupComponent(BaseInputComponent):
    """输入框组"""
    OBJ = TextGroupInput

    def __get__(self, instance, owner) -> TextGroupInput:
        return super(TextGroupComponent, self).__get__(instance, owner)


class SelectAndTextGroupComponent(BaseInputComponent):
    """下拉框+输入框"""
    OBJ = SelectAndTextGroupInput

    def __get__(self, instance, owner) -> SelectAndTextGroupInput:
        return super(SelectAndTextGroupComponent, self).__get__(instance, owner)


class MuiSelectAndTextGroupComponent(BaseInputComponent):
    """多选的下拉框+输入框"""
    OBJ = MuiSelectAndTextGroupInput

    def __get__(self, instance, owner) -> MuiSelectAndTextGroupInput:
        return super(MuiSelectAndTextGroupComponent, self).__get__(instance, owner)


class SelectAndDateComponent(BaseInputComponent):
    """下拉框+日期"""
    OBJ = SelectAndDateInput

    def __get__(self, instance, owner) -> SelectAndDateInput:
        return super(SelectAndDateComponent, self).__get__(instance, owner)


class MuiSelectAndDateComponent(BaseInputComponent):
    """多选下拉框+日期"""
    OBJ = MuiSelectAndDateInput

    def __get__(self, instance, owner) -> MuiSelectAndDateInput:
        return super(MuiSelectAndDateComponent, self).__get__(instance, owner)


class CheckBoxGroupAndTextComponent(BaseInputComponent):
    """复选框组+输入框"""
    OBJ = CheckBoxGroupAndTextInput

    def __get__(self, instance, owner) -> CheckBoxGroupAndTextInput:
        return super(CheckBoxGroupAndTextComponent, self).__get__(instance, owner)


__all__ = ["CheckBoxGroupAndTextComponent", "CheckBoxGroupComponent", "TextGroupComponent", "SelectAndDateComponent",
           "MuiSelectAndDateComponent", "MuiSelectInputComponent", "SearchSelectInputComponent", "DateInputComponent",
           "NumberInputComponent", "TitleInputComponent", "TextInputComponent",
           "NoLabelTextInputComponent", "RadioGroupComponent", "SelectAndTextGroupComponent", "NativeSelectComponent",
           "MuiSelectAndTextGroupComponent", "TextAreaInputComponent"]
