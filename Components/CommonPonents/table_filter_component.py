import logging

from Elements.base_actions import Click
from .form_component import Form
from ..base_component import BaseComponent


class TableFilter(BaseComponent):

    def _handle(self):
        super(TableFilter, self)._handle()
        self._filters = self.element.find_elements_by_xpath(".//div[label]")
        self.clear = self.element.find_element_by_xpath(".//button[contains(span,'清空') or contains(span,'重置') ]")
        self.search = self.element.find_element_by_xpath(".//button[span='查询']")

    @property
    def filters(self):
        result = {}
        for i in self._filters:
            result[i.find_element_by_xpath("./label").text] = \
                i.find_element_by_xpath(".//input/parent::div").text or i.find_element_by_xpath(
                    ".//input").get_attribute('value')
        return result

    @filters.setter
    def filters(self, v: dict):
        form = Form(self.driver, self.locator)
        for key, value in v.items():
            form[key] = value

    def set_filters(self, v):
        self.clear_filters()
        self.filters = v
        Click(self.search)

    def clear_filters(self, is_refresh=False):
        Click(self.clear)
        if is_refresh:
            Click(self.search)
