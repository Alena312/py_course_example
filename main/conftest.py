import pytest


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
