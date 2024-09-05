import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from ui.page_object.mainpage import MainPage
from ui.suite.base import BaseSuite


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
