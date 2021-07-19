from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from Components.base_component import BaseComponent


class FormLeftWord(BaseComponent):
    """左字右框的表单,要求定位到div排列的上面一层，'//div[h4="基础信息"]//div[@variant='outlined']'"""

    def __init__(self, driver: WebDriver, locator):
        super(FormLeftWord, self).__init__(driver, locator)
