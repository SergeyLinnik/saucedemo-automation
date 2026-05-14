"""
Негативные тесты авторизации на сайте Saucedemo
"""

import pytest
from pages.login_page import LoginPage
from config.test_data import TestData


class TestNegativeLogin:
    """
    Класс с негативными тестами авторизации
    """
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        Настройка перед каждым тестом
        """
        self.login_page = LoginPage(driver)
        self.login_page.open()
    
    def test_invalid_password(self, driver):
        """
        Тест 1: Авторизация с неверным паролем
        """
        print("\n[Тест 1] Авторизация с неверным паролем")
        
        # Выполнение входа с неверным паролем
        self.login_page.login(TestData.VALID_USERNAME, TestData.INVALID_PASSWORD)
        
        # Проверка отображения ошибки
        assert self.login_page.is_error_displayed(), "Ошибка: Сообщение об ошибке не отображается"
        print("Сообщение об ошибке отображается")
        
        # Проверка текста ошибки
        error_text = self.login_page.get_error_text()
        assert error_text == TestData.ERROR_MATCH, \
            f"Ошибка: Текст ошибки не соответствует. Ожидалось: '{TestData.ERROR_MATCH}', Получено: '{error_text}'"
        print("Текст ошибки корректен")
        
        # Проверка, что URL не изменился
        assert TestData.SUCCESS_URL_PART not in driver.current_url, \
            "Ошибка: URL изменился, авторизация не должна была пройти"
        print("URL не изменился")
        
        # Закрытие ошибки
        self.login_page.close_error()
        print("Кнопка закрытия ошибки нажата")
        
        # Проверка, что ошибка закрылась
        assert self.login_page.is_error_closed(), "Ошибка: Сообщение об ошибке не закрылось"
        print("Сообщение об ошибке успешно закрыто")
        
        print("[Тест 1] ПРОЙДЕН")
    
    def test_invalid_username(self, driver):
        """
        Тест 2: Авторизация с неверным логином
        """
        print("\n[Тест 2] Авторизация с неверным логином")
        
        # Выполнение входа с неверным логином
        self.login_page.login(TestData.INVALID_USERNAME, TestData.VALID_PASSWORD)
        
        # Проверка отображения ошибки
        assert self.login_page.is_error_displayed(), "Сообщение об ошибке не отображается"
        print("Сообщение об ошибке отображается")
        
        # Проверка текста ошибки
        error_text = self.login_page.get_error_text()
        assert error_text == TestData.ERROR_MATCH, f"Текст ошибки: {error_text}"
        print("Текст ошибки корректен")
        
        # Проверка URL
        assert TestData.SUCCESS_URL_PART not in driver.current_url, "URL изменился"
        print("URL не изменился")
        
        # Закрытие ошибки
        self.login_page.close_error()
        assert self.login_page.is_error_closed(), "Ошибка не закрылась"
        print("Сообщение об ошибке закрыто")
        
        print("[Тест 2] ПРОЙДЕН")
    
    def test_empty_fields(self, driver):
        """
        Тест 3: Авторизация с пустыми полями
        """
        print("\n[Тест 3] Авторизация с пустыми полями")
        
        # Выполнение входа с пустыми полями
        self.login_page.click_login_button()
        
        # Ожидание появления ошибки
        self.login_page.wait_for_error()
        
        # Проверка отображения ошибки
        assert self.login_page.is_error_displayed(), "Сообщение об ошибке не отображается"
        print("Сообщение об ошибке отображается")
        
        # Проверка текста ошибки
        error_text = self.login_page.get_error_text()
        assert error_text == TestData.ERROR_REQUIRED, f"Текст ошибки: {error_text}"
        print("Текст ошибки корректен")
        
        # Проверка URL
        assert TestData.SUCCESS_URL_PART not in driver.current_url, "URL изменился"
        print("URL не изменился")
        
        # Закрытие ошибки
        self.login_page.close_error()
        assert self.login_page.is_error_closed(), "Ошибка не закрылась"
        print("Сообщение об ошибке закрыто")
        
        print("[Тест 3] ПРОЙДЕН")
    
    def test_locked_user(self, driver):
        """
        Тест 4: Авторизация заблокированного пользователя
        """
        print("\n[Тест 4] Авторизация заблокированного пользователя")
        
        # Выполнение входа заблокированным пользователем
        self.login_page.login(TestData.LOCKED_USERNAME, TestData.VALID_PASSWORD)
        
        # Проверка отображения ошибки
        assert self.login_page.is_error_displayed(), "Сообщение об ошибке не отображается"
        print("Сообщение об ошибке отображается")
        
        # Проверка текста ошибки
        error_text = self.login_page.get_error_text()
        assert error_text == TestData.ERROR_LOCKED, f"Текст ошибки: {error_text}"
        print("Текст ошибки корректен")
        
        # Проверка URL
        assert TestData.SUCCESS_URL_PART not in driver.current_url, "URL изменился"
        print("URL не изменился")
        
        # Закрытие ошибки
        self.login_page.close_error()
        assert self.login_page.is_error_closed(), "Ошибка не закрылась"
        print("Сообщение об ошибке закрыто")
        
        print("[Тест 4] ПРОЙДЕН")


if __name__ == "__main__":
    pytest.main(["-v", __file__])