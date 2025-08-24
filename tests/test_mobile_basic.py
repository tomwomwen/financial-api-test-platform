import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy  # 需要导入这个


def test_mobile_basic():
    options = UiAutomator2Options()
    options.device_name = "emulator-5554"
    options.app_package = "com.android.settings"
    options.app_activity = ".Settings"
    driver = webdriver.Remote("http://localhost:4723", options=options)

    # 新增这几行：
    import time

    time.sleep(5)  # 等待5秒，让你看清楚
    print("应用已启动！")

    time.sleep(3)  # 等待页面跳转

    wifi_button = driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR, 'text("不存在的按钮")'
    )
    wifi_button.click()

    time.sleep(5)

    driver.save_screenshot("internet_page.png")
    print("点击network&internet后的界面截图保存！")

    try:
        internet_button = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, 'text("Internet")'
        )
        internet_button.click()
        print("成功点击Internet选项")
    except:
        print("点击Internet选项失败")

    driver.quit()  # 关闭连接
