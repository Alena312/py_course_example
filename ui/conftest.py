import pytest
from selenium import webdriver
from uuid import uuid4


def pytest_addoption(parser):
    parser.addoption('--url', default='https://www.python.org', help='URL для запуска тестов')


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope='session')
def base_url(request):
    return request.config.getoption('--url')


@pytest.fixture
def browser(request):
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    prefs = {'download.default_directory': '/tmp'}

    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)

    yield driver

    print(f'rep_call: {request.node.rep_call}')

    if request.node.rep_call.failed:
        print("executing test failed", request.node.nodeid)
        driver.save_screenshot(f'{uuid4().hex}.png')
    driver.quit()
