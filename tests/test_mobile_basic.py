import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy  # 需要导入这个
from config.test_config import CONFIG
from pages.settings_page import SettingsPage
def test_mobile_basic():
    options = UiAutomator2Options()
    options.device_name = CONFIG["mobile"]["device_name"]
    options.app_package = CONFIG["mobile"]["app_package"]
    options.app_activity = CONFIG["mobile"]["app_activity"]
    driver = webdriver.Remote(CONFIG["mobile"]["appium_server_url"], options=options)

    settings = SettingsPage(driver)

    # 新增这几行：
    import time

    time.sleep(5)  # 等待5秒，让你看清楚
    print("应用已启动！")

    time.sleep(3)  # 等待页面跳转

    settings.click_wifi()

    time.sleep(5)

    driver.save_screenshot("internet_page.png")
    print("点击network&internet后的界面截图保存！")

    try:
        settings.click_internet()
        print("成功点击Internet选项")
    except:
        print("点击Internet选项失败")

    driver.quit()  # 关闭连接
