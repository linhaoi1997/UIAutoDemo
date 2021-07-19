import logging

import allure
from selenium.webdriver.common.by import By

from Components import TableFilterComponent
from Utils.RunTest.run_test import run_certain
from Pages.basepage import BasePage

from Utils.RunTest.get_driver import get_driver


class Page(BasePage):
    path = "https://mc-test.teletraan.io/subapp/sale/order"
    table_filter = TableFilterComponent(By.XPATH, "//form")


class TestTableFilter:
    def setup_class(self):
        self.driver = get_driver()
        self.table_filter = Page(self.driver).table_filter

    @allure.title("拿到所有的filter")
    def test1(self):
        logging.info(self.table_filter.filters)
        assert self.table_filter.filters

    @allure.title("清除filter")
    def test2(self):
        self.table_filter.clear_filters()

    @allure.title("设定filter")
    def test3(self):
        self.table_filter.set_filters(
            {
                "客户经理": "xin001",
                "收款情况": "已收款",
                "关键字": "1"
            }
        )


if __name__ == '__main__':
    run_certain(__file__)
