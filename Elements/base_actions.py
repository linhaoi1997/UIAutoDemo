"""元素基本行为封装"""

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


def Clear(element):
    """清空输入框内容，部分使用clear没有用，使用这种方法可以"""
    element.clear()
    element.send_keys(Keys.ARROW_DOWN)
    while element.get_attribute("value"):
        element.send_keys(Keys.BACKSPACE)


def Send_keys(element, value):
    """输入之前先清空输入框"""
    Clear(element)
    element.send_keys(value)


def scroll_view(element):
    """使用javascript将元素滚动到页面可以见的位置"""
    element.parent.execute_script("arguments[0].scrollIntoViewIfNeeded();", element)
    WebDriverWait(element.parent, 10).until(expected_conditions.visibility_of(element))


def scroll_view_and_click(element):
    """滚动之后点击"""
    scroll_view(element)
    element.click()


def Click(element: WebElement):
    """等待元素可以点击之后点击"""
    scroll_view(element)
    WebDriverWait(element.parent, 10).until(lambda x: element.is_enabled())
    element.click()
