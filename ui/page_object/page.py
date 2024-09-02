from typing import List

from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from abc import abstractmethod


class BasePage:

    @property
    @abstractmethod
    def path(self):
        raise NotImplementedError

    def __init__(self, driver):
        self._driver: ChromiumDriver = driver
        self.wait = WebDriverWait(self._driver, 10)

    def _get_waiter(self, time):
        return WebDriverWait(self._driver, time)

    def _find_element(self, by, locator) -> WebElement:
        return self._driver.find_element(by, locator)

    def _find_elements(self, by, locator) -> List[WebElement]:
        return self._driver.find_elements(by, locator)

    def _click(self, by, locator):
        self.wait.until(ec.visibility_of_element_located((by, locator)))
        self._find_element(by, locator).click()

    def _click_after_time(self, by, locator, time):
        self._get_waiter(time).until(ec.visibility_of_element_located((by, locator)))
        return self._click(by, locator)

    def _send_keys(self, by, locator, text):
        self.wait.until(ec.visibility_of_element_located((by, locator)))
        self._find_element(by, locator).clear()
        self._find_element(by, locator).send_keys(text)
