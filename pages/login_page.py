"""
Page Object для страницы логина Saucedemo
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
    
    # =========================================================
    # МЕТОДЫ ДЛЯ РАБОТЫ С КЛАВИШАМИ (ИСПРАВЛЕННЫЕ)
    # =========================================================
    
    def clear_username_field(self) -> None:
        """
        Очистка поля логина
        """
        username_field = self.find_element(self.USERNAME_INPUT)
        username_field.clear()
        print("[INFO] Поле логина очищено методом clear()")
    
    def clear_password_field(self) -> None:
        """
        Очистка поля пароля
        """
        password_field = self.find_element(self.PASSWORD_INPUT)
        password_field.clear()
        print("[INFO] Поле пароля очищено методом clear()")
    
    def select_all_in_username(self) -> None:
        """
        Выделение текста в поле логина (Ctrl+A)
        """
        username_field = self.find_element(self.USERNAME_INPUT)
        username_field.click()
        username_field.send_keys(Keys.CONTROL, "a")
        print("[INFO] Текст в поле логина выделен")
    
    def select_all_in_password(self) -> None:
        """
        Выделение текста в поле пароля (Ctrl+A)
        """
        password_field = self.find_element(self.PASSWORD_INPUT)
        password_field.click()
        password_field.send_keys(Keys.CONTROL, "a")
        print("[INFO] Текст в поле пароля выделен")
    
    def delete_with_keys(self, locator: tuple) -> None:
        """
        Удаление текста с помощью клавиш Delete
        
        Args:
            locator: Локатор элемента
        """
        element = self.find_element(locator)
        element.click()
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        print("[INFO] Текст удален с помощью клавиш")
    
    def press_tab(self) -> None:
        """
        Нажатие клавиши Tab
        """
        active_element = self.driver.switch_to.active_element
        active_element.send_keys(Keys.TAB)
        print("[INFO] Нажата клавиша Tab")
    
    def press_enter(self) -> None:
        """
        Нажатие клавиши Enter
        """
        active_element = self.driver.switch_to.active_element
        active_element.send_keys(Keys.ENTER)
        print("[INFO] Нажата клавиша Enter")
    
    def login_with_enter(self, username: str, password: str) -> None:
        """
        Авторизация с помощью клавиши Enter
        
        Args:
            username: Логин
            password: Пароль
        """
        self.enter_username(username)
        self.press_tab()
        self.enter_password(password)
        self.press_enter()
        print("[INFO] Форма отправлена через Enter")
    
    def get_username_value(self) -> str:
        """
        Получение значения поля логина
        
        Returns:
            str: Значение поля логина
        """
        element = self.find_element(self.USERNAME_INPUT)
        return element.get_attribute("value")
    
    def get_password_value(self) -> str:
        """
        Получение значения поля пароля
        
        Returns:
            str: Значение поля пароля
        """
        element = self.find_element(self.PASSWORD_INPUT)
        return element.get_attribute("value")
    
    def is_username_empty(self) -> bool:
        """
        Проверка, что поле логина пустое
        
        Returns:
            bool: True если поле пустое
        """
        return self.get_username_value() == ""
    
    def is_password_empty(self) -> bool:
        """
        Проверка, что поле пароля пустое
        
        Returns:
            bool: True если поле пустое
        """
        return self.get_password_value() == ""