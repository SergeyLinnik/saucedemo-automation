"""
Тест имитации нажатия клавиш для работы с полями ввода
"""

import pytest
import time
from pages.login_page import LoginPage
from config.test_data import TestData


class TestKeyboardActions:
    """
    Класс с тестами для проверки имитации нажатия клавиш
    """
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        Настройка перед каждым тестом
        """
        self.login_page = LoginPage(driver)
        self.login_page.open()
    
    def test_clear_fields_with_clear_method(self, driver):
        """
        Тест 1: Очистка полей методом clear()
        """
        print("\n[Тест 1] Очистка полей методом clear()")
        
        # Вводим данные
        self.login_page.enter_username(TestData.VALID_USERNAME)
        self.login_page.enter_password(TestData.VALID_PASSWORD)
        print("Данные введены")
        
        # Проверяем, что данные введены
        assert self.login_page.get_username_value() == TestData.VALID_USERNAME
        assert self.login_page.get_password_value() == TestData.VALID_PASSWORD
        print("Проверка: данные введены корректно")
        
        # Очищаем поля методом clear()
        self.login_page.clear_username_field()
        self.login_page.clear_password_field()
        
        # Проверяем, что поля очистились
        assert self.login_page.is_username_empty(), "Поле логина не очистилось"
        assert self.login_page.is_password_empty(), "Поле пароля не очистилось"
        print("Проверка: поля успешно очищены")
        
        print("[Тест 1] ПРОЙДЕН")
    
    def test_select_all_text(self, driver):
        """
        Тест 2: Выделение текста в полях
        """
        print("\n[Тест 2] Выделение текста в полях")
        
        # Вводим данные
        self.login_page.enter_username(TestData.VALID_USERNAME)
        self.login_page.enter_password(TestData.VALID_PASSWORD)
        print("Данные введены")
        
        # Выделяем текст в поле логина
        self.login_page.select_all_in_username()
        print("Текст в поле логина выделен")
        
        # Выделяем текст в поле пароля
        self.login_page.select_all_in_password()
        print("Текст в поле пароля выделен")
        
        # Проверяем, что поля не пустые (текст есть)
        assert self.login_page.get_username_value() == TestData.VALID_USERNAME
        assert self.login_page.get_password_value() == TestData.VALID_PASSWORD
        print("Проверка: текст в полях присутствует")
        
        print("[Тест 2] ПРОЙДЕН")
    
    def test_tab_navigation(self, driver):
        """
        Тест 3: Навигация между полями с помощью Tab
        """
        print("\n[Тест 3] Навигация между полями с помощью Tab")
        
        # Нажимаем Tab для перехода к полю логина
        self.login_page.press_tab()
        
        # Вводим логин
        self.login_page.enter_username(TestData.VALID_USERNAME)
        print("Логин введен")
        
        # Нажимаем Tab для перехода к полю пароля
        self.login_page.press_tab()
        
        # Вводим пароль
        self.login_page.enter_password(TestData.VALID_PASSWORD)
        print("Пароль введен")
        
        # Проверяем, что данные введены
        assert self.login_page.get_username_value() == TestData.VALID_USERNAME
        assert self.login_page.get_password_value() == TestData.VALID_PASSWORD
        print("Проверка: данные успешно введены с использованием Tab")
        
        print("[Тест 3] ПРОЙДЕН")
    
    def test_login_with_enter_key(self, driver):
        """
        Тест 4: Авторизация с помощью клавиши Enter
        """
        print("\n[Тест 4] Авторизация с помощью клавиши Enter")
        
        # Выполняем авторизацию через Enter
        self.login_page.login_with_enter(
            TestData.VALID_USERNAME, 
            TestData.VALID_PASSWORD
        )
        
        # Проверяем успешную авторизацию
        time.sleep(2)
        assert TestData.SUCCESS_URL_PART in driver.current_url, \
            "Авторизация через Enter не удалась"
        print("Проверка: авторизация через Enter успешна")
        
        print("[Тест 4] ПРОЙДЕН")
    
    def test_clear_and_relogin(self, driver):
        """
        Тест 5: Очистка полей и повторная авторизация
        """
        print("\n[Тест 5] Очистка полей и повторная авторизация")
        
        # Вводим неверные данные
        self.login_page.enter_username(TestData.VALID_USERNAME)
        self.login_page.enter_password(TestData.INVALID_PASSWORD)
        self.login_page.click_login_button()
        
        # Проверяем ошибку
        assert self.login_page.is_error_displayed(), "Ошибка не отображается"
        print("Ошибка отображается")
        
        # Очищаем поля методом clear()
        self.login_page.clear_username_field()
        self.login_page.clear_password_field()
        print("Поля очищены")
        
        # Вводим правильные данные
        self.login_page.enter_username(TestData.VALID_USERNAME)
        self.login_page.enter_password(TestData.VALID_PASSWORD)
        print("Правильные данные введены")
        
        # Нажимаем кнопку входа
        self.login_page.click_login_button()
        print("Нажата кнопка входа")
        
        # Проверяем успешную авторизацию
        time.sleep(2)
        assert TestData.SUCCESS_URL_PART in driver.current_url, \
            f"Повторная авторизация не удалась. Текущий URL: {driver.current_url}"
        print("Проверка: повторная авторизация успешна")
        
        print("[Тест 5] ПРОЙДЕН")


if __name__ == "__main__":
    pytest.main(["-v", __file__])