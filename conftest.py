"""
Pytest фикстуры для тестов
"""

import pytest
from utils.driver_factory import DriverFactory


@pytest.fixture
def driver():
    """
    Фикстура для создания и закрытия драйвера
    """
    driver = DriverFactory.get_driver(headless=False)
    yield driver
    DriverFactory.quit_driver(driver)


@pytest.fixture
def driver_headless():
    """
    Фикстура для создания драйвера в headless режиме
    """
    driver = DriverFactory.get_driver(headless=True)
    yield driver
    DriverFactory.quit_driver(driver)


@pytest.fixture
def login_page(driver):
    """
    Фикстура для создания страницы логина
    """
    from pages.login_page import LoginPage
    page = LoginPage(driver)
    page.open()
    return page