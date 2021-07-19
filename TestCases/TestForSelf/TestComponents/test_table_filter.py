import allure

from Components import TableFilterComponent
from Utils.RunTest.run_test import run_certain
from Pages.basepage import BasePage

from Utils.RunTest.get_driver import get_driver


class Page(BasePage):
    path = "https://mc-test.teletraan.io/management/user"
    table_filter = TableFilterComponent()


class TestTableFilter:
    def setup_class(self):
        self.driver = get_driver()
        self.table_filter = Page(self.driver).table_filter
        url = "https://mc-test.teletraan.io/management/user"
        if self.driver.current_url != url:
            self.driver.get(url)

    @allure.title("拿到所有的filter")
    def test1(self):
        assert self.table_filter.filters

    @allure.title("清除filter")
    def test2(self):
        self.table_filter.clear_filters()

    @allure.title("设定filter")
    def test3(self):
        self.table_filter.set_filters(
            {
                "直属组织": "erp测试",
                "角色": "erp_role",
                "账户状态": "允许登录",
                "关键字": "1"
            }
        )


if __name__ == '__main__':
    run_certain(__file__)
