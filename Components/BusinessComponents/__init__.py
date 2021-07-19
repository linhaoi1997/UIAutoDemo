from selenium.webdriver.common.by import By

from ..components import Component

from .permission_table_component import PermissionTable, Permission


class PermissionTableComponent(Component):

    def __init__(self, *locator):
        if not locator:
            locator = (By.XPATH, "//div[contains(@class,'permissionTable')]")
        super(PermissionTableComponent, self).__init__(*locator)

    def __get__(self, instance, owner) -> PermissionTable:
        driver = instance.driver
        return PermissionTable(driver, self.locator)


__all__ = ["PermissionTableComponent", "Permission"]
