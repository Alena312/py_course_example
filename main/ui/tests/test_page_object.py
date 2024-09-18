import time

import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.relative_locator import with_tag_name, locate_with


from main.ui.page_object.mainpage import MainPage
from main.ui.suite.base import BaseSuite


class TestMainPage(BaseSuite):

    @pytest.mark.skip
    @pytest.mark.parametrize('text', ['python'])
    def test_search(self, text):
        page = self.get_page(MainPage)
        page.search_by_text(text)
        assert 'python' in self.browser.current_url

    @pytest.mark.skip
    def test_go_to_another_page(self):
        main_page = self.get_page(MainPage)
        download_page = main_page.go_to_downloads()
        assert download_page.is_page_loaded(), f'Страница {download_page.path} не загрузилась'
        assert download_page.get_widget_title_text() == 'Active Python Releases', 'Неправильный тайтл'

    @pytest.mark.skip
    def test_scroll(self):
        main_page = self.get_page(MainPage)
        main_page.scroll(9999, 9999)
        main_page.scroll(-9999, -9999)

    @pytest.mark.skip
    def test_scroll_by_element(self):
        main_page = self.get_page(MainPage)
        main_page.scroll(9999, 9999)
        main_page.scroll_by_element(main_page.get_search_input())

    @pytest.mark.skip
    def test_drag_n_drop(self):
        self.browser.get('https://codepen.io/ThibaultJanBeyer/full/pNOWeq')
        window_id = self.browser.current_window_handle

        self.browser.switch_to.frame(
            self.browser.find_element(By.CSS_SELECTOR, 'iframe')
        )
        ac = ActionChains(self.browser)
        element1 = self.browser.find_element(By.CSS_SELECTOR, '#element1')
        # ac.drag_and_drop_by_offset(element1, xoffset=500, yoffset=0).pause(1).drag_and_drop_by_offset(element1, xoffset=450, yoffset=0).perform()
        drop_zone_1 = self.browser.find_element(By.CSS_SELECTOR, '#dropZone1')
        ac.drag_and_drop(element1, drop_zone_1).perform()

        # self.browser.switch_to.parent_frame()
        self.browser.switch_to.window(window_id)

    @pytest.mark.skip
    def test_geolocation(self):
        params = {
            'latitude': 42.1408845,
            'longitude': -72.5033907,
            'accuracy': 100
        }
        self.browser.execute_cdp_cmd('Emulation.setGeolocationOverride', params)
        self.browser.get('https://www.google.com/maps')
        time.sleep(5)
        element = WebDriverWait(self.browser, 20).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'div[id="mylocation"]'))
        )
        element.click()
        time.sleep(5)

    @pytest.mark.skip
    def test_hide_scrollar(self):
        self.browser.execute_cdp_cmd('Emulation.setScrollbarsHidden', {'hidden': True})
        self.browser.get('https://www.google.com/')
        time.sleep(1)
        self.browser.set_window_size(500, 400)
        time.sleep(5)

    @pytest.mark.skip
    def test_rel_locators(self):
        self.browser.get('https://www.python.org/')
        self.browser.maximize_window()
        element_1 = self.browser.find_element(By.CSS_SELECTOR, '.icon-search+label')
        element_2 = self.browser.find_element(By.CSS_SELECTOR, 'button.search-button')
        # используем имя тега и относительные локаторы, чтобы найти элемент между ними
        # elements = self.browser.find_elements(with_tag_name("input").below(element_1))
        elements = self.browser.find_elements(locate_with(By.CSS_SELECTOR, 'input').near(element_1))

    def test_browser_logs(self):
        self.browser.get('https://ngs.ru/')
        assert 0
