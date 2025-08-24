from .base_page import BasePage
class SettingsPage(BasePage):
    def click_internet(self):
        self.click_by_text("Internet")
    def click_wifi(self):
        self.click_by_text("Network & internet")
