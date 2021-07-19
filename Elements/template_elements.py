from selenium.webdriver.common.by import By

from .elements import Element, Elements
from .templates import Templates


class TemplateElement(Element):
    template = ''

    def __init__(self, *args):
        locator = self.template % args
        super(TemplateElement, self).__init__(By.XPATH, locator)


class TemplateElements(Elements):
    template = ''

    def __init__(self, *args):
        locator = self.template % args
        super(TemplateElements, self).__init__(By.XPATH, locator)


class ButtonElement(TemplateElement):
    """ 按钮类型的元素 """
    template = Templates.button


class TopButtonElement(TemplateElement):
    """ 最上层页面的按钮元素，多数情况是弹出框 """
    template = Templates.top_button


class CrumbsElement(TemplateElement):
    """ 面包屑元素 """
    template = Templates.crumb


class SideBarElement(TemplateElement):
    """ 侧边栏 """
    template = Templates.side_bar
