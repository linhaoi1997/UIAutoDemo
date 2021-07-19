"""测试权限表格的组件"""
import allure

from Components import PermissionTableComponent, Permission
from Utils.RunTest.run_test import run_certain
from Pages.basepage import BasePage

from Utils.RunTest.get_driver import get_driver


class Page(BasePage):
    path = "https://mc-test.teletraan.io/management/role/1239"
    permissions = PermissionTableComponent()


class TestPermissionTable:
    def setup_class(self):
        self.driver = get_driver()
        self.permissions = Page(self.driver).permissions
        url = "https://mc-test.teletraan.io/management/role/1239"
        if self.driver.current_url != url:
            self.driver.get(url)

    def teardown_class(self):
        self.permissions.select_app("客户管理")
        self.driver.quit()

    @allure.title("选择权限")
    def test1(self):
        self.permissions.search("客户清单").change_to(Permission.SELECTED)

    @allure.title("清除所有权限")
    def test2(self):
        self.permissions.clear_permission()

    @allure.title("数据权限选择")
    def test3(self):
        self.permissions.search("删除").change_to(Permission.SELECTED).select_data_permission(Permission.ONLY)

    @allure.title("重名权限的选择")
    def test4(self):
        self.permissions.search_in_order("客户经理清单", "删除").change_to(Permission.SELECTED).select_data_permission(
            Permission.ONLY)

    @allure.title("选择侧边栏的app")
    def test5(self):
        self.permissions.select_app("销售管理")


if __name__ == '__main__':
    run_certain(__file__)
