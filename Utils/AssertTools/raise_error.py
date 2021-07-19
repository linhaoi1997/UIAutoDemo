import allure


def raise_assert_error(driver, title):
    """错误，然后截图"""
    allure.attach(driver.get_screenshot_as_png(), title, allure.attachment_type.PNG)
    raise AssertionError(title)
