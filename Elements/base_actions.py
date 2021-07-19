from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


def Clear(element):
    element.clear()
    element.send_keys(Keys.ARROW_DOWN)
    while element.get_attribute("value"):
        element.send_keys(Keys.BACKSPACE)


def Send_keys(element, value):
    Clear(element)
    element.send_keys(value)


def scroll_view(element):
    element.parent.execute_script("arguments[0].scrollIntoViewIfNeeded();", element)
    WebDriverWait(element.parent, 10).until(expected_conditions.visibility_of(element))


def scroll_view_and_click(element):
    scroll_view(element)
    element.click()


def Click(element: WebElement):
    scroll_view(element)
    WebDriverWait(element.parent, 10).until(lambda x: element.is_enabled())
    element.click()
