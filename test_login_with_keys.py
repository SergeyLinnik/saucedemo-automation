"""
Тест авторизации с использованием имитации нажатия клавиш
"""

import pytest
import time
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from config.test_data import TestData


class TestLoginWithKeys:
    """Класс с тестом для проверки авторизации через имитацию нажатия клавиш"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Настройка перед тестом"""
        self.login_page = LoginPage(driver)
        self.login_page.open()
    
    def test_login_with_keys(self, driver):
        """Тест авторизации с использованием клавиатуры (полный способ)"""
        print("\n" + "=" * 60)
        print("ТЕСТ: АВТОРИЗАЦИЯ С ИСПОЛЬЗОВАНИЕМ КЛАВИАТУРЫ")
        print("=" * 60)
        
        print("\n[Шаг 1] Ввод неверных данных...")
        username_field = driver.find_element(By.XPATH, "//input[@id='user-name']")
        password_field = driver.find_element(By.XPATH, "//input[@id='password']")
        
        username_field.send_keys("wrong_user")
        password_field.send_keys("wrong_password")
        print("Введены неверные данные")
        
        print("\n[Шаг 2] Очистка полей и ввод корректных данных...")
        self.login_page.login_with_keys(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        
        time.sleep(2)
        
        print("\n[Шаг 3] Проверка результата...")
        current_url = driver.current_url
        print(f"Текущий URL: {current_url}")
        
        assert TestData.SUCCESS_URL_PART in current_url, \
            f"Авторизация не выполнена. Текущий URL: {current_url}"
        
        print("Авторизация успешно выполнена")
        print("\n" + "=" * 60)
        print("[ТЕСТ] ПРОЙДЕН")
        print("=" * 60)


if __name__ == "__main__":
    pytest.main(["-v", __file__])