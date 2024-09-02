import pytest
from selenium.webdriver.chromium.webdriver import ChromiumDriver
import typing
from ui.page_object.page import BasePage

T = typing.TypeVar('T', bound=BasePage)


class BaseSuite:

    browser: ChromiumDriver
    base_url: str

    @pytest.fixture(autouse=True)
    def prepare(self, browser, base_url):
        self.browser: ChromiumDriver = browser
        self.base_url: str = base_url

    def get_page(self, page_class: typing.Type[T]) -> T:
        self.browser.get(self.base_url + page_class.path)
        return page_class(self.browser)
