"""测试树组件"""
from selenium.webdriver import ActionChains

from Components import TreeComponent
from Elements.base_actions import scroll_view
from Pages.basepage import BasePage

from Utils.RunTest.get_driver import get_driver
from Utils.RunTest.run_test import run


class Page(BasePage):
    path = "https://mc-test.teletraan.io/management/company"
    tree = TreeComponent()


class TestTree:

    def setup_class(self):
        self.driver = get_driver()
        self.tree = Page(self.driver).tree
        url = "https://mc-test.teletraan.io/management/company"
        if self.driver.current_url != url:
            self.driver.get(url)

    def test1(self):
        print(self.tree.all_nodes)

    def test2(self):
        print(self.tree.search("BI测试").text)

    def test3(self):
        ele = self.tree.search("BI测试")
        scroll_view(ele.element)
        ActionChains(self.driver).pause(0.5).double_click(ele.operator[0]).perform()


if __name__ == '__main__':
    run(__file__)
