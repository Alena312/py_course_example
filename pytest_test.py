import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.skip
@pytest.mark.parametrize('title', ['Google', 'Not'])
def test_title(browser, title):
    time.sleep(1)
    assert browser.title == title


@pytest.mark.skip
def test_waiting_callback(browser):
    # browser.implicitly_wait(15)
    wait = WebDriverWait(browser, 15)

    def wait_slider(browser):
        print('ждем движения слайдера')
        return browser.find_element(By.XPATH, '//*[@id="dive-into-python"]/ul[2]/li[2]/div[2]/p/a').is_displayed()

    wait.until(wait_slider)

    browser.find_element(By.XPATH, '//*[@id="dive-into-python"]/ul[2]/li[2]/div[2]/p/a').click()
    assert 'An Informal Introduction to Python' in browser.title



def test_waiting_ec(browser):
    wait = WebDriverWait(browser, 15)
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dive-into-python"]/ul[2]/li[2]/div[2]/p/a')))

    browser.find_element(By.XPATH, '//*[@id="dive-into-python"]/ul[2]/li[2]/div[2]/p/a').click()
    assert 'An Informal Introduction to Python' in browser.title

@pytest.mark.skip
def test_download(browser):
    browser.get('https://www.python.org/downloads/')

    wait = WebDriverWait(browser, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.download-for-current-os .download-os-windows .download-buttons a')))
    browser.find_element(By.CSS_SELECTOR, '.download-for-current-os .download-os-windows .download-buttons a').click()

    import os
    files = os.listdir('/tmp')
    print(files)

    def wait_file(_):
        return len(files) < len(os.listdir('/tmp'))

    wait.until(wait_file)
    time.sleep(10)
