from main.ui.page_object.downloadpage import DownloadsPage
from main.ui.page_object.page import BasePage
from selenium.webdriver.common.by import By


class MainPageLocators:
    SEARCH_INPUT = (By.CSS_SELECTOR, '#id-search-field')
    GO_BUTTON = (By.CSS_SELECTOR, '#submit')
    DOWNLOAD_LINK = (By.CSS_SELECTOR, '#downloads > a')


class MainPage(BasePage):
    """
    PageObject: https://python.org/
    """

    path = '/'
    locators = MainPageLocators()

    def is_page_loaded(self) -> bool:
        self.wait.until(lambda _: self._find_element(*self.locators.SEARCH_INPUT))
        return True

    def search_by_text(self, text):
        self._send_keys(*self.locators.SEARCH_INPUT, text)
        self._click(*self.locators.GO_BUTTON)

    def go_to_downloads(self) -> DownloadsPage:
        self._click(*self.locators.DOWNLOAD_LINK)
        return DownloadsPage(self._driver)

    def get_search_input(self):
        return self._find_element(*self.locators.SEARCH_INPUT)
