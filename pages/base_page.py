"""
Базовый класс Page Object
Содержит общие методы для всех страниц
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """Базовый класс для всех Page Object"""
    
    def __init__(self, driver):
        """
        Инициализация базовой страницы
        
        Args:
            driver: Экземпляр веб-драйвера
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator: tuple, timeout: int = 10) -> WebElement:
        """
        Поиск элемента с ожиданием
        
        Args:
            locator: Кортеж (By.XPATH, "xpath_expression")
            timeout: Время ожидания в секундах
        
        Returns:
            WebElement: Найденный элемент
        
        Raises:
            TimeoutException: Если элемент не найден
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    def click_element(self, locator: tuple, timeout: int = 10) -> None:
        """
        Клик по элементу с ожиданием
        
        Args:
            locator: Кортеж (By.XPATH, "xpath_expression")
            timeout: Время ожидания в секундах
        """
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def enter_text(self, locator: tuple, text: str, timeout: int = 10) -> None:
        """
        Ввод текста в поле
        
        Args:
            locator: Кортеж (By.XPATH, "xpath_expression")
            text: Текст для ввода
            timeout: Время ожидания в секундах
        """
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator: tuple, timeout: int = 10) -> str:
        """
        Получение текста элемента
        
        Args:
            locator: Кортеж (By.XPATH, "xpath_expression")
            timeout: Время ожидания в секундах
        
        Returns:
            str: Текст элемента
        """
        element = self.find_element(locator, timeout)
        return element.text
    
    def is_element_displayed(self, locator: tuple, timeout: int = 5) -> bool:
        """
        Проверка отображения элемента
        
        Args:
            locator: Кортеж (By.XPATH, "xpath_expression")
            timeout: Время ожидания в секундах
        
        Returns:
            bool: True если элемент отображается, иначе False
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located(locator))
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False
    
    def get_current_url(self) -> str:
        """
        Получение текущего URL
        
        Returns:
            str: Текущий URL страницы
        """
        return self.driver.current_url
    
    def wait_for_url_contains(self, text: str, timeout: int = 10) -> bool:
        """
        Ожидание, что URL содержит указанный текст
        
        Args:
            text: Ожидаемый текст в URL
            timeout: Время ожидания в секундах
        
        Returns:
            bool: True если URL содержит текст
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.url_contains(text))
    
    def wait_for_element_visible(self, locator: tuple, timeout: int = 10) -> WebElement:
        """
        Ожидание видимости элемента
        
        Args:
            locator: Кортеж (By.XPATH, "xpath_expression")
            timeout: Время ожидания в секундах
        
        Returns:
            WebElement: Видимый элемент
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))