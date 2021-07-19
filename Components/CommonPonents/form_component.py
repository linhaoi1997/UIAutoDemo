import logging
import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from Elements.base_actions import Click, Send_keys
from Utils.AssertTools.raise_error import raise_assert_error
from Utils.RunTest.fake import fake_plus
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random

from Utils.SeleniumTools.change_wait_time import change_wait_time
from .tree_component import Tree
from ..base_component import BaseComponent


def role_to_radio(element):
    if element.get_attribute("type") == "radio":
        return RadioInput


def role_to_text(element):
    if element.get_attribute("type") == "text":
        return TextInput


def role_to_password(element):
    if element.get_attribute("type") == "password":
        return TextInput


def role_to_select(element):
    if "MuiSelect-nativeInput" in element.get_attribute("class"):
        return NativeSelectionInput


def role_to_search_select(element):
    if "mui" in element.get_attribute("id"):
        return SearchSelectionInput


def role_to_file(element):
    if "file" == element.get_attribute("type"):
        return FileInput


def role_to_text_area(element):
    if "textarea" == element.tag_name:
        return TextInput


def role_to_number(element):
    if element.get_attribute("type") == "number":
        return NumberInput


def role_to_search(element):
    if element.get_attribute("type") == "search":
        return BaseInput


def role_to_checkbox(element):
    if element.get_attribute("type") == "checkbox":
        return CheckBoxInput


class BaseRoleToInput:
    """
    通过规则选择input的类型
    """
    rules = []

    @classmethod
    def choice(cls, element):
        for rule in cls.rules:
            if rule(element):
                return rule(element)
        raise_assert_error(element.parent, "没有规则和元素匹配 %s" % element.get_attribute("name"))

    @classmethod
    def add_rule(cls, func, order=0):
        assert callable(func)
        if order == -1:
            cls.rules.append(func)
        else:
            cls.rules.insert(order, func)


class RoleToInput(BaseRoleToInput):
    rules = [
        role_to_search_select,
        role_to_select,
        role_to_radio,
        role_to_text,
        role_to_password,
        role_to_file,
        role_to_text_area,
        role_to_number,
        role_to_search,
        role_to_checkbox
    ]


class BaseInput(object):
    FOCUS_LOCATOR = ".."
    HINT_LOCATOR = "./ancestor::div/following-sibling::p"
    LABEL_LOCATOR = "./ancestor::div/preceding-sibling::label"

    def __init__(self, input_element):
        self.element = input_element
        self._value = None
        self.handled = False
        self.name = self._handle_name()
        self.attribute_name = self._handle_attribute_name()

    def get_name(self):
        path = self.LABEL_LOCATOR  # 向上查找祖先div的兄弟节点label节点的值
        return self.element.find_element_by_xpath(path).text.split("\u2009")

    def _handle_name(self):
        names = self.get_name()
        if names[0] and names[0][-1] == "*":
            return names[0][:-1]
        else:
            return names[0]

    def _handle_attribute_name(self):  # 返回input标签的name属性，一般是标识发送接口的字段名，暂时用不到
        return self.element.get_attribute("name")

    @property
    def required(self):
        return self.element.get_attribute("required")

    @property
    def is_focus(self):
        return "focused" in self.element.find_element_by_xpath(self.FOCUS_LOCATOR).get_attribute("class")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.element.clear()
        self.element.send_keys(Keys.ARROW_DOWN)  # 不这么做无法成功清除值
        while self.element.get_attribute("value"):
            self.element.send_keys(Keys.BACKSPACE)
        self.element.send_keys(value)
        self.handled = True

    @property
    def hint(self):  # 获取警告
        return self.element.find_element_by_xpath(self.HINT_LOCATOR).text

    @property
    def changeable(self):
        return "disabled" not in self.element.get_attribute("class")

    def fake(self):  # mock一个值
        if self.changeable:
            name = self.name
            self.value = fake_plus(name)

    def click_while(self, condition="is_focus"):  # 选中输入框
        ac = ActionChains(self.element.parent)
        ac.click(self.element)
        for i in range(3):
            if not getattr(self, condition):
                ac.perform()
            else:
                break
        else:
            raise_assert_error(self.element.parent, "%s 没有被选中" % self.name)


class TextInput(BaseInput):
    type = "text"
    LIMIT_LOCATOR = "./parent::*/parent::*/following-sibling::p"

    @property
    def limit(self):  # 文本输入框有限制值
        return int(self.element.find_element_by_xpath(self.LIMIT_LOCATOR).text.split("/")[-1])


class NumberInput(BaseInput):
    type = "number"

    def fake(self):  # 数字不好弄规则，全部mock 1
        if self.changeable:
            self.element.clear()
            self.element.send_keys(1)


class RadioInput(BaseInput):
    type = "radio"  # radio标签特殊处理，有多个input，但是name属性是同一个值
    CHOICE_LOCATOR = "./ancestor::label/span[last()]"

    def __init__(self, element):
        super(RadioInput, self).__init__(element)
        self.elements = [element]

    def _choice(self, element):
        element.click()
        self._value = element.find_element_by_xpath(self.CHOICE_LOCATOR).text

    def choice(self, value):
        for i in self.elements:
            if i.find_element_by_xpath(self.CHOICE_LOCATOR).text == value:
                self._choice(i)
                break
        else:
            raise_assert_error(self.element.parent, "无效的value %s" % value)

    def fake(self):
        if self.changeable:
            element = random.choice(self.elements)
            self._choice(element)

    def add_radio(self, element):
        self.elements.append(element)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.choice(value)
        self.handled = True


# 下拉框
class NativeSelectionInput(BaseInput):
    type = "selection"
    OPTIONS_LOCATOR = "//div[@role='presentation']"
    TREE_NODES_LOCATOR = ".//ul/div[contains(@class,'Tree')]"
    DIV_LOCATOR = "./preceding-sibling::div"

    @property
    def options(self):  # 点击下拉框之后拿到所有可选项
        self.expand()
        with change_wait_time(self.element.parent):
            lis: WebElement = self.element.find_elements_by_xpath(self.OPTIONS_LOCATOR)[-1].find_elements_by_xpath(
                ".//li")
        if lis:
            return lis
        else:
            tree_elements = self.element.find_elements_by_xpath(self.OPTIONS_LOCATOR)[-1].find_element_by_xpath(
                self.TREE_NODES_LOCATOR
            )
            if tree_elements:
                logging.info("下拉框为tree节点")
                return [i.element for i in
                        Tree(self.element.parent, ("xpath", "//ul/div[contains(@class,'Tree')]")).all_nodes]
            else:
                raise_assert_error(self.element.parent, "未识别的节点")

    @property
    def is_expand(self):
        return self.element.find_element_by_xpath(self.DIV_LOCATOR).get_attribute("aria-expanded") == "true"

    def expand(self):
        for i in range(3):
            self.click_while("is_expand")
            if not self.is_expand:
                print("没展开成功")
            else:
                break
        else:
            raise_assert_error(self.element.parent, "没展开成功")

    def _choice(self, element):
        self._value = element.text
        Click(element)
        # 如果还是展开，说明是多选
        n = 0
        while self.is_expand and n < 3:
            ele = self.element.find_element_by_xpath("//div[contains(@class,'MuiAvatar-circle')]")
            ActionChains(self.element.parent).move_to_element(ele).click().perform()
            time.sleep(1)
            n += 1

    def choice(self, value):
        for i in self.options:
            if i.text == value:
                return self._choice(i)
        raise_assert_error(self.element.parent, "无效的value %s" % value)

    def fake(self):
        options = self.options
        if options:
            self._choice(random.choice(list(options)))
        else:
            raise_assert_error(self.element.parent, "没有可选值")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.choice(value)
        self.handled = True


# 可以搜索的下拉框
class SearchSelectionInput(NativeSelectionInput):
    type = "selection"
    DIV_LOCATOR = "../../.."

    def search(self, value):  # 有些下拉框可以输入文字搜索
        Send_keys(self.element, value)
        self.value = value


class FileInput(BaseInput):
    type = "file"

    def get_name(self):
        return ["图片"]

    def upload(self, file_path):  # 上传文件字段，只需要调用send_key方法，把文件路径发给input
        self.element.send_keys(file_path)

    def fake(self):
        """待实现"""
        # from tempfile import TemporaryFile
        # path = os.path.join(config.get_file_path("root_dir"), 'support/test_file/images')
        # file_path = os.path.join(path, random.choice(os.listdir(path)))
        # self.upload(os.path.abspath(file_path))


class CheckBoxInput(BaseInput):
    type = "checkbox"  # 新增的复选框字段
    LABEL_LOCATOR = "./ancestor::label"

    @property
    def value(self):
        return self.element.is_selected()

    @value.setter  # 设定复选框的值只有选中还是没选中，bool值
    def value(self, value: bool):
        if value != self.value:
            Click(self.element)
        self._value = value
        self.handled = True


class Form(BaseComponent):
    """form"""

    def _handle(self):
        # radio 类型的input要把name相同的分在一起
        super(Form, self)._handle()
        inputs = []

        def search(name_):
            for input_ in inputs:
                if input_.attribute_name == name_:
                    return input_

        # 拿到所有的input节点
        __inputs = self.element.find_elements_by_tag_name("input,textarea")

        for i in __inputs:
            name = i.get_attribute("name")
            input_type = RoleToInput.choice(i)
            result = search(name) if name else None  # 如果查找到了一样的name说明是一个radio组件，那么特殊处理
            if not result:
                inputs.append(input_type(i))
            else:
                result.add_radio(i)
        self.inputs = inputs
        self._params = {}

    # 拿到表单的所有可以填写的项
    @property
    def all_field(self):
        result = []
        for input_ in self.inputs:
            result.append(input_.name)
        return result

    # 找到表单的字段
    def search(self, name):
        for input_ in self.inputs:
            if input_.name == name:
                return input_
        raise_assert_error(self.element.parent, "not found input named %s " % name)

    def __getattr__(self, item):
        return self.search(item)

    # 变为可迭代的
    def __iter__(self):
        yield from self.inputs

    # 使用test["字段"] 直接调用
    def __getitem__(self, item) -> BaseInput:
        return self.search(item)

    # 使用test["字段"]="值1"直接修改输入框
    def __setitem__(self, key, value):
        # 如果操作标记这个input，确保提交之后不会覆盖操作
        input_ = self.search(key)
        input_.value = value

    # 底层使用faker mock数据
    def fake(self, submit=True):
        for i in self:
            # 检查是否标记为已操作
            if not getattr(i, "handled"):
                try:
                    i.fake()
                except Exception as e:
                    raise_assert_error(self.element.parent, str(e))
        result = self.params
        if submit:
            self.submit()
        return result

    # 输入dict，批量修改表单
    def change(self, key_value: dict):
        for key, value in key_value.items():
            self[key] = value

    # 提交
    def submit(self, excepted_condition=None):
        self.element.submit()
        WebDriverWait(self.driver, 10).until(expected_conditions.invisibility_of_element(self.element))

    @property
    def params(self):
        """get all changes"""
        result = {}
        for i in self.inputs:
            result[i.name] = i.value
        self._params = result
        return result
