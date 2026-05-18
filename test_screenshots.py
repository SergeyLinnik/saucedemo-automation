"""
Тест создания скриншотов страницы каталога
"""

import pytest
import os
from pages.login_page import LoginPage
from config.test_data import TestData


class TestScreenshots:
    """
    Класс с тестами для проверки создания скриншотов
    """
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        Настройка перед каждым тестом
        """
        self.login_page = LoginPage(driver)
        self.login_page.open()
    
    def test_screenshot_of_catalog_page(self, driver):
        """
        Тест 1: Создание скриншота страницы каталога
        """
        print("\n[Тест 1] Создание скриншота страницы каталога")
        
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        self.login_page.wait_for_url_contains(TestData.SUCCESS_URL_PART)
        assert TestData.SUCCESS_URL_PART in driver.current_url
        print("Страница каталога загружена")
        
        screenshot_path = self.login_page.take_screenshot("catalog_page")
        
        assert os.path.exists(screenshot_path), f"Скриншот не создан: {screenshot_path}"
        print(f"Скриншот создан: {screenshot_path}")
        
        file_size = os.path.getsize(screenshot_path)
        assert file_size > 0, "Файл скриншота пустой"
        print(f"Размер скриншота: {file_size} байт")
        
        print("[Тест 1] ПРОЙДЕН")
    
    def test_screenshot_with_date(self, driver):
        """
        Тест 2: Создание скриншота с датой в имени
        """
        print("\n[Тест 2] Создание скриншота с датой в имени")
        
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        self.login_page.wait_for_url_contains(TestData.SUCCESS_URL_PART)
        
        screenshot_path = self.login_page.take_screenshot_with_date("catalog")
        
        assert os.path.exists(screenshot_path), "Скриншот с датой не создан"
        print(f"Скриншот с датой создан: {screenshot_path}")
        
        print("[Тест 2] ПРОЙДЕН")
    
    def test_screenshot_before_login(self, driver):
        """
        Тест 3: Создание скриншота страницы логина
        """
        print("\n[Тест 3] Создание скриншота страницы логина")
        
        screenshot_path = self.login_page.take_screenshot("login_page")
        
        assert os.path.exists(screenshot_path), "Скриншот страницы логина не создан"
        print(f"Скриншот страницы логина создан: {screenshot_path}")
        
        print("[Тест 3] ПРОЙДЕН")
    
    def test_screenshot_after_error(self, driver):
        """
        Тест 4: Создание скриншота после ошибки авторизации
        """
        print("\n[Тест 4] Создание скриншота после ошибки авторизации")
        
        self.login_page.login(TestData.VALID_USERNAME, TestData.INVALID_PASSWORD)
        assert self.login_page.is_error_displayed(), "Ошибка не отображается"
        print("Ошибка отображается")
        
        screenshot_path = self.login_page.take_screenshot("error_page")
        
        assert os.path.exists(screenshot_path), "Скриншот ошибки не создан"
        print(f"Скриншот ошибки создан: {screenshot_path}")
        
        print("[Тест 4] ПРОЙДЕН")
    
    def test_multiple_screenshots(self, driver):
        """
        Тест 5: Создание нескольких скриншотов
        """
        print("\n[Тест 5] Создание нескольких скриншотов")
        
        path1 = self.login_page.take_screenshot("step_1_login")
        print(f"Скриншот 1: {path1}")
        
        self.login_page.enter_username(TestData.VALID_USERNAME)
        path2 = self.login_page.take_screenshot("step_2_username")
        print(f"Скриншот 2: {path2}")
        
        self.login_page.enter_password(TestData.VALID_PASSWORD)
        path3 = self.login_page.take_screenshot("step_3_password")
        print(f"Скриншот 3: {path3}")
        
        self.login_page.click_login_button()
        self.login_page.wait_for_url_contains(TestData.SUCCESS_URL_PART)
        path4 = self.login_page.take_screenshot("step_4_catalog")
        print(f"Скриншот 4: {path4}")
        
        assert os.path.exists(path1), "Скриншот 1 не создан"
        assert os.path.exists(path2), "Скриншот 2 не создан"
        assert os.path.exists(path3), "Скриншот 3 не создан"
        assert os.path.exists(path4), "Скриншот 4 не создан"
        print("Все 4 скриншота успешно созданы")
        
        print("[Тест 5] ПРОЙДЕН")


if __name__ == "__main__":
    pytest.main(["-v", __file__])