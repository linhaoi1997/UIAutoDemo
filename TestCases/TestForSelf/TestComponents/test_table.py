from Components import TableComponent
from Utils.RunTest.run_test import run_certain
from Pages.basepage import BasePage

from Utils.RunTest.get_driver import get_driver


class Page(BasePage):
    path = "https://mc-test.teletraan.io/management/platformUser"
    table = TableComponent()


class TestTable:
    def setup_class(self):
        self.driver = get_driver()
        self.table = Page(self.driver).table
        url = "https://mc-test.teletraan.io/management/platformUser"
        if self.driver.current_url != url:
            self.driver.get(url)
        self.filter = {"平台账号": "ceshi_pingtai_019"}
        self.filter2 = {"平台账号": "teacher"}

    def teardown_class(self):
        self.driver.quit()

    def test1(self):
        assert self.table.to_dict()

    def test2(self):
        print(self.table.search(self.filter))
        assert self.table.search(self.filter)

    def test3(self):
        self.table.search(self.filter).operation.buttons[0].click()
        self.driver.find_element_by_xpath("//button[span='取消']").click()

    def test4(self):
        self.table.next_page()
        self.table.search(self.filter2)
        self.table.previous_page()
        self.table.search(self.filter)


if __name__ == '__main__':
    run_certain(__file__)
