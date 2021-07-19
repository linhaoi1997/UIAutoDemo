import datetime

from Utils.RunTest.get_driver import get_driver
from Components import BaseFormLeftWordComponent
from Components.CommonPonents.FormLeftWordComponent.Inputs import *
from Pages.basepage import BasePage


class SaleForm(BaseFormLeftWordComponent):
    wish_date = DateInputComponent("期望交期")
    amount_received = NumberInputComponent("已收款金额")
    amount_percent = NumberInputComponent("已收款百分比")
    self_define1 = CheckBoxGroupAndTextComponent("新增字段")
    notify_production_conditions = RadioGroupComponent("通知生产条件")
    notify_sale_conditions = RadioGroupComponent("通知发货条件")
    remark = TextAreaInputComponent("备注")
    mui_select_adn_date = MuiSelectAndDateComponent("下拉框+日期")
    check_and_text = CheckBoxGroupAndTextComponent("复选框组+输入框")

    def __get__(self, instance, owner):
        driver = instance.driver
        self.element = driver.find_element(*self.locator)
        return self


class UsePage(BasePage):
    path = "subapp/sale/order/create"
    form = SaleForm()


class TestInput:

    def setup_class(self):
        self.driver = get_driver()
        self.form = UsePage(self.driver, auto_jump=False).form

    def test(self):
        self.form.wish_date = datetime.datetime.today()
        self.form.amount_received = 10000
        self.form.amount_percent = 20
        self.form.notify_production_conditions = "即时生产"
        self.form.notify_sale_conditions = "手动通知"
        self.form.remark = "test"
        self.form.self_define1 = [["1", "2"], "cesces"]
        self.form.mui_select_adn_date = [["1", "2"], datetime.datetime.today()]
        self.form.check_and_text = [["1", "2"], "cescesces"]


if __name__ == '__main__':
    from Utils.RunTest.run_test import run_certain

    run_certain(__file__)
