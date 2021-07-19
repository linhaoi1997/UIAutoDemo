from selenium.webdriver.remote.webdriver import WebDriver

from .table_component import Table

from selenium.webdriver.common.by import By

from .form_component import Form
from .table_filter_component import TableFilter
from .tree_component import Tree
from ..components import Component


class TableComponent(Component):

    def __init__(self, *locator):
        if not locator:
            locator = (By.XPATH, "//table")
        super(TableComponent, self).__init__(*locator)

    def __get__(self, instance, owner):
        driver = instance.driver
        return Table(driver, self.locator)


class TreeComponent(Component):

    def __init__(self, *locator):
        if not locator:
            locator = (By.XPATH, "//ul/div[contains(@class,'TreeItem')]")
        super(TreeComponent, self).__init__(*locator)

    def __get__(self, instance, owner) -> Tree:
        driver = instance.driver
        return Tree(driver, self.locator)


class FormComponent(Component):

    def __init__(self, *locator):
        if not locator:
            locator = (By.XPATH, "//form")
        super(FormComponent, self).__init__(*locator)

    def __get__(self, instance, owner) -> Form:
        driver = instance.driver
        return Form(driver, self.locator)


class TableFilterComponent(Component):

    def __init__(self, *locator):
        if not locator:
            locator = (By.XPATH, "//div[contains(@class,'TableFilter')]")
        super(TableFilterComponent, self).__init__(*locator)

    def __get__(self, instance, owner) -> TableFilter:
        driver = instance.driver
        return TableFilter(driver, self.locator)


class BaseFormLeftWordComponent(Component):
    FORM_LOCATOR = "//div[@variant='outlined']"

    def __init__(self, *locator):
        if not locator:
            locator = (By.XPATH, self.FORM_LOCATOR)
        super(BaseFormLeftWordComponent, self).__init__(*locator)

    def __get__(self, instance, owner):
        driver: WebDriver = instance.driver
        self.element = driver.find_element(*self.locator)
        return self


__all__ = ["Component", "TableComponent", "TableFilterComponent", "FormComponent", "TreeComponent",
           "BaseFormLeftWordComponent"]
