import allure
import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from Components import FormComponent
from Pages.basepage import BasePage
from Elements.elements import Element
from Utils.RunTest.get_driver import get_driver
from Utils.RunTest.run_test import run


class Page(BasePage):
    path = "https://mc-test.teletraan.io/management/company"
    form = FormComponent()
    add_button = Element(By.XPATH, "//div[contains(h6,'企业列表')]/button")


class TestTree:

    def setup_class(self):
        self.driver = get_driver()
        p = Page(self.driver)
        try:
            self.driver.find_element_by_xpath("//form")
        except NoSuchElementException:
            p.add_button.click()
        finally:
            self.form = p.form

        url = "https://mc-test.teletraan.io/management/company"
        if self.driver.current_url != url:
            self.driver.get(url)

    @allure.title("拿出表单所有值")
    def test1(self):
        assert self.form.all_field == ['企业名称', '所属行业', '省', '市', '区', '详细地址', '统一社会信用代码',
                                       '电子邮件', '手机号码']

    @allure.title("拿出表单设置的所有值")
    def test2(self):
        assert self.form.params == {'企业名称': None, '所属行业': None, '省': None, '市': None, '区': None, '详细地址': None,
                                    '统一社会信用代码': None, '电子邮件': None, '手机号码': None}

    @allure.title("修改表单中的值")
    def test3(self):
        name = "22333"
        self.form["企业名称"] = name
        assert self.form.params == {'企业名称': name, '所属行业': None, '省': None, '市': None, '区': None, '详细地址': None,
                                    '统一社会信用代码': None, '电子邮件': None, '手机号码': None}

    @allure.title("找不到input name时报错")
    def test4(self):
        with pytest.raises(AssertionError):
            self.form["企业名称1"] = ""

    @allure.title("处理树下拉框选项的表现")
    def test5(self):
        self.form["所属行业"] = "光电"

    @allure.title("处理列表下拉框选项的表现")
    def test6(self):
        self.form["省"] = "北京市"


if __name__ == '__main__':
    run(__file__)
