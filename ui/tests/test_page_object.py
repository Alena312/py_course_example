import pytest

from ui.page_object.mainpage import MainPage
from ui.suite.base import BaseSuite


class TestMainPage(BaseSuite):

    @pytest.mark.debug
    @pytest.mark.parametrize('text', ['python'])
    def test_search(self, text):
        page = self.get_page(MainPage)
        page.search_by_text(text)
        assert 'Python' in self.browser.page_source
