import logging

import allure
import pytest
from selenium.webdriver.chromium.webdriver import ChromiumDriver
import typing
from main.ui.page_object.page import BasePage

T = typing.TypeVar('T', bound=BasePage)
# T = typing.TypeVar('T')


class BaseSuite:

    browser: ChromiumDriver
    base_url: str
    logger: logging.Logger

    @pytest.fixture(autouse=True)
    def prepare(self, browser, base_url, logger):
        self.browser = browser
        self.base_url = base_url
        self.logger = logger

        self.logger.info('PREPARE DONE')

    @allure.step('Getting page {page_class}')
    def get_page(self, page_class: typing.Type[T]) -> T:
        self.browser.get(self.base_url + page_class.path)
        # document.readyState \ 'complete', 'eager' - при получении страницы селениум смотрит на состояние страницы
        page = page_class(self.browser)
        assert page.is_page_loaded(), f'{page.path} не загрузилась'
        return page

