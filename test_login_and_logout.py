"""
Тест авторизации, открытия скрытого меню и выхода из системы
"""

import pytest
import time
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from config.test_data import TestData


class TestLoginAndLogout:
    """
    Класс с тестом для проверки:
    1. Авторизация на сайте
    2. Открытие скрытого бургер-меню
    3. Разлогинивание (выход из системы)
    """
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Настройка перед тестом: открытие страницы логина"""
        self.login_page = LoginPage(driver)
        self.login_page.open()
    
    def test_login_open_menu_and_logout(self, driver):
        """
        Тест: Авторизация -> Открытие скрытого меню -> Выход из системы
        """
        print("\n" + "=" * 60)
        print("ТЕСТ: АВТОРИЗАЦИЯ, ОТКРЫТИЕ МЕНЮ, ВЫХОД ИЗ СИСТЕМЫ")
        print("=" * 60)
        
        # =========================================================
        # ШАГ 1: АВТОРИЗАЦИЯ НА САЙТЕ
        # =========================================================
        print("\n[Шаг 1] Авторизация на сайте...")
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        
        # Ожидание загрузки страницы каталога
        time.sleep(2)
        
        # Проверка успешной авторизации
        assert self.login_page.is_logged_in(), \
            f"Авторизация не выполнена. Текущий URL: {driver.current_url}"
        print("Авторизация успешно выполнена")
        print(f"Текущий URL: {driver.current_url}")
        
        # =========================================================
        # ШАГ 2: ОТКРЫТИЕ СКРЫТОГО БУРГЕР-МЕНЮ
        # =========================================================
        print("\n[Шаг 2] Открытие скрытого бургер-меню...")
        self.login_page.open_burger_menu()
        
        # Небольшая задержка для анимации открытия меню
        time.sleep(1)
        print("Бургер-меню успешно открыто")
        
        # Проверяем, что кнопка Logout отображается в меню
        logout_button = driver.find_element(By.XPATH, "//a[@id='logout_sidebar_link']")
        assert logout_button.is_displayed(), "Кнопка Logout не отображается в меню"
        print("Кнопка Logout отображается в меню")
        
        # =========================================================
        # ШАГ 3: ВЫХОД ИЗ СИСТЕМЫ (РАЗЛОГИНИВАНИЕ)
        # =========================================================
        print("\n[Шаг 3] Выход из системы...")
        self.login_page.click_logout()
        
        # Ожидание перенаправления на страницу логина
        time.sleep(2)
        
        # Проверка, что выход выполнен успешно
        assert self.login_page.is_logged_out(), \
            f"Выход из системы не выполнен. Текущий URL: {driver.current_url}"
        print("Выход из системы успешно выполнен")
        print(f"Текущий URL: {driver.current_url}")
        
        # Дополнительная проверка: поле логина должно быть доступно
        username_field = driver.find_element(By.XPATH, "//input[@id='user-name']")
        assert username_field.is_displayed(), "Поле логина не отображается после выхода"
        print("Поле логина отображается на странице входа")
        
        # =========================================================
        # ВЫВОД РЕЗУЛЬТАТА
        # =========================================================
        print("\n" + "=" * 60)
        print("РЕЗУЛЬТАТ ТЕСТА:")
        print("=" * 60)
        print("Авторизация на сайте - ВЫПОЛНЕНО")
        print("Открытие скрытого меню - ВЫПОЛНЕНО")
        print("Разлогинивание (выход) - ВЫПОЛНЕНО")
        print("=" * 60)
        print("[ТЕСТ] ПРОЙДЕН")


if __name__ == "__main__":
    pytest.main(["-v", __file__])