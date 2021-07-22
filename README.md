# UIAutoTest

UI自动化测试
选用selenium + page object + pytest + allure

### 六大原则

- 用公共方法代表UI所提供的功能
- 方法应该返回其他的PageObject或者用于断言的数据
- 同样的行为不同的结果可以建模为不同的方法
- 不要在方法内加断言
- 不要暴露页面内部的元素给外部
- 不需要建模页面所有的元素

### [基于前端的组件最大程度减少Page Object的编写成本](https://selenium-python-zh.readthedocs.io/en/latest/page-objects.html#id4.)

- 在page object的基础上引入组件，分层如下
    - 元素：页面的最小定位
    - 组件：先给一个定位定位到组件，再使用相对定位，定位到组件的元素。每个组件有对应的操作，封装成对应的方法。给所有页面复用。
    - 页面：由元素和组件组成，再封装一层方法暴露给用例执行层
- 举个例子，假设前端每个页面使用相同的表格组件，那么每个页面都可以使用这个组件，给出定位就可以。
    - 首先定义组成组件的基本元素

    ```python
    class Element(object):
        def __init__(self, *locator):
            self.locator = locator

        def _handle(self, instance):
            driver = instance.driver
            WebDriverWait(driver, self.wait_time).until(
                lambda d: driver.find_element(*self.locator)
            )
            return driver.find_element(*self.locator)

        def __set__(self, instance, value):
            element = self._handle(instance)
            element.send_keys(value)

        def __get__(self, instance, owner) -> WebElement:
            return self._handle(instance)
    ```

    - 然后使用元素组成组件

    ```python

    class Table(object):

    	search_ele = Element("xpath", "./ancestor::*//input[@type='search']")
    	search_check_box = Element("xpath", "./ancestor::*//div[count(button)>1]/button")
    	page_info = Element("xpath","//div[@class ='MuiTablePagination-root']//p[2]") # 展示第几页的信息
    	
        def __init__(self, element, locator):
    				self.loactor = locator
            self.element = element
    				self.driver = element.parent
            self._handle()
            self.ac = ActionChains(self.element.parent).click(self.element)

        # table一般有搜索框
        @property
        def search_box(self):
            return self.search_ele

        # 有的搜索框有一些筛选按钮
        @property
        def check_buttons(self):
            return self.search_check_box

        # 读取table的头和每一行的值
        @try_refresh
        def _handle(self):
            self.head = THead(self.element.find_element_by_tag_name("thead"))
            self.body = TBody(self.element.find_element_by_tag_name("tbody"), self.head)
            self.start, self.end, self.total_number = self.page_finder.search(self.pages_info.text).groups()
            self.page_operators = self.pages_info.find_elements_by_xpath("./following-sibling::div/button")
    		
    	# 获取第几行
        def __getitem__(self, item):
            return self.body[item]
    		
    	# 筛选表格的值
        @try_refresh
        def filter(self, items: dict, search=''):
            if search:
                Send_keys(self.search_box, search)
                time.sleep(2)
                self.refresh()
            iter_list = self.body
            for key, value in items.items():
                iter_list = list(filter(lambda a: a[key] == str(value), iter_list))
            return list(iter_list)
    ```

    - 页面的调用再封装一层以实时获取

    ```python
    class TableElement(Element):
        template = "//table"

        def __get__(self, instance, owner) -> Table:
            result = super(TableElement, self).__get__(instance, owner)
            return Table(result, *self.locator)
    ```

- 页面中调用

```python
class CompanyJobPage(CompanyBasePage):
    # 搜索栏
    search_job = SearchElement()
    # 岗位信息
    table = TableElement()
		
def enter_detail(self, filter_):
    t = self.table
    self.click(t.search(filter_, search=filter_["岗位名称"]).get_element("操作"))
    return JobDetailPage(self.driver)
```

目录结构

- Elements(基础元素)
    - elements（元素类）
    - locators（把相同的定位方式总结到一起，以复用代码）
- Components（组件）
    - CommonPonents(通用组件)（部分定位可以引用基础元素，部分引用当前层级目录元素）
    - BusinessComponents（业务使用的组件，下面按照模块新增目录）
    - components（按照描述器封装所有组件）
- Pages（页面）
    - 按照业务模块封装（模块-侧边栏）
    - basepage
- Utils（弥补框架不足的工具）
    - Runtest
        - run_tes生成报告，封装运行用例的方法和调试用例的方法
        - load_yaml 调用数据驱动的方法
        - get_driver 调用调试的包,
        - fake 模拟数据的编写
    - AssertTools（使用harmest这个包自己封装通用的匹配器，用例校验时统一使用）
- Data（放置数据驱动的yaml或者excel什么的）
- TestCases（测试用例）
    - 按照业务模块封装（模块-侧边栏）
- loadconfig 读取配置
