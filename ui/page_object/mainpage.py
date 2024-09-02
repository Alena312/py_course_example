from ui.page_object.page import BasePage
from selenium.webdriver.common.by import By


class MainPage(BasePage):
    """
        PageObject: https://python.org/
    """

    path = '/'

    SEARCH_INPUT = (By.CSS_SELECTOR, '#id-search-field')
    GO_BUTTON = (By.CSS_SELECTOR, '#submit')

    def search_by_text(self, text):
        self._send_keys(*self.SEARCH_INPUT, text)
        self._click(*self.GO_BUTTON)
