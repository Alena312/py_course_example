from ui.page_object.page import BasePage
from selenium.webdriver.common.by import By

from ui.page_object.elements_stolen_code import Page, Element


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


class DescrMainPage(Page):

    path = '/'

    search_input = Element(By.CSS_SELECTOR, '#id-search-field', 'Поисковый инпут')
    go_button = Element(By.CSS_SELECTOR, '#submit', 'Кнопка "GO"')
