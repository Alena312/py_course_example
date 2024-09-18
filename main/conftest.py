import os
import shutil
import sys

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


@pytest.fixture(scope='session')
def repo_root():
    # выводит C:\Users\user\Desktop\py_course_example\main - директорию, в которой лежит этот конфтест
    print(f'.........path: {os.path.abspath(os.path.join(__file__, os.path.pardir))}')
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def base_dir():
    if sys.platform.startswith('win'):
        base_dir = 'C:\\Users\\user\\Desktop\\py_course_example\\tmp_dir'
    else:
        base_dir = '/tmp/tests'

    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    return base_dir


@pytest.fixture()
def test_dir(request, base_dir):
    # print(os.environ['PYTEST_CURRENT_TEST'])
    test_name = request._pyfuncitem.nodeid
    test_dir = os.path.join(base_dir, test_name
                            .replace('/', '_')
                            .replace(':', '_')
                            .replace('-', '_')
                            .replace('[', '_')
                            .replace(']', '_'))
    os.makedirs(test_dir)
    return test_dir
