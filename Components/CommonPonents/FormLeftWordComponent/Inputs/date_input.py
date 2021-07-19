from Components.CommonPonents.FormLeftWordComponent.Inputs.base_input import BaseInput
import datetime


class DateInput(BaseInput):
    @property
    def value(self):
        """:return input已经输入的值"""
        return self._value

    @value.setter
    def value(self, value: datetime.datetime):
        self._value = value
        input_ = self.element.find_element_by_xpath(".//input")
        self.send_keys(input_, value.strftime("%Y%m%d%H%M"))
