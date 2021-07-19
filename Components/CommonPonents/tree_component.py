import logging

from selenium.webdriver.support.wait import WebDriverWait

from Elements.base_actions import Click
from ..base_component import BaseComponent
from selenium.webdriver.remote.webelement import WebElement


class Node(object):
    SELECTED = "selected"
    HALF_SELECTED = "half_selected"
    NOT_SELECTED = "not_selected"
    CAN_NOT_UNFOLD = "can_not_unfold"
    NOT_UNFOLD = "not_unfold"
    UNFOLD = "unfold"
    # locator
    TEXT_LOCATOR = "./div[2]"
    UNFOLD_LOCATOR = "./div[1]//button"
    OPERATOR_LOCATOR = "./div[3]//button"

    def __init__(self, element: WebElement, children: list):
        self.element = element
        self.children = children

    @property
    def selected_status(self):
        input_ = self.element.find_element_by_tag_name("input")
        if input_.get_attribute("data-indeterminate") == "true":
            return self.HALF_SELECTED
        elif input_.is_selected():
            return self.SELECTED
        else:
            return self.NOT_SELECTED

    @property
    def text(self):
        return self._find(self.TEXT_LOCATOR).text

    @property
    def unfold_status(self):
        unfold_button = self._find(self.UNFOLD_LOCATOR)
        if "disabled" in unfold_button.get_attribute("class"):
            return self.CAN_NOT_UNFOLD
        elif self.children:
            return self.UNFOLD
        else:
            return self.NOT_UNFOLD

    @property
    def operator(self):
        return self.element.find_elements_by_xpath(self.OPERATOR_LOCATOR)

    def _find(self, locator):
        return self.element.find_element_by_xpath(locator)

    def unfold(self):
        if self.unfold_status == self.NOT_UNFOLD:
            Click(self._find(self.UNFOLD_LOCATOR))
            return True
        else:
            logging.info("%s节点状态为%s，不可以展开" % (self.text, self.unfold_status))
            return False

    def __iter__(self):
        _css = int(self.element.get_attribute("_css"))
        yield self

        def is_child(ele):
            ele_css = ele.get_attribute("_css")
            if ele_css:
                return int(ele_css) > _css

        if self.unfold():
            children = self.element.find_elements_by_xpath("./following-sibling::div")
            for child in children:
                if is_child(child):
                    self.children.append(Node(child, []))
                else:
                    break
        for child in self.children:
            yield from child

    def search(self, name):
        if self.text == name:
            yield self
        else:
            for child in self.children:
                yield from child.search(name)

    def _click_input(self):
        input_ = self.element.find_element_by_tag_name("input")

        def assert_status(status):
            input_.click()
            WebDriverWait(self.element.parent, 10).until(lambda: self.selected_status != status,
                                                         "未达到预期的状态 %s" % status)

        if self.selected_status == self.SELECTED:
            assert_status(self.NOT_SELECTED)
        elif self.selected_status == self.HALF_SELECTED:
            assert_status(self.NOT_SELECTED)
        else:
            assert_status(self.SELECTED)

    def change_to(self, status):
        n = 0
        while self.selected_status != status and n < 3:
            self._click_input()
            n += 1


class Tree(BaseComponent):
    NODE = Node

    # 加载树，并把节点的父节点记录在list里面
    def _handle(self):
        # 父节点列表
        self.tree_parent = []
        self.elements = self.driver.find_elements(*self.locator)

        def get_len(element):
            if element.get_attribute("_css"):
                return int(element.get_attribute("_css"))

        base_len = get_len(self.elements[0])
        last_len = base_len
        record = [-1]
        # 记录树的parent
        for index, i in enumerate(self.elements):
            current_len = get_len(i)
            if current_len is not None:
                if last_len < current_len:
                    last_len = current_len
                    record.append(index - 1)
                elif last_len > current_len:
                    last_len = current_len
                    while len(record) != 1 and get_len(self.elements[record[-1]]) >= last_len:
                        record.pop()
            # 记录每个节点的父节点，如果没有那么记-1
            self.tree_parent.append(record[-1])
        self._iter_tree()

    def _iter_tree(self):
        def get_children(index_):
            result = []
            for par_index in range(len(self.tree_parent)):
                if self.tree_parent[par_index] == index_:
                    result.append(self.NODE(self.elements[par_index], get_children(par_index)))
            return result

        self.node = self.NODE(self.elements[0], get_children(0))
        self.nodes = []
        for par_index2 in range(len(self.tree_parent)):
            if self.tree_parent[par_index2] == -1:
                self.nodes.append(self.NODE(self.elements[par_index2], get_children(par_index2)))

    def search(self, name):
        for i in self.unfold_deep():
            if i.text == name:
                return i
        else:
            raise AssertionError("没找到命名为'%s'的树节点" % name)

    def _unfold(self):
        def unfold_breadth(node):
            yield node.unfold()
            for child in node.children:
                yield from unfold_breadth(child)

        for i in self.nodes:
            yield from unfold_breadth(i)

    def unfold_breadth(self):
        while True in list(self._unfold()):
            self.refresh()

    def unfold_deep(self):
        for node in self.nodes:
            yield from node

    @property
    def all_nodes(self):
        return list(self.unfold_deep())
