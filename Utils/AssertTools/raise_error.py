import allure


def raise_assert_error(driver, title):
    allure.attach(driver.get_screenshot_as_png(), title, allure.attachment_type.PNG)
    raise AssertionError(title)
