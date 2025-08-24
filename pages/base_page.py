from appium.webdriver.common.appiumby import AppiumBy  # 需要导入这个
from selenium.webdriver.support.ui import WebDriverWait  # 这个！
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 3
        self.wait = WebDriverWait(self.driver,self.timeout)

    def find_by_text(self,text):
        return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'text("{text}")')
    def click_by_text(self,text):
        find = self.find_by_text(text)
        find.click()