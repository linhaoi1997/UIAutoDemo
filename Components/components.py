from .base_component import BaseComponent


class Component(object):

    def __init__(self, *locator):
        self.locator = locator

    def __get__(self, instance, owner):
        driver = instance.driver
        return BaseComponent(driver, self.locator)
