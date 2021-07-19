import logging

from selenium.webdriver.support.wait import WebDriverWait

from Components.base_component import BaseComponent
from Elements.base_actions import scroll_view, scroll_view_and_click
from Utils.AssertTools.raise_error import raise_assert_error


class Permission:
    SELECTED = "selected"
    NOT_SELECTED = 'not_selected'
    HALF_SELECTED = 'half_selected'
    ALL = "all"
    ONLY = "only"

    name_locator = ".//div[contains(@class,'Tree')]/span"
    button_locator = ".//input[@type='radio']"

    def __init__(self, element):
        self.element = element
        self.name = self.element.find_element_by_xpath(self.name_locator).text

    @property
    def selected_status(self):
        """返回节点被选中的状态：选中，半选，未选中"""
        input_ = self.element.find_element_by_tag_name("input")
        if input_.get_attribute("data-indeterminate") == "true":
            return self.HALF_SELECTED
        elif input_.is_selected():
            return self.SELECTED
        else:
            return self.NOT_SELECTED

    def _click_input(self):
        """点击元素，并校验点击成功，点击之后状态必变"""
        input_ = self.element.find_element_by_tag_name("input")

        def assert_status(status):
            scroll_view(self.element)
            input_.click()
            if not self._check_status(status):
                raise_assert_error(input_.parent, "未达到预期的状态 %s" % status)

        if self.selected_status == self.SELECTED:
            assert_status(self.NOT_SELECTED)
        elif self.selected_status == self.HALF_SELECTED:
            assert_status(self.NOT_SELECTED)
        else:
            assert_status(self.SELECTED)

    def _check_status(self, status):
        """校验input的选中状态是否与预期一致，由于目前页面反应慢, 设定最晚时间20s,如果还是不一致，返回False"""
        return WebDriverWait(self.element.parent, 5).until(lambda x: self.selected_status == status)

    def change_to(self, status):
        """把节点变为想要的状态，只有三种：SELECTED HALF_SELECTED NOT_SELECTED"""
        if self.selected_status != status:
            logging.info("将 %s 的input节点状态变为 %s " % (self.name, status))
            self._click_input()
        else:
            logging.info(" %s 的input节点状态已经是 %s ，不需要操作" % (self.name, status))
        return self

    def select(self):
        """勾选input"""
        self.change_to(self.SELECTED)

    def select_data_permission(self, data_permission):
        """
        选择数据权限
        :Args
            - data_permission - 选择数据权限: "全部数据"：all 或者"仅角色新增" only
        """
        buttons = self.element.find_elements_by_xpath(self.button_locator)
        logging.info("将 %s 节点的数据权限修改为 %s " % (self.name, data_permission))
        if data_permission == self.ALL:
            scroll_view(self.element)
            buttons[0].click()
        else:
            scroll_view(self.element)
            buttons[1].click()
        return self


class PermissionTable(BaseComponent):
    """
    描述：平台选择角色的操作
    一般定位："//div[contains(@class,'permissionTable')]"
    """
    items_locator = "./div[2]/div"
    tab_locator = "//div[contains(@class,'permissionTable') and contains(@class,'MuiTabs-vertical')]"

    def _handle(self):
        super(PermissionTable, self)._handle()
        self.nodes = [Permission(i) for i in self.element.find_elements_by_xpath(self.items_locator)]
        self.root = self.nodes[0]
        self.apps = self.driver.find_element_by_xpath(self.tab_locator).find_elements_by_tag_name("button")

    def clear_permission(self):
        self.nodes[0].change_to(Permission.NOT_SELECTED)

    def search(self, name):
        """搜索并返回节点"""
        for node in self.nodes:
            if node.name == name:
                return node
        else:
            raise_assert_error(self.element.parent, "没找到%s节点" % name)

    def search_in_order(self, *args):
        """有时多个层级可能有相同的名称，那么依次传入层级进行定位"""
        index = 0
        for node in self.nodes:
            if node.name == args[index]:
                if index != len(args) - 1:
                    index += 1
                else:
                    return node
        else:
            raise_assert_error(self.element.parent, f"按顺序没找到 {args}节点")

    def select_app(self, name):
        """选择侧边栏，点击某个侧边栏，会展示该app的权限table"""
        for i in self.apps:
            if i.text == name:
                return scroll_view_and_click(i)
        else:
            raise_assert_error(self.element.parent, "没找到名称为 %s 的app" % name)