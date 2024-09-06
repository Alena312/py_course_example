import pytest

from selenium import webdriver
from uuid import uuid4


@pytest.fixture
def browser(request):
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-certificate-errors')

    prefs = {'download.default_directory': '/tmp'}

    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)

    yield driver

    print(f'rep_call: {request.node.rep_call}')

    if request.node.rep_call.failed:
        print("executing test failed", request.node.nodeid)
        driver.save_screenshot(f'{uuid4().hex}.png')
    driver.quit()
