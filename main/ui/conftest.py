import logging
import os.path

import allure
import pytest

from selenium import webdriver


@pytest.fixture()
def logger(test_dir):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s')
    log_file = os.path.join(test_dir, 'debug.log')
    log_level = logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

    allure.attach.file(log_file, 'debug.log', attachment_type=allure.attachment_type.TEXT)


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

    if request.node.rep_call.failed:
        print("executing test failed", request.node.nodeid)
        browser_log_path = os.path.join(test_dir, 'browser.log')

        with open(browser_log_path, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f'{i["level"]} - {i["source"]}\n{i["message"]}\n\n')

        with open(browser_log_path, 'r') as f:
            allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)

        screenshot_path = os.path.join(test_dir, 'failure.png')
        driver.save_screenshot(screenshot_path)
        allure.attach.file(screenshot_path, 'failure.png', attachment_type=allure.attachment_type.PNG)

    driver.quit()
