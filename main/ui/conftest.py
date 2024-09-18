import os.path

import allure
import pytest

from selenium import webdriver


@pytest.fixture
def browser(request, test_dir):
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-certificate-errors')

    prefs = {'download.default_directory': test_dir}

    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)

    yield driver

    print(f'rep_call: {request.node.rep_call}')
    allure.attach('test text for allure attach', attachment_type=allure.attachment_type.TEXT)


    if request.node.rep_call.failed:
        print("executing test failed", request.node.nodeid)
        browser_log_path = os.path.join(test_dir, 'browser.log')
        with open(browser_log_path, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f'{i["level"]} - {i["source"]}\n{i["message"]}\n\n')

        driver.save_screenshot(os.path.join(test_dir, 'failure.png'))

    driver.quit()
