from selenium.webdriver import Remote
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from typing import Union, Type, List, TypeVar, Optional
import logging

# from ui.page_object.page import BasePage
from ui.page_object.advanced.wait import Wait

logger = logging.getLogger()

class TimeOuts:
    """ Таймауты для UI-тестов"""

    # для поиска элементов в Element/Elements
    SEARCH = 5

    # для ожиданий
    SHORT_WAIT = 2
    MEDIUM_WAIT = 5
    LONG_WAIT = 15


# чтобы в каждой пейдже не импортировать селениум, а тащить все из этого модуля
Locators = By


class EmptyWebElement(object):
    """ Заглушка с описанием элемента, которую возвращаем, если элемент не найден"""

    def __init__(self):
        pass


class Page:
    """
    Базовый класс для описания всех страниц. На страницы добавляются секции/элементы
    Пример:
        class MainPage(Page):
            input = Element(Locators.XPATH, '//a')
    """

    # для каждой страницы прописываем путь, по которой ее можно открыть
    @property
    def path(self):
        raise NotImplementedError

    def __init__(self, driver: Remote):
        self.driver = driver
        self.wait = Wait(self.driver) #  меня такого нет, некуда обратиться за Wait
        self.timeout = TimeOuts


PageBoundVar = TypeVar('PageBoundVar', bound=Page)


class Section:
    """
    Класс для переиспользования одинаковых блоков на разных страницах.
    На класс секции накидываются элементы, которые будут искаться относительно локаторов самой секции, а не всей страницы.
    Пример:
    class DropDownList(Section):
        block = Element(Locators.CSS_SELECTOR, '.drop_down_form')
        items = Element(Locators.CSS_SELECTOR, 'ul li')
        def select(text):
            self.block.click()
            self.wait.until(lambda _: len(self.items) > 0, message='Список элементов не появился')
            for el in self.items:
                if el.text == text:
                    el.click(Locators.CSS_SELECTOR, '.class_name')

    class MainPage(Page):
        section_name = Section()
    """

    def __init__(self, by: str, locator: str, description: str):
        self.by = by
        self.locator = locator
        # драйвер появится на секции, при обращении к ней из теста (в __get__)
        self.root = lambda: self.driver.find_element(self.by, self.locator)
        # при поиске секции используем это поле для отчета
        self.description = f'<{description}>'
        # драйвер будет инициализирован во время выполнения тестов на пейдже. В __get__ секции получим драйвер
        # noinspection PyTypeChecker
        self.driver: Remote = None
        # noinspection PyTypeChecker
        self.wait: Optional[Wait] = None
        self.timeout = TimeOuts

    @property
    def root(self) -> WebElement:
        """
        Возвращает объект, относительно которого будем искать элементы
        Методы для поиска элементов (find_element, find_elements) есть у драйвера (WebDriver класс)
        и элементов (WebElements)
        """
        return self.method()

    @root.setter
    def root(self, value):
        """
        Устанавливаем метод, которым будем искать рутовый элемент секции
        """
        self.method = value

    def __get__(self, instance: Page, owner: Type[Page]):  # NOQA
        # сохраняем драйвер на секцию, чтобы получить к нему доступ из методов секции
        self.driver = instance.driver
        self.wait = Wait(self.driver)

        if isinstance(instance, Section):
            # надо подумать, как это можно было бы реализовать
            raise TypeError('Секция не может быть вложена в секцию!')

        # Для доступа до элементов секции возвращаем self.
        # Если в тесте нужен будет WebElement привязанный к секции -- просто вызовем section_object.root
        return self


class Element:
    """
    Класс-обертка для обращения к элементам страницы
    """

    def __init__(self, by, locator, description):
        self.by = by
        self.locator = locator
        # текст, который будет использоваться в отчете для обозначения элемента
        self.description = f'<{description}>'
        self.timeout = TimeOuts

    def __get__(self, instance: Union[Page, Section], owner: Union[Type[Page], Type[Section]]) -> TWebElement:
        """
        Для ленивой инициализации используем дескрипторы https://docs.python.org/3/howto/descriptor.html
        Это позволит искать элементы непосредственно перед их использованием в тесте
        и минимизирует количество ошибок StateElementReferenceException, NoSuchElement итд
        """

        if isinstance(instance, Page):
            method = lambda _: instance.driver.find_element(self.by, self.locator)
        elif isinstance(instance, Section):
            try:
                # в биндингах селениума захардкожен перехват ошибки NoSuchElementException
                # поэтому при попытке в ожидании найти секцию, которой нет на странице, вместо NoSuchElementException
                # мы получаем TimeOutException и то сообщение, которое передано в ожидании. Это сильно сбивает с толку
                # и усложняет разбор теста. Поэтому, прежде чем искать элемент на странице, чекаем, что сама секция есть
                # noinspection PyStatementEffect
                instance.root
            except NoSuchElementException:
                raise RuntimeError(f'На странице нет секции {instance.__doc__}')
            # https://github.com/seleniumhq/selenium-google-code-issue-archive/issues/7312
            # WebDriver follows the XPath spec for location of elements.This means there is no implied context node,
            # which means that even if you use WebElement.findElement(By.xpath("//foo/...")), the "//" operator searches
            # from the root node of the document.The proper way to accomplish what you want is to use the following:
            #
            # container.find_element(By.XPATH, ".//*[@class='commonClass']")
            # Note the leading '.' on the XPath expression.

            if self.locator.startswith('//') or self.locator.startswith('//'):
                logger.warning( 'using xpath with "//" operator can be ambiguous ' 
                                'https://github.com/seleniumhq/selenium-google-code-issue-archive/issues/7312')

            method = lambda _: instance.root.find_element(self.by, self.locator)

        else:
            raise TypeError('Элемент не прикреплен ни к странице, ни к секции')

        try:
            logger.info(f'Search {self.description} by: {self.by}, {self.locator}')
            web_element = Wait(instance.driver).until(method, timeout=self.timeout.SEARCH)
            # добавляем описание на WebElement, чтобы использовать его в ассертах
            web_element.description = self.description
            return web_element
        except (NoSuchElementException, TimeoutException):
            logger.info(f'no such element: {self.locator}')
            return EmptyWebElement(self.by, self.locator, self.description)

class Elements:
    """
    Класс-обертка для обращения к элементам страницы списком
    """

    def __init__(self, by, locator, description):
        self.by = by
        self.locator = locator
        # текст, который будет использоваться в отчете для обозначения элемента
        self.description = f'<{description}>'
        self.timeout = TimeOuts

    def __get__(self, instance: Union[Page, Section], owner: Union[Type[Page], Type[Section]]) -> List[WebElement]:
        if isinstance(instance, Page):
            method = instance.driver.find_elements
        elif isinstance(instance, Section):
            method = instance.root.find_elements()
        else:
            raise TypeError('Элемент не прикреплен ни к странице, ни к секции')

        # find_element вернет WebElement или кинет исключение
        # find_elements вернет список элементов или пустой список
        # также для списка не будет никакого ожидания
        logger.info(f'Search {self.description} by: {self.by}, {self.locator}')
        elements = []

        def search(_):
            nonlocal elements
            elements = method(self.by, self.locator)
            return len(elements) > 0

        # Для пачек элементов добавляем ожидание аналогично ожиданию при поиске одного элемента
        # скипаем все исключения -- пустой список тут это норма, в тесте решим, как его обработать
        try:
            Wait(instance.driver).until(search, timeout=self.timeout.SEARCH, ignored_exceptions=TimeoutException)
        except Exception as error:
            logger.error(error)

        for web_element in elements:
            web_element.description = self.description
            return elements

        elif isinstance(instance, Section):
            try:
                # в биндингах селениума захардкожен перехват ошибки NoSuchElementException
                # поэтому при попытке в ожидании найти секцию, которой нет на странице, вместо NoSuchElementException
                # мы получаем TimeOutException и то сообщение, которое передано в ожидании. Это сильно сбивает с толку
                # и усложняет разбор теста. Поэтому, прежде чем искать элемент на странице, чекаем, что сама секция есть
                # noinspection PyStatementEffect
                instance.root
            except NoSuchElementException:
                raise RuntimeError(f'На странице нет секции {instance.__doc__}')
            # https://github.com/seleniumhq/selenium-google-code-issue-archive/issues/7312
            # WebDriver follows the XPath spec for location of elements.This means there is no implied context node,
            # which means that even if you use WebElement.findElement(By.xpath("//foo/...")), the "//" operator searches
            # from the root node of the document.The proper way to accomplish what you want is to use the following:
            #
            # container.find_element(By.XPATH, ".//*[@class='commonClass']")
            # Note the leading '.' on the XPath expression.

            if self.locator.startswith('//') or self.locator.startswith('//'):
                logger.warning( 'using xpath with "//" operator can be ambiguous ' 
                                'https://github.com/seleniumhq/selenium-google-code-issue-archive/issues/7312')

            method = lambda _: instance.root.find_element(self.by, self.locator)

        else:
            raise TypeError('Элемент не прикреплен ни к странице, ни к секции')

        try:
            logger.info(f'Search {self.description} by: {self.by}, {self.locator}')
            web_element = Wait(instance.driver).until(method, timeout=self.timeout.SEARCH)
            # добавляем описание на WebElement, чтобы использовать его в ассертах
            web_element.description = self.description
            return web_element
        except (NoSuchElementException, TimeoutException):
            logger.info(f'no such element: {self.locator}')
            return EmptyWebElement(self.by, self.locator, self.description)
