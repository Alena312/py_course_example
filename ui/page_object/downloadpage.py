from ui.page_object.page import BasePage
from selenium.webdriver.common.by import By


class DownloadsPage(BasePage):
    """
    PageObject: https://www.python.org/downloads/
    """

    path = '/downloads'
    WIDGET_TITLE = (By.CSS_SELECTOR, '.active-release-list-widget .widget-title')

    def is_page_loaded(self) -> bool:
        return self.path in self._driver.current_url

    def get_widget_title_text(self):
        return self._find_element(*self.WIDGET_TITLE).text
