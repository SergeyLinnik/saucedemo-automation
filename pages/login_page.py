"""
Page Object для страницы логина Saucedemo
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.test_data import TestData


class LoginPage(BasePage):
    """Класс для работы со страницей логина"""
    
    # Локаторы элементов страницы
    USERNAME_INPUT = (By.XPATH, "//input[@id='user-name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@id='password']")
    LOGIN_BUTTON = (By.XPATH, "//input[@id='login-button']")
    ERROR_CONTAINER = (By.XPATH, "//div[@class='error-message-container error']")
    ERROR_TEXT = (By.XPATH, "//div[@class='error-message-container error']//h3")
    ERROR_CLOSE_BUTTON = (By.XPATH, "//button[@class='error-button']")
    
    def __init__(self, driver):
        """
        Инициализация страницы логина
        
        Args:
            driver: Экземпляр веб-драйвера
        """
        super().__init__(driver)
    
    def open(self) -> None:
        """
        Открытие страницы логина
        """
        self.driver.get(TestData.BASE_URL)
    
    def enter_username(self, username: str) -> None:
        """
        Ввод логина
        
        Args:
            username: Логин для ввода
        """
        self.enter_text(self.USERNAME_INPUT, username)
    
    def enter_password(self, password: str) -> None:
        """
        Ввод пароля
        
        Args:
            password: Пароль для ввода
        """
        self.enter_text(self.PASSWORD_INPUT, password)
    
    def click_login_button(self) -> None:
        """
        Нажатие кнопки входа
        """
        self.click_element(self.LOGIN_BUTTON)
    
    def login(self, username: str, password: str) -> None:
        """
        Выполнение авторизации
        
        Args:
            username: Логин
            password: Пароль
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
    
    def is_error_displayed(self) -> bool:
        """
        Проверка отображения сообщения об ошибке
        
        Returns:
            bool: True если ошибка отображается, иначе False
        """
        return self.is_element_displayed(self.ERROR_CONTAINER)
    
    def get_error_text(self) -> str:
        """
        Получение текста сообщения об ошибке
        
        Returns:
            str: Текст сообщения об ошибке
        """
        return self.get_text(self.ERROR_TEXT)
    
    def close_error(self) -> None:
        """
        Закрытие сообщения об ошибке
        """
        if self.is_error_displayed():
            self.click_element(self.ERROR_CLOSE_BUTTON)
    
    def is_error_closed(self) -> bool:
        """
        Проверка, что сообщение об ошибке закрыто
        
        Returns:
            bool: True если ошибка не отображается, иначе False
        """
        return not self.is_error_displayed()
    
    def wait_for_error(self, timeout: int = 5) -> None:
        """
        Ожидание появления ошибки
        
        Args:
            timeout: Время ожидания в секундах
        """
        self.wait_for_element_visible(self.ERROR_CONTAINER, timeout)